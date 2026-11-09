"""Offline matrix expansion; these fixtures do not execute authorization."""

import csv
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
SCRIPT = HERE.parents[1] / "skills/api-authorization/scripts/authz-matrix-cases.py"
GOOD = (HERE / "fixtures/pass.csv").read_text(encoding="utf-8")
HEADER, ALLOW, DENY = GOOD.strip().splitlines()


class MatrixTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix="authz-matrix-")
        self.directory = Path(self.temporary.name)
        self.path = self.directory / "matrix.csv"

    def tearDown(self):
        self.temporary.cleanup()

    def run_cli(self, data, *extra):
        self.path.write_text(data, encoding="utf-8")
        return subprocess.run([sys.executable, str(SCRIPT), str(self.path), *extra],
                              capture_output=True, text=True, cwd=self.directory)

    def test_expands_combinations_with_explicit_expected_results(self):
        result = self.run_cli(GOOD)
        self.assertEqual(result.returncode, 0, result.stderr)
        report = json.loads(result.stdout)
        self.assertEqual(report["count"], 6)
        cases = report["cases"]
        self.assertEqual({(c["role"], c["tenant"], c["entrypoint"], c["expect"]) for c in cases},
                         {("member", "same", "http", "allow"), ("member", "same", "export", "allow"),
                          ("auditor", "same", "http", "allow"), ("auditor", "same", "export", "allow"),
                          ("member", "other", "http", "deny"), ("member", "other", "export", "deny")})
        self.assertEqual(len({c["id"] for c in cases}), 6)

    def test_repeat_is_deterministic_and_does_not_write(self):
        first = self.run_cli(GOOD)
        before = {p.name: p.read_bytes() for p in self.directory.iterdir()}
        second = self.run_cli(GOOD)
        self.assertEqual(first.stdout, second.stdout)
        self.assertEqual(before, {p.name: p.read_bytes() for p in self.directory.iterdir()})

    def test_duplicate_and_conflicting_cells_fail_without_partial_output(self):
        for extra in (DENY, DENY.rsplit(",", 1)[0] + ",allow"):
            result = self.run_cli(GOOD + extra + "\n")
            self.assertEqual(result.returncode, 1)
            self.assertEqual(result.stdout, "")
            self.assertIn("repeated cell", result.stderr)
        self.assertEqual(self.run_cli(GOOD).returncode, 0)

    def test_blank_wildcard_duplicate_dimension_and_bad_expectation(self):
        for broken in (GOOD.replace("same,", ",", 1),
                       GOOD.replace("same,", "*,", 1),
                       GOOD.replace("member|auditor", "member|member"),
                       GOOD.replace(",deny", ",unknown")):
            result = self.run_cli(broken)
            self.assertEqual(result.returncode, 1)
            self.assertEqual(result.stdout, "")

    def test_empty_and_missing_allow_or_deny_control_fail(self):
        for value in (HEADER + "\n", HEADER + "\n" + ALLOW + "\n", HEADER + "\n" + DENY + "\n"):
            result = self.run_cli(value)
            self.assertEqual(result.returncode, 1)
            self.assertIn("allow", result.stderr)

    def test_usage_schema_and_csv_errors(self):
        for value in (GOOD.replace("entrypoint", "path", 1),
                      GOOD.replace(",expect", ",expect,expect", 1),
                      GOOD + "member,same\n", GOOD + '"unterminated'):
            result = self.run_cli(value)
            self.assertEqual(result.returncode, 2)
            self.assertEqual(result.stdout, "")
        for bound in ("0", "-1", "bad"):
            self.assertEqual(self.run_cli(GOOD, "--max-cases", bound).returncode, 2)

    def test_bound_refuses_work_without_partial_cases(self):
        result = self.run_cli(GOOD, "--max-cases", "5")
        self.assertEqual(result.returncode, 1)
        self.assertEqual(result.stdout, "")
        self.assertIn("--max-cases", result.stderr)
        self.assertEqual(self.run_cli(GOOD, "--max-cases", "6").returncode, 0)

    def test_diagnostics_do_not_echo_labels(self):
        marker = "synthetic-secret-marker-782"
        duplicate = DENY.replace("member", marker)
        result = self.run_cli(GOOD + duplicate + "\n" + duplicate + "\n")
        self.assertEqual(result.returncode, 1)
        self.assertNotIn(marker, result.stdout + result.stderr)

    def expanded(self):
        result = self.run_cli(GOOD)
        self.assertEqual(result.returncode, 0, result.stderr)
        return json.loads(result.stdout)["cases"]

    def observed_rows(self):
        return [[case["id"], case["expect"], case["identity"]] for case in self.expanded()]

    def check_results(self, rows, matrix=GOOD, header=("id", "observed", "identity")):
        results = self.directory / "results.csv"
        with results.open("w", newline="", encoding="utf-8") as out:
            writer = csv.writer(out)
            writer.writerow(header)
            writer.writerows(rows)
        return self.run_cli(matrix, "--results", str(results))

    def test_all_results_and_identities_pass_on_repeat(self):
        rows = self.observed_rows()
        first = self.check_results(rows)
        before = {p.name: p.read_bytes() for p in self.directory.iterdir()}
        second = self.check_results(rows)
        self.assertEqual(first.returncode, 0, first.stderr)
        self.assertEqual(json.loads(first.stdout), {"checked": 6, "findings": []})
        self.assertEqual(first.stdout, second.stdout)
        self.assertEqual(before, {p.name: p.read_bytes() for p in self.directory.iterdir()})

    def test_leak_and_deny_all_fail(self):
        rows = self.observed_rows()
        rows[-1][1] = "allow"
        result = self.check_results(rows)
        self.assertEqual(result.returncode, 1)
        self.assertIn("denial-failed", result.stdout)
        result = self.check_results([[i, "deny", identity] for i, _, identity in self.observed_rows()])
        self.assertEqual(result.returncode, 1)
        self.assertIn("over-denied", result.stdout)

    def test_missing_unknown_duplicate_and_invalid_result_fail(self):
        rows = self.observed_rows()
        variations = [(rows[1:], "missing-result"),
                      (rows + [["synthetic-secret-marker", "deny", "app_api"]], "unknown-result"),
                      (rows + rows[:1], "duplicate-result"),
                      ([[rows[0][0], "403", "app_api"], *rows[1:]], "bad-result")]
        for data, rule in variations:
            result = self.check_results(data)
            self.assertEqual(result.returncode, 1, result.stderr)
            self.assertIn(rule, result.stdout)
            self.assertNotIn("synthetic-secret-marker", result.stdout + result.stderr)

    def test_wrong_or_unrecorded_runtime_identity_fails(self):
        rows = self.observed_rows()
        for identity in ("postgres", "", "synthetic-secret-marker"):
            rows[0][2] = identity
            result = self.check_results(rows)
            self.assertEqual(result.returncode, 1)
            self.assertIn("wrong-identity", result.stdout)
            self.assertNotIn("synthetic-secret-marker", result.stdout + result.stderr)

    def test_results_schema_and_empty_results(self):
        self.assertEqual(self.check_results([], header=("id", "observed")).returncode, 2)
        result = self.check_results([])
        self.assertEqual(result.returncode, 1)
        self.assertEqual(len(json.loads(result.stdout)["findings"]), 6)
        self.assertEqual(self.check_results([["only-one-field"]]).returncode, 2)

    def test_identity_is_required_and_case_ids_bind_policy(self):
        self.assertEqual(self.run_cli(GOOD.replace(",app_api,", ",,", 1)).returncode, 1)
        rows = self.observed_rows()
        for changed in (GOOD.replace(",read,", ",download,"),
                        GOOD.replace(",app_api,", ",app_jobs,")):
            result = self.check_results(rows, matrix=changed)
            self.assertEqual(result.returncode, 1)
            self.assertIn("unknown-result", result.stdout)
            self.assertIn("missing-result", result.stdout)
        reordered = "\n".join((HEADER, DENY, ALLOW)) + "\n"
        self.assertEqual(self.check_results(rows, matrix=reordered).returncode, 0)

    def test_help_has_no_side_effect(self):
        result = subprocess.run([sys.executable, str(SCRIPT), "--help"], cwd=self.directory,
                                capture_output=True, text=True)
        self.assertEqual(result.returncode, 0)
        self.assertIn("Exit:", result.stdout)
        self.assertEqual(list(self.directory.iterdir()), [])


if __name__ == "__main__":
    unittest.main(verbosity=2)
