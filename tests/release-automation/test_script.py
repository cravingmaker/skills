"""Offline candidate version adapters; no release tool or publication runs."""
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
SCRIPT = HERE.parents[1] / 'skills/release-automation/scripts/check-release-config.py'


class ReleaseTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix='release-candidate-')
        self.base = Path(self.tmp.name)
        self.root = self.base / 'candidate'
        shutil.copytree(HERE / 'fixtures/candidate', self.root)

    def tearDown(self):
        self.tmp.cleanup()

    def invoke(self, mode='release-please', state='manifest.json', extra=()):
        return subprocess.run([sys.executable, str(SCRIPT), '--root', str(self.root), '--mode', mode, '--state', state, *extra],
                              cwd=self.base, capture_output=True, text=True)

    def snapshot(self):
        return {str(p.relative_to(self.base)): p.read_bytes() for p in self.base.rglob('*') if p.is_file()}

    def test_node_cargo_python_pass_repeat_read_only(self):
        before = self.snapshot()
        first, second = self.invoke(), self.invoke()
        self.assertEqual(first.returncode, 0, first.stderr)
        self.assertEqual(json.loads(first.stdout)['packages'], 3)
        self.assertEqual(first.stdout, second.stdout)
        self.assertEqual(before, self.snapshot())

    def test_each_candidate_mismatch_fails_then_restored_passes(self):
        for name, version in (('node', '1.2.0'), ('rust', '0.4.0'), ('python', '2.3.0')):
            file = next((self.root / name).iterdir())
            original = file.read_text()
            file.write_text(original.replace(version, '9.9.9'))
            result = self.invoke()
            self.assertEqual(result.returncode, 1, result.stderr)
            self.assertIn('generated candidate', result.stdout)
            file.write_text(original)
            self.assertEqual(self.invoke().returncode, 0)

    def test_changesets_uses_new_not_old_version(self):
        args = ('--package', 'node/package.json')
        result = self.invoke('changesets', 'status.json', args)
        self.assertEqual(result.returncode, 0, result.stderr)
        package = self.root / 'node/package.json'
        package.write_text(package.read_text().replace('1.2.0', '1.1.0'))
        self.assertEqual(self.invoke('changesets', 'status.json', args).returncode, 1)

    def test_changesets_missing_package_and_no_release(self):
        self.assertEqual(self.invoke('changesets', 'status.json').returncode, 1)
        (self.root / 'status.json').write_text('{"releases":[]}')
        result = self.invoke('changesets', 'status.json')
        self.assertEqual(result.returncode, 0)
        self.assertEqual(json.loads(result.stdout)['packages'], 0)

    def test_dynamic_and_workspace_versions_need_native_adapter(self):
        (self.root / 'rust/Cargo.toml').write_text('[package]\nname="fixture"\nversion.workspace=true\n')
        self.assertEqual(self.invoke().returncode, 1)
        (self.root / 'python/pyproject.toml').write_text('[project]\nname="fixture"\ndynamic=["version"]\n')
        self.assertEqual(self.invoke().returncode, 1)

    def test_poetry_static_adapter(self):
        (self.root / 'python/pyproject.toml').write_text('[tool.poetry]\nname="fixture"\nversion="2.3.0"\n')
        self.assertEqual(self.invoke().returncode, 0)

    def test_multiple_manifest_ambiguity_is_finding(self):
        (self.root / 'node/Cargo.toml').write_text('[package]\nname="fixture"\nversion="1.2.0"\n')
        self.assertEqual(self.invoke().returncode, 1)

    def test_paths_cannot_escape_root_including_symlinks(self):
        outside = self.base / 'outside.json'
        outside.write_text('{"version":"SYNTHETIC-SENSITIVE-VALUE"}')
        self.assertEqual(self.invoke(state='../outside.json').returncode, 2)
        link = self.root / 'linked.json'
        link.symlink_to(outside)
        result = self.invoke(state='linked.json')
        self.assertEqual(result.returncode, 2)
        self.assertNotIn('SYNTHETIC-SENSITIVE-VALUE', result.stderr)
        package = self.root / 'node/package.json'
        package.unlink()
        package.symlink_to(outside)
        self.assertEqual(self.invoke().returncode, 2)

    def test_malformed_duplicate_state_and_duplicate_planned_package(self):
        for raw in ('{', '[]', '{"node":"1.2.0","node":"1.2.0"}'):
            (self.root / 'manifest.json').write_text(raw)
            result = self.invoke()
            self.assertEqual(result.returncode, 2)
            self.assertEqual(result.stdout, '')
        status = json.loads((self.root / 'status.json').read_text())
        status['releases'] *= 2
        (self.root / 'status.json').write_text(json.dumps(status))
        self.assertEqual(self.invoke('changesets', 'status.json').returncode, 2)

    def test_configured_package_membership(self):
        path = self.root / 'release-please-config.json'
        config = {'packages': {'node': {}, 'rust': {}, 'python': {}}}
        path.write_text(json.dumps(config))
        args = ('--config', path.name)
        self.assertEqual(self.invoke(extra=args).returncode, 0)
        config['packages']['missing'] = {}
        path.write_text(json.dumps(config))
        result = self.invoke(extra=args)
        self.assertEqual(result.returncode, 1)
        self.assertIn('configured candidate', result.stdout)
        config['packages'] = {'../outside': {}}
        path.write_text(json.dumps(config))
        self.assertEqual(self.invoke(extra=args).returncode, 2)
        self.assertEqual(self.invoke('changesets', 'status.json', args).returncode, 2)

    def test_help_no_io(self):
        before = self.snapshot()
        result = subprocess.run([sys.executable, str(SCRIPT), '--help'], cwd=self.base, capture_output=True, text=True)
        self.assertEqual(result.returncode, 0)
        self.assertIn('Exit:', result.stdout)
        self.assertEqual(before, self.snapshot())


if __name__ == '__main__':
    unittest.main(verbosity=2)
