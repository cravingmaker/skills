"""Offline structural and saved-observation cases; never a database rehearsal."""
import copy
from datetime import date
import json
import hashlib
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

HERE = Path(__file__).resolve().parent
CHECK = HERE.parents[1] / "skills/runbook-authoring/scripts/check-runbook.py"


class Runbook(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="fixtures-", dir=HERE)
        self.work = Path(self.temp.name)
        self.value = json.loads((HERE / "fixtures/postgres-runbook.json").read_text())
        self.value["last_rehearsed"] = date.today().isoformat()
        (self.work / "synthetic-receipt.txt").write_text("Synthetic checker fixture; not a real operator rehearsal.\n")

    def tearDown(self):
        self.temp.cleanup()

    def call(self, *args):
        return subprocess.run([sys.executable, str(CHECK), *map(str, args)],
                              capture_output=True, text=True, cwd=self.work, timeout=5)

    def check(self, value=None, raw=None, restamp=True):
        path = self.work / "runbook.json"
        path.write_text(raw if raw is not None else json.dumps(self.value if value is None else value))
        if raw is None and restamp:
            value = self.value if value is None else value
            record = {"procedure_sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
                      "rehearsed_on": value["last_rehearsed"], "target": value["target"],
                      "operator": "Synthetic fixture only, no rehearsal occurred",
                      "steps": [{"id": s["id"], "observed": "Synthetic observation", "matched": True} for s in value["steps"]],
                      "not_rehearsed": []}
            (self.work / "synthetic-receipt.txt").write_text(json.dumps(record))
        return self.call(path)

    def findings(self, result):
        self.assertEqual(result.returncode, 1, result.stderr + result.stdout)
        return json.loads(result.stdout)["findings"]

    def test_help_no_read_or_write(self):
        before = list(self.work.iterdir())
        result = self.call("--help")
        self.assertEqual(result.returncode, 0)
        self.assertIn("Exit:", result.stdout)
        self.assertEqual(list(self.work.iterdir()), before)

    def test_accept_repeat_no_execution_or_source_leak(self):
        self.value["steps"][0]["command"] = "printf SYNTHETIC_CREDENTIAL; touch must-not-exist"
        first = self.check()
        source = (self.work / "runbook.json").read_bytes()
        second = self.call(self.work / "runbook.json")
        self.assertEqual(first.returncode, 0, first.stderr)
        self.assertEqual(first.stdout, second.stdout)
        self.assertEqual(source, (self.work / "runbook.json").read_bytes())
        self.assertFalse((self.work / "must-not-exist").exists())
        self.assertNotIn("SYNTHETIC_CREDENTIAL", first.stdout + first.stderr)

    def test_dangling_cycle_and_unreachable_are_rejected(self):
        for mutation, code in (
            (lambda v: v["steps"][0].update(on_expected="missing"), "dangling_branch"),
            (lambda v: v["steps"][0].update(on_expected="observe"), "cycle_without_bound"),
            (lambda v: v["steps"][0].update(on_expected="verify"), "unreachable_step"),
        ):
            value = copy.deepcopy(self.value)
            mutation(value)
            self.assertIn(code, self.findings(self.check(value)))

    def test_owner_rehearsal_authority_and_budget_are_required(self):
        for mutate, code in (
            (lambda v: v.update(owner=""), "missing_text:owner"),
            (lambda v: v.update(last_rehearsed=None), "missing_successful_rehearsal_date"),
            (lambda v: v.update(rehearsal_receipt="absent"), "missing_local_rehearsal_receipt"),
            (lambda v: v["steps"][5].update(authority="read-only"), "missing_mitigation_authority:5"),
            (lambda v: v["steps"][5].pop("undo"), "missing_mitigation_undo:5"),
            (lambda v: v["steps"][0].update(timeout_seconds=True), "unbounded_step:0"),
        ):
            value = copy.deepcopy(self.value)
            mutate(value)
            self.assertIn(code, self.findings(self.check(value)))

    def test_recovery_needs_verification(self):
        self.value["steps"][0]["on_expected"] = "recovered"
        self.assertIn("recovery_without_verification:0", self.findings(self.check()))

    def test_literal_comparison_and_input_redirection_are_valid_text(self):
        self.value["steps"][0]["command"] = "read_fixture < observations.txt"
        self.value["steps"][0]["expected"] = "queued requests < the agreed budget"
        self.assertEqual(self.check().returncode, 0)

    def test_invalid_url_and_escaping_receipt(self):
        self.value["runbook_url"] = "https://user:synthetic-secret@example.invalid/runbook"
        self.value["rehearsal_receipt"] = "../test_helper.py"
        codes = self.findings(self.check())
        self.assertIn("invalid_runbook_url", codes)
        self.assertIn("missing_local_rehearsal_receipt", codes)
        self.assertNotIn("synthetic-secret", self.check().stdout + self.check().stderr)

    def test_unknown_duplicate_malformed_and_nonfinite_inputs(self):
        for raw in ("{", '{"title":"SYNTHETIC_CREDENTIAL","title":1}', '{"steps":NaN}'):
            result = self.check(raw=raw)
            self.assertEqual(result.returncode, 2)
            self.assertEqual(result.stdout, "")
            self.assertNotIn("SYNTHETIC_CREDENTIAL", result.stderr)
        self.value["typo"] = "value"
        self.assertEqual(self.check().returncode, 2)
        self.assertEqual(self.call(self.work / "absent").returncode, 2)

    def test_postgres_competing_cause_observation_replay(self):
        self.assertEqual(self.check().returncode, 0)
        steps = {step["id"]: step for step in self.value["steps"]}
        cases = json.loads((HERE / "fixtures/postgres-cases.json").read_text())
        # These saved predicates are independent expected observations. No SQL,
        # cluster or arbitrary runbook command is executed by this replay.
        for case in cases:
            observed, visited, node = case["observations"], [], "observe"
            for _ in range(len(steps) + 1):
                if node in {"recovered", "abort", "escalate"}:
                    break
                visited.append(node)
                matches = {
                    "observe": observed["collector_visible"] and observed["archiver"]["reset_epoch"] == "same",
                    "provider": observed["database_reachable"],
                    "locks": any(row["blocked_by"] for row in observed["activity"]),
                    "capacity": observed["connections"]["used"] >= observed["connections"]["usable_limit"],
                    "pool": observed["pool"]["queued"] > 0 and observed["pool"]["active"] >= observed["pool"]["limit"],
                    "archive": observed["archiver"]["after"]["failed_count"] > observed["archiver"]["before"]["failed_count"] and observed["archiver"]["after"]["archived_count"] == observed["archiver"]["before"]["archived_count"],
                    "slots": any(row["retained_bytes"] > row["capacity_budget_bytes"] and not row["progressed"] for row in observed["slots"]),
                    "lock_change": observed["mitigation_succeeds"],
                    "capacity_change": observed["mitigation_succeeds"],
                    "pool_change": observed["mitigation_succeeds"],
                    "archive_change": observed["mitigation_succeeds"],
                    "slot_change": observed["mitigation_succeeds"],
                    "verify": observed["user_path_recovers"],
                }[node]
                node = steps[node]["on_expected" if matches else "otherwise"]
            self.assertEqual(node, case["terminal"], case["name"])
            self.assertEqual(visited, case["expected_steps"], case["name"])

    def test_receipt_binds_current_procedure_and_reports_incomplete_rehearsal(self):
        self.assertEqual(self.check().returncode, 0)
        self.value["steps"][0]["command"] = "Changed after rehearsal"
        self.assertIn("receipt_stale", self.findings(self.check(restamp=False)))
        self.check()
        receipt_path = self.work / "synthetic-receipt.txt"
        record = json.loads(receipt_path.read_text())
        record["not_rehearsed"] = [{"id": record["steps"][0]["id"], "reason": "Never executed"}]
        record["steps"].pop(0)
        receipt_path.write_text(json.dumps(record))
        codes = self.findings(self.check(restamp=False))
        self.assertIn("unrehearsed_steps", codes)
        self.assertIn("receipt_step_coverage", codes)
        receipt_path.write_text('[]')
        self.assertIn("invalid_rehearsal_receipt", self.findings(self.check(restamp=False)))


if __name__ == "__main__":
    unittest.main()
