"""Offline reference-integrity checks and independent consumer-query oracles."""
import copy
import json
import sqlite3
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SKILL = ROOT / "skills/logical-data-modeling"
SCRIPT = SKILL / "scripts/check-model.py"


class ModelTests(unittest.TestCase):
    def setUp(self):
        self.work = tempfile.TemporaryDirectory(prefix="logical-model-test-")
        self.addCleanup(self.work.cleanup)
        self.path = Path(self.work.name) / "model.json"
        self.model = json.loads((SKILL / "assets/model-example.json").read_text())

    def run_model(self, model):
        self.path.write_text(json.dumps(model))
        return subprocess.run([sys.executable, str(SCRIPT), str(self.path)], capture_output=True, text=True)

    def test_accept_repeat_without_writes(self):
        self.path.write_text(json.dumps(self.model))
        before = self.path.read_bytes()
        args = [sys.executable, str(SCRIPT), str(self.path)]
        first = subprocess.run(args, capture_output=True, text=True)
        second = subprocess.run(args, capture_output=True, text=True)
        self.assertEqual(first.returncode, 0, first.stderr)
        self.assertEqual(first.stdout, second.stdout)
        self.assertEqual(self.path.read_bytes(), before)
        self.assertEqual(json.loads(first.stdout), {"ok": True, "findings": 0, "unresolved": 1})

    def test_reject_reference_and_grain_errors(self):
        mutations = [
            lambda m: m.update(questions=[]),
            lambda m: m["entities"][0].update(serves=["missing"]),
            lambda m: m["questions"][0].update(consumer=""),
            lambda m: m["mappings"][0].update(grain=""),
            lambda m: m["entities"][0].update(id="trade"),
            lambda m: m["entities"][0].update(grain=["missing"]),
            lambda m: m["entities"][0]["keys"][0].update(fields=["missing"]),
            lambda m: m["relationships"][0].update(to_key="missing"),
            lambda m: m["relationships"][0].update(fields=["issuer", "code"]),
            lambda m: m["relationships"][0].update(optional="yes"),
            lambda m: m["mappings"][0].update(entity="missing"),
            lambda m: m["mappings"].pop(),
            lambda m: m["mappings"][0].update(fields={"source": "missing"}),
            lambda m: m["mappings"][0].update(status="unbuilt", reason=""),
            lambda m: m["unresolved"][0].update(owner=""),
        ]
        for mutate in mutations:
            with self.subTest(mutation=mutate):
                model = copy.deepcopy(self.model)
                mutate(model)
                result = self.run_model(model)
                self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
                self.assertFalse(json.loads(result.stdout)["ok"])

    def test_explicit_unbuilt_is_preserved(self):
        self.model["mappings"][0].update(status="unbuilt", reason="Destination not implemented; owner assigned.")
        self.assertEqual(self.run_model(self.model).returncode, 0)

    def test_malformed_shape_is_a_finding(self):
        for value in ([], {}, {"entities": "wrong"}, {"entities": [{"id": []}]}):
            result = self.run_model(value)
            self.assertEqual(result.returncode, 1, result.stderr)
            self.assertNotIn("Traceback", result.stderr)

    def test_duplicate_json_member(self):
        self.path.write_text('{"entities": [], "entities": []}')
        result = subprocess.run([sys.executable, str(SCRIPT), str(self.path)], capture_output=True, text=True)
        self.assertEqual(result.returncode, 2)
        self.assertNotIn("Traceback", result.stderr)

    def test_help_and_unreadable_input(self):
        result = subprocess.run([sys.executable, str(SCRIPT), "--help"], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0)
        self.assertFalse(self.path.exists())
        result = subprocess.run([sys.executable, str(SCRIPT), "--unknown", "postgres://DO_NOT_ECHO"], capture_output=True, text=True)
        self.assertEqual(result.returncode, 2)
        self.assertNotIn("DO_NOT_ECHO", result.stdout + result.stderr)
        self.path.write_text('{"private":"DO_NOT_ECHO",')
        result = subprocess.run([sys.executable, str(SCRIPT), str(self.path)], capture_output=True, text=True)
        self.assertEqual(result.returncode, 2)
        self.assertNotIn("DO_NOT_ECHO", result.stdout + result.stderr)


class SemanticTests(unittest.TestCase):
    def setUp(self):
        self.sql = (SKILL / "assets/counterexamples.sql").read_text()
        self.expected = sorted([
            ("reuse_early", "alpha"), ("reuse_late", "beta"),
            ("ambiguous_candidates", "2"), ("ambiguous_accepted", "0"),
            ("missing_quantity", "7"), ("correction_before", "10"),
            ("correction_after", "12"), ("fanout_total", "12"),
        ])

    def query(self, sql):
        with sqlite3.connect(":memory:") as connection:
            return sorted(connection.execute(sql).fetchall())

    def test_all_five_independent_oracles(self):
        self.assertEqual(self.query(self.sql), self.expected)

    def test_lossy_models_are_distinguished(self):
        changes = [
            ("t.issuer = i.issuer AND t.code = i.code", "t.code = i.code"),
            ("AND t.day >= i.first_day AND t.day < i.last_day", ""),
            ("AND accepted = 1", "AND accepted IN (0, 1)"),
            ("LEFT JOIN identifiers", "JOIN identifiers"),
            ("recorded_day <= 2", "recorded_day <= 6"),
            ("CAST(quantity AS TEXT) FROM totals\n  WHERE EXISTS (SELECT 1 FROM tags WHERE tags.order_id = totals.order_id)",
             "CAST(SUM(lines.quantity) AS TEXT) FROM lines JOIN tags ON lines.order_id = tags.order_id"),
        ]
        for before, after in changes:
            with self.subTest(lossy_rule=before):
                self.assertIn(before, self.sql)
                self.assertNotEqual(self.query(self.sql.replace(before, after)), self.expected)


if __name__ == "__main__":
    unittest.main()
