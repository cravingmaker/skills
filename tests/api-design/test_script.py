"""Offline CLI fixtures; no network, model calls, or database."""

import copy
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
SCRIPT = HERE.parents[1] / "skills/api-design/scripts/check-problem-responses.py"
GOOD = json.loads((HERE / "fixtures/pass.json").read_text(encoding="utf-8"))


class ProblemTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix="problem-examples-")
        self.directory = Path(self.temporary.name)
        self.path = self.directory / "input.json"

    def tearDown(self):
        self.temporary.cleanup()

    def run_cli(self, data, *extra, raw=False):
        self.path.write_text(data if raw else json.dumps(data), encoding="utf-8")
        return subprocess.run([sys.executable, str(SCRIPT), str(self.path), *extra],
                              capture_output=True, text=True, cwd=self.directory)

    def test_accept_repeat_and_no_writes(self):
        first = self.run_cli(GOOD)
        before = {p.name: p.read_bytes() for p in self.directory.iterdir()}
        second = self.run_cli(GOOD)
        self.assertEqual(first.returncode, 0, first.stderr)
        self.assertEqual(first.stdout, second.stdout)
        self.assertEqual(json.loads(first.stdout), {"checked": 2, "findings": []})
        self.assertEqual(before, {p.name: p.read_bytes() for p in self.directory.iterdir()})

    def test_status_disagreement_rejects_then_recovers(self):
        cases = copy.deepcopy(GOOD)
        cases[0]["body"]["status"] = 400
        result = self.run_cli(cases)
        self.assertEqual(result.returncode, 1)
        self.assertEqual(json.loads(result.stdout)["findings"][0]["rule"], "status-mismatch")
        self.assertEqual(self.run_cli(GOOD).returncode, 0)

    def test_status_is_optional_unless_local_policy_requires_it(self):
        cases = copy.deepcopy(GOOD)
        del cases[0]["body"]["status"]
        self.assertEqual(self.run_cli(cases).returncode, 0)
        result = self.run_cli(cases, "--require-status")
        self.assertEqual(result.returncode, 1)
        self.assertIn("missing-status", result.stdout)

    def test_head_cannot_carry_content(self):
        cases = copy.deepcopy(GOOD)
        cases[1]["body"] = {}
        result = self.run_cli(cases)
        self.assertEqual(result.returncode, 1)
        self.assertIn("head-body", result.stdout)

    def test_media_and_problem_shape(self):
        for field, value, rule in (("content_type", "application/json", "media-type"),
                                   ("body", [], "problem-object"),
                                   ("body", {"status": True}, "status-mismatch"),
                                   ("body", {"title": 7}, "member-type")):
            with self.subTest(field=field, value=value):
                cases = copy.deepcopy(GOOD)
                cases[0][field] = value
                result = self.run_cli(cases)
                self.assertEqual(result.returncode, 1)
                self.assertIn(rule, result.stdout)
        cases = copy.deepcopy(GOOD)
        cases[0]["content_type"] = "Application/Problem+Json; charset=utf-8"
        self.assertEqual(self.run_cli(cases).returncode, 0)

    def test_empty_malformed_duplicate_and_nonfinite_are_usage_errors(self):
        for raw in ("[]", "{}", "[", '[{"method":"POST","method":"HEAD"}]',
                    '[{"method":"POST","http_status":409,"content_type":null,"body":{"status":NaN}}]'):
            result = self.run_cli(raw, raw=True)
            self.assertEqual(result.returncode, 2, raw)
            self.assertEqual(result.stdout, "")
            self.assertIn("see --help", result.stderr)

    def test_diagnostics_do_not_echo_input(self):
        marker = "synthetic-secret-marker-647"
        result = self.run_cli("{" + marker, raw=True)
        self.assertNotIn(marker, result.stdout + result.stderr)
        cases = copy.deepcopy(GOOD)
        cases[0]["body"] = {"status": 400, "detail": marker}
        result = self.run_cli(cases)
        self.assertEqual(result.returncode, 1)
        self.assertNotIn(marker, result.stdout + result.stderr)

    def test_internal_diagnostics_reject_without_echoing(self):
        for signature in ("Traceback (most recent call last)", "SQLSTATE 23505",
                          "duplicate key value violates", "syntax error at or near",
                          "panic: panicked at app.rs", "frame\n  at handler (app.js:1:2)"):
            cases = copy.deepcopy(GOOD)
            cases[0]["body"]["detail"] = signature + " synthetic-secret-marker"
            result = self.run_cli(cases)
            self.assertEqual(result.returncode, 1, signature)
            self.assertIn("internal-diagnostic", result.stdout)
            self.assertNotIn("synthetic-secret-marker", result.stdout + result.stderr)

    def test_numeric_status_and_unknown_extensions_pass(self):
        cases = copy.deepcopy(GOOD)
        cases[0]["body"]["status"] = 409.0
        self.assertEqual(self.run_cli(cases).returncode, 0)

    def test_help_has_no_input_or_write_side_effect(self):
        result = subprocess.run([sys.executable, str(SCRIPT), "--help"], cwd=self.directory,
                                capture_output=True, text=True)
        self.assertEqual(result.returncode, 0)
        self.assertIn("Exit:", result.stdout)
        self.assertEqual(list(self.directory.iterdir()), [])


if __name__ == "__main__":
    unittest.main(verbosity=2)
