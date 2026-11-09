"""Offline rejection fixtures; no database or privileged runner."""
import copy
import hashlib
import json
import subprocess
import sys
import tempfile
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SKILL = ROOT / "skills/postgres-change-execution"
SCRIPT = SKILL / "scripts/check-change.py"


class ChangeTests(unittest.TestCase):
    def setUp(self):
        self.work = tempfile.TemporaryDirectory(prefix="change-preflight-test-")
        self.addCleanup(self.work.cleanup)
        self.root = Path(self.work.name)
        self.sql = self.root / "candidate.sql"
        self.sql.write_bytes(b"-- inert candidate fixture\nSELECT 1;\n")
        self.plan = json.loads((SKILL / "assets/change-plan.json").read_text())
        self.plan["candidate_sha256"] = hashlib.sha256(self.sql.read_bytes()).hexdigest()
        self.plan["recovery"]["usable"] = True
        self.observed = {k: copy.deepcopy(self.plan[k]) for k in
                         ("target", "candidate_sha256", "preconditions", "selected_keys_sha256")}
        self.observed.update(row_count=1, observed_at=datetime.now(timezone.utc).isoformat())

    def run_check(self, plan=None, observed=None):
        p, o = self.root / "plan.json", self.root / "observed.json"
        p.write_text(json.dumps(self.plan if plan is None else plan))
        o.write_text(json.dumps(self.observed if observed is None else observed))
        return subprocess.run([sys.executable, str(SCRIPT), str(p), str(o), str(self.sql)],
                              capture_output=True, text=True)

    def test_accept_repeat_and_read_only(self):
        first = self.run_check()
        before = {p.name: p.read_bytes() for p in self.root.iterdir()}
        second = self.run_check()
        self.assertEqual(first.returncode, 0, first.stderr)
        self.assertEqual(second.stdout, first.stdout)
        self.assertEqual(json.loads(first.stdout)["next"], "native_recheck")
        self.assertEqual({p.name: p.read_bytes() for p in self.root.iterdir()}, before)

    def test_wrong_target_principal_state_count_keys_and_age(self):
        mutations = [
            lambda o: o["target"].update(endpoint_id="wrong"),
            lambda o: o["target"].update(principal="wrong"),
            lambda o: o["preconditions"].update(status="changed"),
            lambda o: o.update(row_count=2),
            lambda o: o.update(row_count=True),
            lambda o: o.update(selected_keys_sha256="a" * 64),
            lambda o: o.update(observed_at=(datetime.now(timezone.utc) - timedelta(days=1)).isoformat()),
            lambda o: o.update(observed_at=(datetime.now(timezone.utc) + timedelta(days=1)).isoformat()),
            lambda o: o.update(observed_at="2000-01-01T00:00:00"),
        ]
        for mutate in mutations:
            with self.subTest(mutation=mutate):
                observed = copy.deepcopy(self.observed)
                mutate(observed)
                result = self.run_check(observed=observed)
                self.assertEqual(result.returncode, 1, result.stderr + result.stdout)
                self.assertEqual(json.loads(result.stdout)["next"], "stop")

    def test_changed_candidate_is_rejected(self):
        self.sql.write_bytes(self.sql.read_bytes() + b"\n")
        self.assertEqual(self.run_check().returncode, 1)

    def test_precondition_types_are_not_coerced(self):
        self.plan["preconditions"]["enabled"] = True
        self.observed["preconditions"]["enabled"] = 1
        self.assertEqual(self.run_check().returncode, 1)

    def test_authority_recovery_timeouts_and_side_effects(self):
        mutations = [
            lambda p: p.update(authority_ref=""),
            lambda p: p.update(lock_timeout_ms=0),
            lambda p: p.update(max_observation_age_seconds=float("inf")),
            lambda p: p["recovery"].update(usable=False),
            lambda p: p["recovery"]["target"].update(endpoint_id="wrong"),
            lambda p: p.update(rehearsal={"disposable": False, "receipt_ref": "fixture"}),
            lambda p: p.update(effects=[]),
        ]
        for mutate in mutations:
            with self.subTest(mutation=mutate):
                plan = copy.deepcopy(self.plan)
                mutate(plan)
                self.assertEqual(self.run_check(plan=plan).returncode, 1)
        for effect in ("nontransactional", "sequence", "trigger", "external"):
            plan = copy.deepcopy(self.plan)
            plan.update(effects=[effect], rehearsal={})
            self.assertEqual(self.run_check(plan=plan).returncode, 1)

    def test_duplicate_json_member(self):
        p, o = self.root / "plan.json", self.root / "observed.json"
        self.run_check()
        p.write_text('{"target": {}, "target": {}}')
        result = subprocess.run([sys.executable, str(SCRIPT), str(p), str(o), str(self.sql)], capture_output=True, text=True)
        self.assertEqual(result.returncode, 2)
        self.assertNotIn("Traceback", result.stderr)

    def test_bad_shapes_help_and_secret_free_diagnostics(self):
        result = self.run_check(plan=[])
        self.assertEqual(result.returncode, 1)
        self.assertNotIn("Traceback", result.stderr)
        self.observed["target"]["principal"] = "DO_NOT_ECHO"
        result = self.run_check()
        self.assertNotIn("DO_NOT_ECHO", result.stdout + result.stderr)
        result = subprocess.run([sys.executable, str(SCRIPT), "--help"], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0)
        result = subprocess.run([sys.executable, str(SCRIPT), "--unknown", "postgres://DO_NOT_ECHO"], capture_output=True, text=True)
        self.assertEqual(result.returncode, 2)
        self.assertNotIn("DO_NOT_ECHO", result.stdout + result.stderr)
        bad = self.root / "bad.json"
        bad.write_text('{"DO_NOT_ECHO":')
        result = subprocess.run([sys.executable, str(SCRIPT), str(bad), str(bad), str(self.sql)],
                                capture_output=True, text=True)
        self.assertEqual(result.returncode, 2)
        self.assertNotIn("DO_NOT_ECHO", result.stderr + result.stdout)


if __name__ == "__main__":
    unittest.main()
