"""Offline canonical emission and chronology checks."""

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
SCRIPT = HERE.parents[1] / "skills/api-compatibility/scripts/check-lifecycle-headers.py"
GOOD = json.loads((HERE / "fixtures/pass.json").read_text(encoding="utf-8"))


class LifecycleTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix="lifecycle-fields-")
        self.directory = Path(self.temporary.name)
        self.path = self.directory / "headers.json"

    def tearDown(self):
        self.temporary.cleanup()

    def run_cli(self, data, raw=False):
        self.path.write_text(data if raw else json.dumps(data), encoding="utf-8")
        return subprocess.run([sys.executable, str(SCRIPT), str(self.path)],
                              capture_output=True, text=True, cwd=self.directory)

    def test_pass_repeat_and_no_writes(self):
        first = self.run_cli(GOOD)
        before = {p.name: p.read_bytes() for p in self.directory.iterdir()}
        second = self.run_cli(GOOD)
        self.assertEqual(first.returncode, 0, first.stderr)
        self.assertEqual(first.stdout, second.stdout)
        self.assertEqual(json.loads(first.stdout), {"checked": 2, "findings": []})
        self.assertEqual(before, {p.name: p.read_bytes() for p in self.directory.iterdir()})

    def test_case_insensitive_names_and_each_field_alone(self):
        for fields in ({"dEpReCaTiOn": "@0"}, {"sunset": GOOD["Sunset"]},
                       {"Deprecation": "@-1", "Sunset": "Thu, 01 Jan 1970 00:00:00 GMT"}):
            result = self.run_cli(fields)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_swapped_forms_are_rejected(self):
        result = self.run_cli({"Deprecation": GOOD["Sunset"], "Sunset": "@0"})
        self.assertEqual(result.returncode, 1)
        self.assertEqual(len(json.loads(result.stdout)["findings"]), 2)

    def test_chronology_rejects_and_equal_instant_passes(self):
        fields = {"Deprecation": "@86401", "Sunset": GOOD["Sunset"]}
        result = self.run_cli(fields)
        self.assertEqual(result.returncode, 1)
        self.assertIn("chronology", result.stdout)
        fields["Deprecation"] = "@86400"
        self.assertEqual(self.run_cli(fields).returncode, 0)

    def test_invalid_date_weekday_and_timezone(self):
        for value in ("Thu, 02 Jan 1970 00:00:00 GMT",
                      "Fri, 31 Feb 1970 00:00:00 GMT",
                      "Fri, 02 Jan 1970 00:00:00 UTC"):
            result = self.run_cli({"Sunset": value})
            self.assertEqual(result.returncode, 1)
            self.assertIn("http-date-profile", result.stdout)

    def test_deprecation_is_bare_date_profile(self):
        for value in ("0", "@1.5", "@+0", "@1000000000000000", "@0;custom", True, None):
            result = self.run_cli({"Deprecation": value})
            self.assertEqual(result.returncode, 1, value)
        self.assertEqual(self.run_cli({"Deprecation": "@999999999999999"}).returncode, 0)

    def test_bad_input_duplicates_and_redaction(self):
        for raw in ("{}", "[]", "{", '{"Deprecation":"@0","deprecation":"@1"}',
                    '{"Authorization":"synthetic-secret-marker-562"}'):
            result = self.run_cli(raw, raw=True)
            self.assertEqual(result.returncode, 2)
            self.assertEqual(result.stdout, "")
            self.assertNotIn("synthetic-secret-marker-562", result.stderr)
        result = self.run_cli({"Deprecation": "synthetic-secret-marker-562"})
        self.assertEqual(result.returncode, 1)
        self.assertNotIn("synthetic-secret-marker-562", result.stdout + result.stderr)

    def test_help_has_no_side_effect(self):
        result = subprocess.run([sys.executable, str(SCRIPT), "--help"], cwd=self.directory,
                                capture_output=True, text=True)
        self.assertEqual(result.returncode, 0)
        self.assertIn("Exit:", result.stdout)
        self.assertEqual(list(self.directory.iterdir()), [])


if __name__ == "__main__":
    unittest.main(verbosity=2)
