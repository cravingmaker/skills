"""Synthetic native-shaped exports test the pure-refactor boundary."""
from copy import deepcopy
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "skills/terraform-state-operations/scripts/check-refactor-plan.py"
MARKER = "SYNTHETIC_IMPORT_ID_WITHHELD"
ACCEPT = {"format_version": "1.2", "planned_values": {}, "resource_changes": [
    {"mode": "managed", "address": "test.new", "previous_address": "test.old", "change": {"actions": ["no-op"], "after": {"secret": MARKER}}},
    {"mode": "managed", "address": "test.import", "change": {"actions": ["no-op"], "importing": {"id": MARKER}}},
    {"mode": "data", "address": "data.test.read", "change": {"actions": ["read"]}}]}


class RefactorTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix="refactor-test-")
        self.path = Path(self.tmp.name) / "plan.json"

    def tearDown(self):
        self.tmp.cleanup()

    def run_plan(self, document, *extra):
        self.path.write_text(json.dumps(document))
        before = self.path.read_bytes()
        result = subprocess.run([sys.executable, str(SCRIPT), str(self.path), *extra], text=True, capture_output=True)
        self.assertEqual(self.path.read_bytes(), before)
        self.assertNotIn(MARKER, result.stdout + result.stderr)
        return result

    def test_accept_and_repeat(self):
        first, second = self.run_plan(ACCEPT), self.run_plan(ACCEPT)
        self.assertEqual(first.returncode, 0, first.stderr)
        self.assertEqual(first.stdout, second.stdout)
        output = json.loads(first.stdout)
        self.assertEqual((output["moved"], output["imported"]), (1, 1))

    def test_every_managed_mutation_is_rejected(self):
        for actions in (["create"], ["delete"], ["update"], ["create", "delete"], ["delete", "create"], ["forget"], ["read"]):
            document = deepcopy(ACCEPT)
            document["resource_changes"][0]["change"]["actions"] = actions
            result = self.run_plan(document)
            self.assertEqual(result.returncode, 1, result.stderr)
            self.assertEqual(json.loads(result.stdout)["findings"][0]["row"], 1)

    def test_exact_expected_operations_and_private_identifiers(self):
        expected = self.path.with_name("expected.json")
        expectation = {"moved": {"test.old": "test.new"}, "imported": ["test.import"]}
        expected.write_text(json.dumps(expectation))
        before = expected.read_bytes()
        first = self.run_plan(ACCEPT, "--expect", str(expected))
        self.assertEqual(first.returncode, 0, first.stderr)
        self.assertEqual(first.stdout, self.run_plan(ACCEPT, "--expect", str(expected)).stdout)
        self.assertEqual(before, expected.read_bytes())
        self.assertTrue(json.loads(first.stdout)["expectation_sha256"])
        for changed in ({"moved": {}, "imported": []},
                        {"moved": {"test.old": "test.wrong"}, "imported": ["test.import"]},
                        {"moved": {"test.old": "test.new"}, "imported": [MARKER]}):
            expected.write_text(json.dumps(changed))
            self.assertEqual(self.run_plan(ACCEPT, "--expect", str(expected)).returncode, 1)
        private = deepcopy(ACCEPT)
        private["resource_changes"][0].update(previous_address=MARKER + ".old", address=MARKER + ".new")
        expected.write_text(json.dumps({"moved": {MARKER + ".old": MARKER + ".new"}, "imported": ["test.import"]}))
        self.assertEqual(self.run_plan(private, "--expect", str(expected)).returncode, 0)

    def test_invalid_expectations_and_duplicate_moves(self):
        expected = self.path.with_name("expected.json")
        for value in ([], {"forgotten": []}, {"moved": []}, {"imported": [[MARKER]]},
                      {"imported": ["test.import", "test.import"]}, {"moved": {"same": "same"}}):
            expected.write_text(json.dumps(value))
            self.assertEqual(self.run_plan(ACCEPT, "--expect", str(expected)).returncode, 2)
        document = deepcopy(ACCEPT)
        document["resource_changes"].append(deepcopy(document["resource_changes"][0]))
        self.assertEqual(self.run_plan(document).returncode, 2)

    def test_unknown_outputs_drift_and_partial_work(self):
        variants = [{"output_changes": {MARKER: {"actions": ["update"], "after": MARKER}}},
                    {"resource_drift": [{}]}, {"complete": False}, {"errored": True},
                    {"deferred_changes": [{}]}, {"checks": [{"status": "unknown"}]}]
        for extra in variants:
            document = deepcopy(ACCEPT)
            document.update(extra)
            self.assertEqual(self.run_plan(document).returncode, 1)
        document = deepcopy(ACCEPT)
        document["resource_changes"][0]["change"]["after_unknown"] = {"sensitive": [False, True]}
        self.assertEqual(self.run_plan(document).returncode, 1)

    def test_malformed_and_help(self):
        for document in ({}, [], {"format_version": "9.0", "planned_values": {}}, {"format_version": "1.2", "planned_values": {}, "resource_changes": [None]}):
            self.assertEqual(self.run_plan(document).returncode, 2)
        self.path.write_text(MARKER)
        result = subprocess.run([sys.executable, str(SCRIPT), str(self.path)], text=True, capture_output=True)
        self.assertEqual(result.returncode, 2)
        self.assertNotIn(MARKER, result.stderr)
        before = self.path.read_bytes()
        result = subprocess.run([sys.executable, str(SCRIPT), "--help"], cwd=self.path.parent, text=True, capture_output=True)
        self.assertEqual(result.returncode, 0)
        self.assertEqual(self.path.read_bytes(), before)


if __name__ == "__main__":
    unittest.main(verbosity=2)
