"""Independent arithmetic oracles plus generated native-rule counterexamples."""
import copy
from decimal import Decimal
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
SCRIPT = ROOT / 'skills/slo-error-budgets/scripts/burn-rate.py'
BASE = json.loads((HERE / 'fixtures/contract.json').read_text())
PROMTOOL = shutil.which(os.environ.get('PROMTOOL', 'promtool'))


class CalculatorTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix='slo-burn-')
        self.addCleanup(self.temporary.cleanup)
        self.target = Path(self.temporary.name)
        self.contract = self.target / 'contract.json'
        self.contract.write_text(json.dumps(BASE))

    def run_script(self, spec=None, *args):
        if spec is not None:
            self.contract.write_text(json.dumps(spec))
        return subprocess.run([sys.executable, str(SCRIPT), str(self.contract), *args], cwd=self.target, capture_output=True, text=True, timeout=15)

    def test_hand_derived_thresholds_and_repeat(self):
        result = self.run_script()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stderr, '')
        data = json.loads(result.stdout)
        self.assertEqual(data['allowed_bad_fraction'], '0.001')
        self.assertEqual([p['burn_threshold'] for p in data['policies']], ['14.4', '6', '1'])
        self.assertEqual([p['bad_fraction_threshold'] for p in data['policies']], ['0.0144', '0.006', '0.001'])
        self.assertEqual(self.run_script().stdout, result.stdout)

    def test_policy_is_input_not_a_fixed_starting_table(self):
        spec = copy.deepcopy(BASE)
        spec['target'] = '0.99'
        spec['objective_window_seconds'] = 10000
        spec['policies'] = [dict(spec['policies'][0], long_seconds=1000, short_seconds=100, budget_fraction='0.2')]
        result = self.run_script(spec)
        self.assertEqual(result.returncode, 0, result.stderr)
        policy = json.loads(result.stdout)['policies'][0]
        self.assertEqual((policy['burn_threshold'], policy['bad_fraction_threshold']), ('2', '0.02'))

    def test_sparse_and_zero_traffic_findings_refuse_generation(self):
        spec = copy.deepcopy(BASE)
        spec['policies'][0]['short_min_events'] = 1
        result = self.run_script(spec)
        self.assertEqual(result.returncode, 1)
        self.assertTrue(json.loads(result.stdout)['policies'][0]['traffic']['short']['single_event_can_cross'])
        refused = self.run_script(spec, '--emit', 'rules')
        self.assertEqual((refused.returncode, refused.stdout), (1, ''))
        spec['policies'][0]['short_min_events'] = 0
        result = self.run_script(spec)
        self.assertEqual(result.returncode, 1)
        self.assertIsNone(json.loads(result.stdout)['policies'][0]['traffic']['short']['single_bad_fraction'])

    def test_unattainable_threshold(self):
        spec = copy.deepcopy(BASE)
        spec['target'] = '0.5'
        result = self.run_script(spec)
        self.assertEqual(result.returncode, 1)
        self.assertTrue(json.loads(result.stdout)['findings'])

    def test_malformed_contracts_do_not_echo_input(self):
        marker = 'SENSITIVE_FIXTURE_VALUE'
        for field, value in (('target', marker), ('target', 'NaN'), ('target', 'Infinity'), ('target', True), ('target', '1'), ('objective_window_seconds', 0), ('policies', []), ('policies', [None])):
            with self.subTest(field=field, value=value):
                spec = copy.deepcopy(BASE)
                spec[field] = value
                result = self.run_script(spec)
                self.assertEqual((result.returncode, result.stdout), (2, ''))
                self.assertNotIn(marker, result.stderr)
        for field, value in (('short_seconds', 0), ('short_seconds', 3600), ('long_seconds', 2592001), ('budget_fraction', '0'), ('short_min_events', -1), ('short_min_events', '1.5')):
            with self.subTest(field=field, value=value):
                spec = copy.deepcopy(BASE)
                spec['policies'][0][field] = value
                result = self.run_script(spec)
                self.assertEqual((result.returncode, result.stdout), (2, ''))

    def test_duplicate_keys_bad_json_and_missing_file(self):
        for content in ('{"schema_version":"1","schema_version":"1"}', '{', '{"target":NaN}'):
            self.contract.write_text(content)
            result = self.run_script()
            self.assertEqual((result.returncode, result.stdout), (2, ''))
        self.contract.unlink()
        result = self.run_script()
        self.assertEqual((result.returncode, result.stdout), (2, ''))

    def test_help_is_effect_free_even_without_a_contract(self):
        self.contract.unlink()
        before = list(self.target.iterdir())
        result = subprocess.run([sys.executable, str(SCRIPT), '--help'], cwd=self.target, capture_output=True, text=True, timeout=15)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn('Exits:', result.stdout)
        self.assertEqual(list(self.target.iterdir()), before)

    def test_generator_refuses_unsafe_or_unsupported_fields(self):
        for field, value in (('service', 'x"} or vector(1)'), ('owner', 'unbounded owner'), ('runbook_url', 'https://user:password@example.invalid'), ('runbook_url', 'not a url')):
            with self.subTest(field=field):
                spec = copy.deepcopy(BASE)
                spec[field] = value
                result = self.run_script(spec, '--emit', 'rules')
                self.assertEqual((result.returncode, result.stdout), (2, ''))
        spec = copy.deepcopy(BASE)
        spec['sli']['bad_counter'] = spec['sli']['eligible_counter']
        result = self.run_script(spec, '--emit', 'rules')
        self.assertEqual((result.returncode, result.stdout), (2, ''))

    @unittest.skipUnless(PROMTOOL, 'install project-pinned promtool or set PROMTOOL; generated-rule execution unavailable')
    def test_generated_rules_and_confirmation_mutation(self):
        result = self.run_script(None, '--emit', 'rules')
        self.assertEqual(result.returncode, 0, result.stderr)
        rules = self.target / 'generated-rules.json'
        rules.write_text(result.stdout)
        shutil.copyfile(HERE / 'fixtures/rule-tests.json', self.target / 'rule-tests.json')
        def native(*args):
            return subprocess.run([PROMTOOL, *args], cwd=self.target, capture_output=True, text=True, timeout=40)
        def passes(result):
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        passes(native('check', 'rules', 'generated-rules.json'))
        passes(native('test', 'rules', 'rule-tests.json'))
        changed = json.loads(result.stdout)
        for rule in changed['groups'][0]['rules']:
            if rule.get('alert') == 'SloBurn_fast':
                rule['expr'] = rule['expr'].replace(' and on (service) (slo:bad_ratio:', ' or on (service) (slo:bad_ratio:', 1)
        rules.write_text(json.dumps(changed))
        passes(native('check', 'rules', 'generated-rules.json'))
        broken = native('test', 'rules', 'rule-tests.json')
        self.assertNotEqual(broken.returncode, 0, broken.stdout + broken.stderr)
        self.assertIn('long-only-burn', broken.stdout + broken.stderr)
        rules.write_text(result.stdout)
        passes(native('test', 'rules', 'rule-tests.json'))


if __name__ == '__main__':
    unittest.main(verbosity=2)
