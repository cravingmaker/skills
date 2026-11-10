"""Offline SBOM package projections; no cryptographic claim is tested here."""
import copy
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
SCRIPT = HERE.parents[1] / 'skills/software-supply-chain-provenance/scripts/check-sbom-components.py'
CDX = json.loads((HERE / 'fixtures/cyclonedx.json').read_text())
SPDX = json.loads((HERE / 'fixtures/spdx.json').read_text())
EXPECTED = json.loads((HERE / 'fixtures/expected.json').read_text())


class SbomTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix='sbom-inventory-')
        self.root = Path(self.tmp.name)

    def tearDown(self):
        self.tmp.cleanup()

    def invoke(self, document=CDX, expected=EXPECTED, raw=False):
        (self.root / 'bom.json').write_text(document if raw else json.dumps(document))
        (self.root / 'expected.json').write_text(json.dumps(expected))
        before = {p.name: p.read_bytes() for p in self.root.iterdir()}
        result = subprocess.run([sys.executable, str(SCRIPT), 'bom.json', '--expected', 'expected.json'],
                              cwd=self.root, capture_output=True, text=True)
        self.assertEqual(before, {p.name: p.read_bytes() for p in self.root.iterdir()}, 'checker must not write')
        return result

    def test_both_formats_pass_repeat_and_read_only(self):
        for document in (CDX, SPDX):
            first = self.invoke(document)
            before = {p.name: p.read_bytes() for p in self.root.iterdir()}
            second = self.invoke(document)
            self.assertEqual(first.returncode, 0, first.stderr)
            self.assertEqual(json.loads(first.stdout)['expected'], 2)
            self.assertEqual(first.stdout, second.stdout)
            self.assertEqual(before, {p.name: p.read_bytes() for p in self.root.iterdir()})

    def test_missing_component_in_both_formats_fails(self):
        for document, key in ((CDX, 'components'), (SPDX, 'packages')):
            data = copy.deepcopy(document)
            data[key].pop()
            result = self.invoke(data)
            self.assertEqual(result.returncode, 1, result.stderr)
            self.assertIn('independently observed', result.stdout)
            self.assertEqual(json.loads(result.stdout)['observed_purls'], 1)

    def test_wrong_namespace_and_wrong_version_fail(self):
        for field, value in (('purl', 'pkg:npm/other-library@1.2.0'), ('version', '1.3.0')):
            data = copy.deepcopy(CDX)
            data['components'][0][field] = value
            self.assertEqual(self.invoke(data).returncode, 1)

    def test_missing_and_conflicting_versions_fail(self):
        data = copy.deepcopy(CDX)
        del data['components'][0]['version']
        self.assertEqual(self.invoke(data).returncode, 1)
        data = copy.deepcopy(CDX)
        conflict = dict(data['components'][0], version='9.9.9')
        data['components'].append(conflict)
        result = self.invoke(data)
        self.assertEqual(result.returncode, 1)
        self.assertIn('conflicting', result.stdout)

    def test_nested_components_and_root_metadata(self):
        data = copy.deepcopy(CDX)
        data['metadata'] = {'component': data['components'].pop()}
        data['components'] = [{'type': 'application', 'name': 'fixture-root', 'components': data['components']}]
        self.assertEqual(self.invoke(data).returncode, 0)

    def test_extra_components_and_identical_context_duplicates_allowed(self):
        data = copy.deepcopy(CDX)
        data['components'].append(copy.deepcopy(data['components'][0]))
        data['components'].append({'purl': 'pkg:generic/extra@1', 'version': '1'})
        self.assertEqual(self.invoke(data).returncode, 0)

    def test_malformed_unsupported_and_duplicate_input_redacted(self):
        for raw in ('{', '[]', '{"bomFormat":"CycloneDX","bomFormat":"CycloneDX"}', '{"secret":"SYNTHETIC-PRIVATE-VALUE"}'):
            result = self.invoke(raw, raw=True)
            self.assertEqual(result.returncode, 2)
            self.assertEqual(result.stdout, '')
            self.assertNotIn('SYNTHETIC-PRIVATE-VALUE', result.stderr)
        self.assertEqual(self.invoke(expected=[]).returncode, 2)
        self.assertEqual(self.invoke(expected=EXPECTED + EXPECTED).returncode, 2)

    def test_help_no_io_and_truthful_limit(self):
        result = subprocess.run([sys.executable, str(SCRIPT), '--help'], cwd=self.root, capture_output=True, text=True)
        self.assertEqual(result.returncode, 0)
        self.assertIn('NOT', result.stdout)
        self.assertIn('signature verifier', result.stdout)
        self.assertEqual(list(self.root.iterdir()), [])


if __name__ == '__main__':
    unittest.main(verbosity=2)
