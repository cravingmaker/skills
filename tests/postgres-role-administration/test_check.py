"""Offline matrix-closure fixtures; database evidence must be collected natively."""
import copy
import hashlib
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SKILL = ROOT / "skills/postgres-role-administration"
SCRIPT = SKILL / "scripts/check-privileges.py"


class AccessTests(unittest.TestCase):
    def setUp(self):
        self.work = tempfile.TemporaryDirectory(prefix="access-matrix-test-")
        self.addCleanup(self.work.cleanup)
        self.root = Path(self.work.name)
        self.policy = json.loads((SKILL / "assets/policy-example.json").read_text())
        for item in list(self.policy["checks"]):
            future = copy.deepcopy(item)
            future.update(id=item["id"] + "-future", phase="future-table")
            self.policy["checks"].append(future)
        self.policy_path = self.root / "policy.json"
        self.policy_path.write_text(json.dumps(self.policy))
        self.results = {"target_id": self.policy["target_id"],
                        "policy_sha256": hashlib.sha256(self.policy_path.read_bytes()).hexdigest(), "checks": []}
        for check in self.policy["checks"]:
            result = {k: check[k] for k in ("id", "login", "session_role", "phase", "kind", "probe_sha256")}
            result.update(result=check["expected"], code=check["codes"][0], fresh_attempt=True,
                          adapter="actual-client", authenticated_login=check["login"],
                          reachable_roles=["fixture_reader"],
                          role_flags={k: False for k in ("superuser", "bypassrls", "createrole", "createdb")})
            self.results["checks"].append(result)

    def run_check(self, results=None):
        result_path = self.root / "results.json"
        result_path.write_text(json.dumps(self.results if results is None else results))
        return subprocess.run([sys.executable, str(SCRIPT), str(self.policy_path), str(result_path)],
                              capture_output=True, text=True)

    def test_accept_repeat_and_read_only(self):
        first = self.run_check()
        before = {p.name: p.read_bytes() for p in self.root.iterdir()}
        second = self.run_check()
        self.assertEqual(first.returncode, 0, first.stderr)
        self.assertEqual(first.stdout, second.stdout)
        self.assertEqual({p.name: p.read_bytes() for p in self.root.iterdir()}, before)

    def test_missing_duplicate_extra_and_wrong_binding(self):
        mutations = [
            lambda r: r["checks"].pop(),
            lambda r: r["checks"].append(copy.deepcopy(r["checks"][0])),
            lambda r: r["checks"].append({"id": "extra"}),
            lambda r: r.update(target_id="wrong"),
            lambda r: r.update(policy_sha256="f" * 64),
            lambda r: r["checks"][0].update(login="wrong"),
            lambda r: r["checks"][0].update(session_role="fixture_owner"),
            lambda r: r["checks"][0].update(phase="wrong"),
            lambda r: r["checks"][0].update(probe_sha256="f" * 64),
            lambda r: r["checks"][0].update(authenticated_login="fixture_owner"),
        ]
        for mutate in mutations:
            with self.subTest(mutation=mutate):
                results = copy.deepcopy(self.results)
                mutate(results)
                result = self.run_check(results)
                self.assertEqual(result.returncode, 1, result.stderr + result.stdout)

    def test_false_denials_and_escalation(self):
        mutations = [
            lambda r: r["checks"][1].update(code="42601"),
            lambda r: r["checks"][0].update(adapter="administrator-set-role"),
            lambda r: r["checks"][0].update(fresh_attempt=False),
            lambda r: r["checks"][0].update(reachable_roles=["fixture_owner"]),
            lambda r: r["checks"][0].update(reachable_roles=["neon_superuser"]),
        ]
        for flag in ("superuser", "bypassrls", "createrole", "createdb"):
            results = copy.deepcopy(self.results)
            results["checks"][0]["role_flags"][flag] = True
            self.assertEqual(self.run_check(results).returncode, 1)
        for mutate in mutations:
            results = copy.deepcopy(self.results)
            mutate(results)
            self.assertEqual(self.run_check(results).returncode, 1)

    def test_edited_policy_and_connection_rejection(self):
        self.policy_path.write_bytes(self.policy_path.read_bytes() + b"\n")
        self.assertEqual(self.run_check().returncode, 1)
        # Same checker handles a classified fresh auth failure without SQL role fields.
        check = {"id": "old-credential", "login": "retired", "phase": "rotation", "kind": "connection",
                 "probe_sha256": "a" * 64, "expected": "deny", "codes": ["28P01"]}
        self.policy["checks"] = [check]
        self.policy_path.write_text(json.dumps(self.policy))
        results = {"target_id": self.policy["target_id"], "policy_sha256": hashlib.sha256(self.policy_path.read_bytes()).hexdigest(),
                   "checks": [{**check, "result": "deny", "code": "28P01", "fresh_attempt": True, "adapter": "actual-client"}]}
        self.assertEqual(self.run_check(results).returncode, 0)

    def test_duplicate_json_member(self):
        self.policy_path.write_text('{"target_id": "fixture", "target_id": "fixture"}')
        self.assertEqual(self.run_check().returncode, 2)

    def test_bad_shape_help_and_secret_free_diagnostics(self):
        result = self.run_check([])
        self.assertEqual(result.returncode, 1)
        self.assertNotIn("Traceback", result.stderr)
        self.results["checks"][0]["login"] = "DO_NOT_ECHO"
        result = self.run_check()
        self.assertNotIn("DO_NOT_ECHO", result.stdout + result.stderr)
        result = subprocess.run([sys.executable, str(SCRIPT), "--help"], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0)
        result = subprocess.run([sys.executable, str(SCRIPT), "--unknown", "postgres://DO_NOT_ECHO"], capture_output=True, text=True)
        self.assertEqual(result.returncode, 2)
        self.assertNotIn("DO_NOT_ECHO", result.stdout + result.stderr)
        self.policy_path.write_text('{"DO_NOT_ECHO":')
        result = self.run_check()
        self.assertEqual(result.returncode, 2)
        self.assertNotIn("DO_NOT_ECHO", result.stdout + result.stderr)


if __name__ == "__main__":
    unittest.main()
