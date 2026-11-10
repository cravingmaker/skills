"""Disposable Git fixtures contain only nonfunctional synthetic material."""
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "skills/secrets-management/scripts/find-long-lived-credentials.py"
MARKER = "SYNTHETIC_VALUE_MUST_NOT_APPEAR"


@unittest.skipUnless(shutil.which("git"), "install Git to run the offline tracked-file fixtures")
class PatternTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix="credential-pattern-test-")
        self.root = Path(self.tmp.name)
        self.env = dict(os.environ, GIT_CONFIG_NOSYSTEM="1", GIT_CONFIG_GLOBAL=os.devnull)
        self.git("init", "--quiet")

    def tearDown(self):
        self.tmp.cleanup()

    def git(self, *args):
        return subprocess.run(["git", "-C", str(self.root), *args], env=self.env, check=True, capture_output=True)

    def write(self, name, body):
        path = self.root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(body)
        self.git("add", "--", name)

    def snapshot(self):
        return {str(p.relative_to(self.root)): p.read_bytes() for p in self.root.rglob("*") if p.is_file() and not p.is_symlink()}

    def scan(self):
        before = self.snapshot()
        result = subprocess.run([sys.executable, str(SCRIPT), "--repo", str(self.root)], text=True, capture_output=True, env=self.env)
        self.assertEqual(self.snapshot(), before)
        self.assertNotIn(MARKER, result.stdout + result.stderr)
        return result

    def test_reject_and_repeat_without_payloads(self):
        self.write(".env", "DUMMY=" + MARKER + "\n")
        self.write(".github/workflows/deploy.yml", "env:\n  key: ${{ secrets.AWS_ACCESS_KEY_ID }}\n  secret: ${{ secrets['AWS_SECRET_ACCESS_KEY'] }}\n# " + MARKER + "\n")
        self.write("secret.yaml", "kind: Secret\nstringData:\n  dummy: " + MARKER + "\n")
        first, second = self.scan(), self.scan()
        self.assertEqual(first.returncode, 1, first.stderr)
        self.assertEqual(first.stdout, second.stdout)
        findings = json.loads(first.stdout)["findings"]
        self.assertEqual(len(findings), 4)
        self.assertEqual({f["line"] for f in findings if f["rule"] == "stored-cloud-key-reference"}, {2, 3})

    def test_accept_examples_oidc_and_encrypted_shape(self):
        self.write(".env.example", "DUMMY=" + MARKER + "\n")
        self.write(".github/workflows/deploy.yaml", "permissions:\n  id-token: write\n# secrets.AWS_ACCESS_KEY_ID\n")
        self.write("encrypted.yaml", "kind: Secret\ndata:\n  dummy: ENC[INERT]\nsops:\n  age: fixture-only\n")
        result = self.scan()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout)["findings"], [])
        # Acceptance covers shape only, not encryption or absence of example-file secrets.

    def test_encrypted_neighbor_does_not_exempt_plaintext(self):
        self.write("mixed.yaml", "kind: Secret\ndata:\n  dummy: ENC[INERT]\nsops:\n  age: fixture\n---\nkind: Secret\nstringData:\n  dummy: " + MARKER + "\n")
        result = self.scan()
        self.assertEqual(result.returncode, 1)
        self.assertEqual(json.loads(result.stdout)["findings"], [{"line": 7, "path": "mixed.yaml", "rule": "secret-document-without-encryption-evidence"}])

    def test_tracked_state_and_static_cloud_login_inputs(self):
        self.write("infra/terraform.tfstate", MARKER)
        self.write("infra/terraform.tfstate.backup", MARKER)
        self.write(".github/workflows/deploy.yaml", "with:\n  credentials_json: " + MARKER + "\n  aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}\n")
        self.write(".gitlab-ci.yml", "login:\n  creds: " + MARKER + "\n# credentials_json: inert-comment\n")
        result = self.scan()
        self.assertEqual(result.returncode, 1)
        found = sorted((f["path"], f["line"], f["rule"]) for f in json.loads(result.stdout)["findings"])
        self.assertEqual(found, [
            (".github/workflows/deploy.yaml", 2, "static-cloud-login-input-review"),
            (".github/workflows/deploy.yaml", 3, "stored-cloud-key-reference"),
            (".gitlab-ci.yml", 2, "static-cloud-login-input-review"),
            ("infra/terraform.tfstate", 1, "tracked-state-file"),
            ("infra/terraform.tfstate.backup", 1, "tracked-state-file")])

    def test_removed_violation_accepts_then_rejects_again(self):
        self.write(".env.local", "DUMMY=" + MARKER)
        self.assertEqual(self.scan().returncode, 1)
        self.git("rm", "--cached", "--quiet", "--", ".env.local")
        self.assertEqual(self.scan().returncode, 0)
        self.git("add", "--", ".env.local")
        self.assertEqual(self.scan().returncode, 1)

    def test_symlink_and_missing_tracked_file_are_not_silent_skips(self):
        self.write("target", MARKER)
        (self.root / "manifest.yaml").symlink_to("target")
        self.git("add", "--", "manifest.yaml")
        (self.root / "target").unlink()
        result = self.scan()
        self.assertEqual(result.returncode, 1)
        self.assertEqual({f["rule"] for f in json.loads(result.stdout)["findings"]}, {"symlink-not-scanned", "tracked-file-unavailable"})

    def test_bad_root_and_help(self):
        nested = self.root / "nested"
        nested.mkdir()
        result = subprocess.run([sys.executable, str(SCRIPT), "--repo", str(nested)], text=True, capture_output=True, env=self.env)
        self.assertEqual(result.returncode, 2)
        before = self.snapshot()
        result = subprocess.run([sys.executable, str(SCRIPT), "--help"], cwd=self.root, text=True, capture_output=True, env=self.env)
        self.assertEqual(result.returncode, 0)
        self.assertEqual(self.snapshot(), before)


if __name__ == "__main__":
    unittest.main(verbosity=2)
