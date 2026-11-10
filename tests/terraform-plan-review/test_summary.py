"""Offline, inert plan exports; no engine or cloud is invoked."""
from copy import deepcopy
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "skills/terraform-plan-review/scripts/plan-summary.py"
MARKER = "SYNTHETIC_PAYLOAD_MUST_NOT_APPEAR"


def plan(actions=None, kind="aws_lambda_function"):
    return {"format_version": "1.2", "planned_values": {}, "resource_changes": [
        {"address": 'aws_lambda_function.test["' + MARKER + '"]', "type": kind, "mode": "managed",
         "change": {"actions": actions or ["update"], "before": {"value": MARKER},
                    "after": {"value": MARKER}, "after_unknown": {"arn": True}}}]}


class SummaryTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix="plan-summary-test-")
        self.path = Path(self.tmp.name)
        self.input = self.path / "plan.json"
        self.binary = self.path / "saved.plan"
        self.binary.write_bytes(b"INERT BINARY FIXTURE")

    def tearDown(self):
        self.tmp.cleanup()

    def run_plan(self, document, *extra):
        self.input.write_text(json.dumps(document))
        before = self.input.read_bytes()
        result = subprocess.run([sys.executable, str(SCRIPT), str(self.input), *extra], text=True, capture_output=True)
        self.assertEqual(self.input.read_bytes(), before)
        self.assertNotIn(MARKER, result.stdout + result.stderr)
        return result

    def test_accept_repeat_hash_and_redaction(self):
        runs = [self.run_plan(plan(), "--saved-plan", str(self.binary), "--detailed-exit-code", "2") for _ in range(2)]
        for result in runs:
            self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(runs[0].stdout, runs[1].stdout)
        output = json.loads(runs[0].stdout)
        self.assertEqual(output["action_counts"], {"update": 1})
        self.assertEqual(output["saved_plan_sha256"], hashlib.sha256(self.binary.read_bytes()).hexdigest())
        self.assertIn("<redacted>", output["resources"][0]["address"])
        self.assertIn("unknown-values-review", output["resources"][0]["flags"])

    def test_stateful_delete_and_both_replacement_orders(self):
        for actions in (["delete"], ["create", "delete"], ["delete", "create"]):
            document = plan(actions, "aws_db_instance")
            document["resource_changes"][0]["change"]["replace_paths"] = [["storage", MARKER]]
            result = self.run_plan(document)
            self.assertEqual(result.returncode, 1, result.stderr)
            row = json.loads(result.stdout)["resources"][0]
            self.assertEqual(row["forcing_root_attributes"], ["storage"])
            self.assertEqual(row["replacement"], len(actions) == 2)

    def test_authority_output_and_incomplete_flags(self):
        document = plan(["create"], "aws_iam_role")
        document["output_changes"] = {MARKER: {"actions": ["update"], "after": MARKER, "after_unknown": True}}
        document["complete"] = False
        result = self.run_plan(document)
        self.assertEqual(result.returncode, 1)
        output = json.loads(result.stdout)
        self.assertIn("authority-or-exposure-review", output["resources"][0]["flags"])
        self.assertEqual(output["changed_outputs"], 1)
        self.assertTrue(output["unknown_outputs"])

    def test_captured_engine_exits_and_mismatch(self):
        unchanged = {"format_version": "1.2", "planned_values": {}}
        self.assertEqual(self.run_plan(unchanged, "--detailed-exit-code", "0").returncode, 0)
        error = self.run_plan(plan(), "--detailed-exit-code", "1")
        self.assertEqual(error.returncode, 1)
        self.assertEqual(error.stdout, "")
        self.assertIn("engine planning failed", error.stderr)
        self.assertEqual(self.run_plan(plan(), "--detailed-exit-code", "2").returncode, 0)
        for document, code in ((plan(), "0"), (unchanged, "2")):
            self.assertEqual(self.run_plan(document, "--detailed-exit-code", code).returncode, 1)

    def test_unknown_actions_are_withheld_and_rejected(self):
        result = self.run_plan(plan([MARKER]))
        self.assertEqual(result.returncode, 1)
        self.assertEqual(json.loads(result.stdout)["resources"][0]["actions"], ["<unsupported>"])

    def test_exact_additional_stateful_types(self):
        document = plan(["delete"], "vendor_retained_object")
        self.assertEqual(self.run_plan(document).returncode, 0)
        flagged = self.run_plan(document, "--stateful-type", "vendor_retained_object")
        self.assertEqual(flagged.returncode, 1)
        self.assertIn("stateful-destruction", json.loads(flagged.stdout)["findings"])
        self.assertEqual(self.run_plan(document, "--stateful-type", "vendor_other").returncode, 0)
        self.assertEqual(self.run_plan(document, "--stateful-type", "bad*type").returncode, 2)

    def test_malformed_and_help(self):
        for document in ({}, {"format_version": "9.0", "planned_values": {}}, [], {"format_version": "1.0", "planned_values": {}, "checks": [MARKER]}):
            self.assertEqual(self.run_plan(document).returncode, 2)
        self.input.write_text('{"malformed": "' + MARKER)
        result = subprocess.run([sys.executable, str(SCRIPT), str(self.input)], text=True, capture_output=True)
        self.assertEqual(result.returncode, 2)
        self.assertNotIn(MARKER, result.stderr)
        result = subprocess.run([sys.executable, str(SCRIPT), "--help"], cwd=self.path, text=True, capture_output=True)
        self.assertEqual(result.returncode, 0)
        self.assertIn("Exits:", result.stdout)
        self.assertEqual(set(p.name for p in self.path.iterdir()), {"plan.json", "saved.plan"})


class ExitMappingTests(unittest.TestCase):
    def test_wrapper_capture_under_fail_fast(self):
        classifier = SCRIPT.with_name("plan-exit.sh")
        with tempfile.TemporaryDirectory(prefix="exit-contract-") as directory:
            fake = Path(directory) / "fake-engine"
            fake.write_text('#!/bin/sh\nexit "$1"\n')
            fake.chmod(0o755)
            wrapper = 'set -eu; if "$1" "$2"; then code=0; else code=$?; fi; sh "$3" "$code"'
            for status, code, output in ((0, 0, "plan_changes=false\n"), (2, 0, "plan_changes=true\n"), (1, 1, ""), (3, 1, "")):
                result = subprocess.run(["sh", "-c", wrapper, "fixture", str(fake), str(status), str(classifier)], capture_output=True, text=True)
                self.assertEqual((result.returncode, result.stdout), (code, output))
            before = {p.name: p.read_bytes() for p in Path(directory).iterdir()}
            for args, code in ((["--help"], 0), ([], 2), (["invalid"], 2), (["0", "2"], 2)):
                result = subprocess.run(["sh", str(classifier), *args], cwd=directory, capture_output=True, text=True)
                self.assertEqual(result.returncode, code)
            self.assertEqual(before, {p.name: p.read_bytes() for p in Path(directory).iterdir()})


if __name__ == "__main__":
    unittest.main(verbosity=2)
