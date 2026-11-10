"""Offline graph/name contract tests over actual JSON input, not line matching."""
import copy
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
SCRIPT = HERE.parents[1] / 'skills/github-actions-workflow-authoring/scripts/check-workflow-contract.py'
GOOD = json.loads((HERE / 'fixtures/workflow.json').read_text())
RULES = json.loads((HERE / 'fixtures/rules.json').read_text())


class WorkflowTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix='workflow-contract-')
        self.root = Path(self.tmp.name)

    def tearDown(self):
        self.tmp.cleanup()

    def run_cli(self, data=None, rules=RULES, raw=False):
        (self.root / 'workflow.json').write_text(data if raw else json.dumps(data or GOOD))
        (self.root / 'rules.json').write_text(json.dumps(rules))
        before = {p.name: p.read_bytes() for p in self.root.iterdir()}
        result = subprocess.run([sys.executable, str(SCRIPT), 'workflow.json', '--rules', 'rules.json'],
                              cwd=self.root, capture_output=True, text=True)
        self.assertEqual(before, {p.name: p.read_bytes() for p in self.root.iterdir()}, 'checker must not write')
        return result

    def test_pass_repeat_and_read_only(self):
        first = self.run_cli(GOOD)
        before = {p.name: p.read_bytes() for p in self.root.iterdir()}
        second = self.run_cli(GOOD)
        self.assertEqual(first.returncode, 0, first.stderr)
        self.assertEqual(json.loads(first.stdout)['required_contexts'], 1)
        self.assertEqual(first.stdout, second.stdout)
        self.assertEqual(before, {p.name: p.read_bytes() for p in self.root.iterdir()})

    def test_missing_declarations_and_fake_text(self):
        for key, expected in (('permissions', 'permissions'), ('concurrency', 'concurrency'), ('on', 'on key')):
            data = copy.deepcopy(GOOD)
            del data[key]
            data['jobs']['build']['steps'][0]['run'] = '# permissions: {}\n# concurrency: ci\n# on: pull_request'
            result = self.run_cli(data)
            self.assertEqual(result.returncode, 1, result.stderr)
            self.assertIn(expected, result.stdout)

    def test_timeout_not_supplied_by_comment(self):
        data = copy.deepcopy(GOOD)
        del data['jobs']['build']['timeout-minutes']
        data['jobs']['build']['steps'][0]['run'] = '# timeout-minutes: 10\ntrue'
        result = self.run_cli(data)
        self.assertEqual(result.returncode, 1)
        self.assertIn('runner timeout', result.stdout)

    def test_timeout_rejects_bool_zero_and_expression(self):
        for value in (True, 0, -1, '${{ inputs.timeout }}'):
            data = copy.deepcopy(GOOD)
            data['jobs']['build']['timeout-minutes'] = value
            self.assertEqual(self.run_cli(data).returncode, 1)

    def test_reusable_call_does_not_need_runner_timeout(self):
        data = copy.deepcopy(GOOD)
        data['jobs']['call'] = {'uses': 'fixture/workflows/.github/workflows/check.yml@' + 'a' * 40}
        self.assertEqual(self.run_cli(data).returncode, 0)

    def test_unknown_dependency_and_cycle(self):
        data = copy.deepcopy(GOOD)
        data['jobs']['build']['needs'] = 'missing'
        self.assertIn('needs job ID', self.run_cli(data).stdout)
        data['jobs']['build']['needs'] = 'gate'
        result = self.run_cli(data)
        self.assertEqual(result.returncode, 1)
        self.assertIn('cycle', result.stdout)

    def test_required_context_missing_matrix_dynamic_and_duplicate(self):
        for change in ('missing', 'matrix', 'dynamic', 'duplicate', 'caller'):
            data = copy.deepcopy(GOOD)
            if change == 'missing':
                del data['jobs']['gate']
            elif change == 'matrix':
                data['jobs']['gate']['strategy'] = {'matrix': {'os': ['linux', 'mac']}}
            elif change == 'dynamic':
                data['jobs']['gate']['name'] = '${{ inputs.name }}'
            elif change == 'caller':
                data['jobs']['gate'] = {'name': 'CI', 'uses': 'fixture/workflows/.github/workflows/check.yml@' + 'a' * 40}
            else:
                data['jobs']['second'] = copy.deepcopy(data['jobs']['gate'])
            result = self.run_cli(data)
            self.assertEqual(result.returncode, 1, result.stderr)
            self.assertIn('required context', result.stdout)

    def test_job_level_concurrency_and_direct_rule_list(self):
        data = copy.deepcopy(GOOD)
        del data['concurrency']
        for job in data['jobs'].values():
            job['concurrency'] = 'fixture'
        self.assertEqual(self.run_cli(data, RULES[0]['rules']).returncode, 0)

    def test_environment_job_cannot_override_workflow_cancellation(self):
        data = copy.deepcopy(GOOD)
        data['jobs']['gate']['environment'] = 'fixture-production'
        data['jobs']['gate']['concurrency'] = {'group': 'fixture-production', 'cancel-in-progress': False}
        result = self.run_cli(data)
        self.assertEqual(result.returncode, 1)
        self.assertIn('workflow cancellation', result.stdout)
        data['concurrency']['cancel-in-progress'] = False
        self.assertEqual(self.run_cli(data).returncode, 0)
        data['jobs']['gate']['concurrency']['cancel-in-progress'] = True
        self.assertIn('job cancellation', self.run_cli(data).stdout)
        data['jobs']['gate']['concurrency']['cancel-in-progress'] = '${{ inputs.cancel }}'
        self.assertEqual(self.run_cli(data).returncode, 1)

    def test_legacy_required_contexts_and_checks(self):
        self.assertEqual(self.run_cli(GOOD, {'contexts': ['CI'], 'checks': [{'context': 'CI'}]}).returncode, 0)
        self.assertEqual(self.run_cli(GOOD, {'checks': [{'context': 'absent'}]}).returncode, 1)
        self.assertEqual(self.run_cli(GOOD, {'contexts': 'CI'}).returncode, 2)

    def test_bad_json_raw_yaml_duplicates_and_redaction(self):
        for raw in ('on: push\njobs: {}', '{', '{"jobs":{},"jobs":{}}', '[]'):
            result = self.run_cli(raw, raw=True)
            self.assertEqual(result.returncode, 2)
            self.assertEqual(result.stdout, '')
        result = self.run_cli({'secret': 'SYNTHETIC-SENSITIVE-CONTENT'})
        self.assertEqual(result.returncode, 2)
        self.assertNotIn('SYNTHETIC-SENSITIVE-CONTENT', result.stderr)
        result = self.run_cli(GOOD, [{'id': 7}])
        self.assertEqual(result.returncode, 2)

    def test_help_no_io(self):
        result = subprocess.run([sys.executable, str(SCRIPT), '--help'], cwd=self.root, capture_output=True, text=True)
        self.assertEqual(result.returncode, 0)
        self.assertIn('Exit:', result.stdout)
        self.assertEqual(list(self.root.iterdir()), [])


if __name__ == '__main__':
    unittest.main(verbosity=2)
