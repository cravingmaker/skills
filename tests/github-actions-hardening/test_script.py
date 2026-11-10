"""Offline resolver tests. All refs, tags and API responses are synthetic."""
import contextlib
import copy
import importlib.util
import io
import json
import os
import subprocess
import sys
import tempfile
import unittest
import urllib.error
from pathlib import Path
from unittest.mock import patch

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
SCRIPT = HERE.parents[1] / 'skills/github-actions-hardening/scripts/resolve-action-refs.py'
spec = importlib.util.spec_from_file_location('owned_pin_resolver', SCRIPT)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
GOOD = json.loads((HERE / 'fixtures/workflow.json').read_text())
TAGS = json.loads((HERE / 'fixtures/tags.json').read_text())
API = json.loads((HERE / 'fixtures/api.json').read_text())


class PinTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix='pin-resolver-')
        self.root = Path(self.tmp.name)

    def tearDown(self):
        self.tmp.cleanup()

    def invoke(self, data=GOOD, tags=TAGS, api=API):
        workflow, tagfile = self.root / 'workflow.json', self.root / 'tags.json'
        workflow.write_text(json.dumps(data))
        tagfile.write_text(json.dumps(tags))
        before = {p.name: p.read_bytes() for p in self.root.iterdir()}
        out, err = io.StringIO(), io.StringIO()
        def fake(endpoint):
            if isinstance(api, Exception):
                raise api
            return copy.deepcopy(api[endpoint])
        with patch.object(module, 'fetch', side_effect=fake) as fetch, patch.object(sys, 'argv', [str(SCRIPT), str(workflow), '--tags', str(tagfile)]), contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            status = module.main()
        self.assertEqual(before, {p.name: p.read_bytes() for p in self.root.iterdir()}, 'resolver must not write')
        return status, out.getvalue(), err.getvalue(), fetch.call_args_list

    def test_direct_annotated_and_reusable_pass_repeat_no_writes(self):
        first = self.invoke()
        before = {p.name: p.read_bytes() for p in self.root.iterdir()}
        second = self.invoke()
        self.assertEqual(first[0], 0, first[2])
        self.assertEqual(json.loads(first[1])['references'], 4)
        self.assertEqual(len(json.loads(first[1])['resolved']), 2)
        self.assertEqual(first[1], second[1])
        self.assertEqual(before, {p.name: p.read_bytes() for p in self.root.iterdir()})
        self.assertTrue(all('/git/ref/tags/' in call.args[0] or '/git/tags/' in call.args[0] for call in first[3]))

    def test_mutable_and_reusable_tag_refs_rejected_without_api(self):
        for use in ('fixture/action@v1', 'fixture/workflows/.github/workflows/check.yml@main'):
            result = self.invoke({'jobs': {'x': {'uses': use}}}, {})
            self.assertEqual(result[0], 1)
            self.assertIn('full upstream commit', result[1])
            self.assertEqual(result[3], [])

    def test_wrong_upstream_tag_commit_rejected(self):
        api = copy.deepcopy(API)
        api['repos/fixture-owner/action/git/tags/' + 'b' * 40]['object']['sha'] = 'f' * 40
        result = self.invoke(api=api)
        self.assertEqual(result[0], 1)
        self.assertIn('mismatch', result[1])

    def test_missing_tag_evidence_and_bad_docker_digest(self):
        result = self.invoke(tags={})
        self.assertEqual(result[0], 1)
        self.assertIn('--tags', result[1])
        result = self.invoke({'runs': {'steps': [{'uses': 'docker://registry.example/tool:latest'}]}}, {})
        self.assertEqual(result[0], 1)
        self.assertEqual(result[3], [])

    def test_local_action_path_traversal_and_composite_documents(self):
        result = self.invoke({'runs': {'steps': [{'uses': './../other'}]}}, {})
        self.assertEqual(result[0], 1)
        self.assertIn('inside the checkout', result[1])
        result = self.invoke({'runs': {'steps': [{'uses': next(iter(TAGS))}]}}, TAGS)
        self.assertEqual(result[0], 0, result[2])

    def test_wrong_tag_endpoint_and_tag_cycle_rejected(self):
        api = copy.deepcopy(API)
        api['repos/fixture-owner/action/git/ref/tags/fixture-v1']['ref'] = 'refs/heads/fixture-v1'
        self.assertEqual(self.invoke(api=api)[0], 2)
        api = copy.deepcopy(API)
        api['repos/fixture-owner/action/git/tags/' + 'b' * 40]['object'] = {'type': 'tag', 'sha': 'b' * 40}
        self.assertEqual(self.invoke(api=api)[0], 2)

    def test_api_failures_do_not_expose_response_or_token(self):
        with patch.dict(os.environ, GH_TOKEN='SYNTHETIC-TOKEN'):
            result = self.invoke(api=urllib.error.URLError('SYNTHETIC-RESPONSE-BODY'))
        self.assertEqual(result[0], 2)
        self.assertEqual(result[1], '')
        self.assertNotIn('SYNTHETIC-', result[2])
        self.assertIn('GH_TOKEN', result[2])

    def test_network_adapter_uses_get_fixed_host_and_no_redirect(self):
        response = io.StringIO('{"ref":"fixture"}')
        with patch.dict(os.environ, GH_TOKEN='SYNTHETIC-TOKEN'), patch.object(module.urllib.request, 'build_opener') as build:
            build.return_value.open.return_value = response
            self.assertEqual(module.fetch('repos/fixture-owner/action/git/ref/tags/fixture-v1'), {'ref': 'fixture'})
            request = build.return_value.open.call_args.args[0]
            self.assertEqual(request.get_method(), 'GET')
            self.assertTrue(request.full_url.startswith('https://api.github.com/repos/'))
            self.assertIsInstance(build.call_args.args[0], module.NoRedirect)
        self.assertIsNone(module.NoRedirect().redirect_request(None, None, 302, '', {}, 'https://other.example'))

    def test_bad_document_and_help_no_io(self):
        self.assertEqual(self.invoke(data=[])[0], 2)
        for file in self.root.iterdir():
            file.unlink()
        result = subprocess.run([sys.executable, str(SCRIPT), '--help'], cwd=self.root, capture_output=True, text=True)
        self.assertEqual(result.returncode, 0)
        self.assertIn('Exit:', result.stdout)
        self.assertEqual(list(self.root.iterdir()), [])


if __name__ == '__main__':
    unittest.main(verbosity=2)
