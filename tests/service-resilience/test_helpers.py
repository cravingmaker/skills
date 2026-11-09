"""Offline CLI contracts: retry arithmetic, malformed input and source candidates."""

import copy
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
SCRIPTS = ROOT / "skills/service-resilience/scripts"
POLICY = ROOT / "skills/service-resilience/assets/retry-policy.json"


class Helpers(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="resilience-fixtures-")
        self.root = Path(self.temp.name)
        self.policy = json.loads(POLICY.read_text())

    def tearDown(self):
        self.temp.cleanup()

    def call(self, script, *args):
        return subprocess.run([sys.executable, str(SCRIPTS / script), *map(str, args)],
                              capture_output=True, text=True, timeout=10)

    def retry(self, value=None, text=None):
        path = self.root / "policy.json"
        path.write_text(text if text is not None else json.dumps(value or self.policy))
        return self.call("retry-amplification.py", path)

    def test_help_without_inputs_or_writes(self):
        for script in ("retry-amplification.py", "find-unbounded-calls.py"):
            before = list(self.root.iterdir())
            result = self.call(script, "--help")
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(result.stderr, "")
            self.assertEqual(list(self.root.iterdir()), before)
            self.assertIn("Exit:", result.stdout)

    def test_retry_accept_repeat_and_no_input_write(self):
        first = self.retry()
        before = (self.root / "policy.json").read_bytes()
        second = self.call("retry-amplification.py", self.root / "policy.json")
        self.assertEqual(first.returncode, 0, first.stderr)
        self.assertEqual(first.stdout, second.stdout)
        self.assertEqual((self.root / "policy.json").read_bytes(), before)
        result = json.loads(first.stdout)
        self.assertEqual(result["leaf_attempts_upper_bound"], 3)
        self.assertEqual(result["outer_bound_with_overhead_ms"], 1100)
        self.assertEqual(result["allocations"][1]["worst_total_ms"], 850)
        self.assertEqual(result["findings"], [])

    def test_nested_attempts_multiply_not_add(self):
        policy = copy.deepcopy(self.policy)
        policy["layers"][0]["attempts"] = 3
        policy["layers"][1]["attempts"] = 4
        result = self.retry(policy)
        self.assertEqual(result.returncode, 1, result.stderr)
        value = json.loads(result.stdout)
        self.assertEqual(value["leaf_attempts_upper_bound"], 12)
        self.assertIn("multiple_retry_owners", value["findings"])
        self.assertIn("leaf_attempt_budget_exceeded", value["findings"])

    def test_inner_retries_must_fit_parent_attempt(self):
        self.policy["layers"][0]["timeout_ms"] = 800
        result = self.retry()
        self.assertEqual(result.returncode, 1)
        self.assertIn("child_exceeds_parent_timeout:1", json.loads(result.stdout)["findings"])

    def test_overhead_consumes_deadline(self):
        self.policy["overhead_ms"] = 201
        result = self.retry()
        self.assertEqual(result.returncode, 1)
        self.assertIn("end_to_end_deadline_exceeded", json.loads(result.stdout)["findings"])

    def test_sequential_hops_add_time_and_calls_instead_of_multiplying(self):
        self.policy["hops"] = self.policy.pop("layers")
        self.policy["hops"][0].update(attempts=2, timeout_ms=100, max_backoff_ms=10)
        self.policy["max_leaf_attempts"] = 5
        self.policy["deadline_ms"] = 1160
        first = self.retry()
        self.assertEqual(first.returncode, 0, first.stderr + first.stdout)
        value = json.loads(first.stdout)
        self.assertEqual(value["leaf_attempts_upper_bound"], 5)
        self.assertEqual(value["outer_bound_with_overhead_ms"], 1160)
        self.assertEqual(first.stdout, self.retry().stdout)
        self.policy["deadline_ms"] = 1159
        self.assertIn("end_to_end_deadline_exceeded", json.loads(self.retry().stdout)["findings"])

    def test_two_budget_models_and_negative_reserve_refused(self):
        self.policy["hops"] = self.policy["layers"]
        self.assertEqual(self.retry().returncode, 2)
        self.policy.pop("hops")
        self.policy["overhead_ms"] = -1000
        self.assertEqual(self.retry().returncode, 2)

    def test_boolean_zero_negative_and_typo_are_usage_failures(self):
        for field, value in (("deadline_ms", True), ("max_leaf_attempts", 0),
                             ("overhead_ms", -1), ("layers", [])):
            policy = copy.deepcopy(self.policy)
            policy[field] = value
            self.assertEqual(self.retry(policy).returncode, 2, (field, value))
        self.policy["misspelled_budget"] = 4
        self.assertEqual(self.retry().returncode, 2)

    def test_malformed_and_duplicate_json_refused_without_echo(self):
        for text in ("{", '{"secret":"SYNTHETIC_CREDENTIAL","secret":1}', '{"layers":NaN}'):
            result = self.retry(text=text)
            self.assertEqual(result.returncode, 2)
            self.assertEqual(result.stdout, "")
            self.assertNotIn("SYNTHETIC_CREDENTIAL", result.stderr)

    def test_source_accept_repeat_and_read_only(self):
        paths = [HERE / "fixtures/bounded.ts", HERE / "fixtures/bounded.rs"]
        before = [p.read_bytes() for p in paths]
        first = self.call("find-unbounded-calls.py", *paths)
        second = self.call("find-unbounded-calls.py", *paths)
        self.assertEqual(first.returncode, 0, first.stderr)
        self.assertEqual(first.stdout, second.stdout)
        self.assertEqual([p.read_bytes() for p in paths], before)
        value = json.loads(first.stdout)
        self.assertEqual(value["files_scanned"], 2)
        self.assertFalse(value["complete_analysis"])
        self.assertEqual(value["candidates"], [])

    def test_source_rejects_visible_unbounded_calls(self):
        result = self.call("find-unbounded-calls.py", HERE / "fixtures/unbounded.ts",
                           HERE / "fixtures/unbounded.rs")
        self.assertEqual(result.returncode, 1, result.stderr)
        codes = [v["code"] for v in json.loads(result.stdout)["candidates"]]
        self.assertCountEqual(codes, ["fetch_no_visible_signal", "fanout_requires_input_bound",
                                    "pg_client_no_visible_query_timeout",
                                    "reqwest_no_visible_total_timeout",
                                    "reqwest_no_visible_total_timeout"])
        self.assertNotIn('method: "POST"', result.stdout)

    def test_directory_missing_empty_argv_and_unknown_suffix_refused(self):
        unknown = self.root / "source.txt"
        unknown.write_text("fetch(url)")
        for args in ([], [self.root], [self.root / "absent.ts"], [unknown]):
            result = self.call("find-unbounded-calls.py", *args)
            self.assertEqual(result.returncode, 2, args)

    def test_grafted_fanout_and_axios_candidates_ignore_comment_hints(self):
        source = self.root / "more.mts"
        source.write_text('await axios.get(url, { /* timeout: 20 */ });\n'
                          'await fetch(url, { /* signal: ignored */ method: "POST" });\n'
                          'await Promise.allSettled(values.map(send));\n'
                          'await axios.get(url, { signal });\n')
        result = self.call("find-unbounded-calls.py", source)
        codes = [v["code"] for v in json.loads(result.stdout)["candidates"]]
        self.assertCountEqual(codes, ["axios_no_visible_timeout_or_signal",
                                    "fetch_no_visible_signal", "fanout_requires_input_bound"])
        source = self.root / "more.rs"
        source.write_text('join_all(ids.iter().map(send)).await;\n')
        result = self.call("find-unbounded-calls.py", source)
        self.assertEqual([v["code"] for v in json.loads(result.stdout)["candidates"]],
                         ["fanout_requires_input_bound"])


if __name__ == "__main__":
    unittest.main()
