"""Offline plan fixtures with hand-derived ratios and inclusive counters."""
import copy
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
SCRIPT = HERE.parents[1] / "skills/postgres-query-performance/scripts/explain-summary.py"
BASE = json.loads((HERE / "plan.json").read_text())


class PlanTests(unittest.TestCase):
    def run_plan(self, data, expected=1, extra=(), candidate=None, raw=False):
        with tempfile.TemporaryDirectory() as temporary:
            work = Path(temporary)
            plan = work / "plan.json"
            plan.write_text(data if raw else json.dumps(data))
            args = [sys.executable, str(SCRIPT), str(plan), *extra]
            if candidate is not None:
                after = work / "after.json"
                after.write_text(json.dumps(candidate))
                args += ["--compare", str(after)]
            snapshot = {p.name: p.read_bytes() for p in work.iterdir()}
            outputs = [subprocess.run(args, cwd=work, capture_output=True, text=True) for _ in range(2)]
            self.assertEqual(outputs[0].stdout, outputs[1].stdout)
            for result in outputs:
                self.assertEqual(result.returncode, expected, result.stdout + result.stderr)
                self.assertNotIn("SECRET_SENTINEL", result.stdout + result.stderr)
                self.assertNotIn("Traceback", result.stderr)
            self.assertEqual(snapshot, {p.name: p.read_bytes() for p in work.iterdir()})
            return json.loads(outputs[0].stdout) if expected != 2 else None

    def test_inclusive_buffers_per_loop_ratio_and_worker_scope(self):
        result = self.run_plan(BASE)
        child = result["nodes"][1]
        self.assertEqual(result["root_buffers_inclusive"]["Shared Read Blocks"], 5)
        self.assertEqual(child["buffers"]["Shared Read Blocks"], 5)
        self.assertEqual(child["estimate_factor"], 20)
        self.assertEqual(child["approx_total_rows"], 60)
        self.assertEqual(child["workers"][0]["buffers"]["Shared Read Blocks"], 3)

    def test_zero_loops_and_zero_estimate_are_distinct(self):
        for estimated, actual, loops, flag in ((1, 0, 0, "not_executed"), (0, 2, 1, "zero_estimate"), (3, 0, 1, "zero_actual")):
            data = copy.deepcopy(BASE)
            child = data[0]["Plan"]["Plans"][0]
            child.update({"Plan Rows": estimated, "Actual Rows": actual, "Actual Loops": loops})
            result = self.run_plan(data)
            self.assertIn(flag, result["nodes"][1]["flags"])
            self.assertIsNone(result["nodes"][1]["estimate_factor"])

    def test_spill_loop_and_scan_flags(self):
        data = copy.deepcopy(BASE)
        data[0]["Plan"]["Plans"] += [
            {"Node Type": "Sort", "Plan Rows": 5, "Actual Rows": 5, "Actual Loops": 1,
             "Sort Space Type": "Disk", "Sort Space Used": 80, "Temp Written Blocks": 9},
            {"Node Type": "Hash", "Plan Rows": 8, "Actual Rows": 8, "Actual Loops": 1, "Hash Batches": 4},
            {"Node Type": "Seq Scan", "Plan Rows": 100, "Actual Rows": 100, "Actual Loops": 10}]
        result = self.run_plan(data, extra=("--large-scan-rows", "1000", "--high-loops", "10"))
        self.assertIn("disk_sort", result["nodes"][2]["flags"])
        self.assertIn("temp_io", result["nodes"][2]["flags"])
        self.assertIn("hash_batches", result["nodes"][3]["flags"])
        self.assertIn("many_loops", result["nodes"][4]["flags"])
        self.assertIn("large_sequential_scan", result["nodes"][4]["flags"])

    def test_clean_plan_and_comparison(self):
        clean = [{"Plan": {"Node Type": "Result", "Plan Rows": 1, "Actual Rows": 1, "Actual Loops": 1}, "Execution Time": 4}]
        self.assertEqual(self.run_plan(clean, 0)["findings"], [])
        after = copy.deepcopy(clean)
        after[0]["Execution Time"] = 3
        self.assertEqual(self.run_plan(clean, 0, candidate=after)["execution_ms_delta"], -1)
        estimated = [{"Plan": {"Node Type": "Result", "Plan Rows": 1}}]
        result = self.run_plan(estimated, candidate=after)
        self.assertIsNone(result["execution_ms_delta"])
        self.assertIn("missing_execution", result["baseline"]["nodes"][0]["flags"])

    def test_scan_filter_work_and_worker_spill(self):
        data = copy.deepcopy(BASE)
        child = data[0]["Plan"]["Plans"][0]
        child.update({"Plan Rows": 1, "Actual Rows": 1, "Actual Loops": 2,
                      "Rows Removed by Filter": 60000})
        child["Workers"][0].update({"Sort Space Type": "Disk", "Temp Written Blocks": 7})
        result = self.run_plan(data)
        output = result["nodes"][1]
        self.assertEqual(output["approx_examined_rows"], 120002)
        self.assertIn("large_sequential_scan", output["flags"])
        self.assertIn("worker_spill", output["flags"])
        self.assertIn("disk_sort", output["workers"][0]["flags"])
        self.assertEqual(result["root_buffers_inclusive"]["Shared Read Blocks"], 5)

    def test_invalid_input_and_metrics(self):
        for data in ([], {}, [{"Plan": {}}], BASE + BASE):
            self.run_plan(data, 2)
        for value in (-1, True, float("nan"), None, "SECRET_SENTINEL"):
            data = copy.deepcopy(BASE)
            data[0]["Plan"]["Actual Rows"] = value
            self.run_plan(data, 2)
        self.run_plan('{"SECRET_SENTINEL":', 2, raw=True)
        self.run_plan('[{"Plan":{},"Plan":{}}]', 2, raw=True)

    def test_unknown_type_not_echoed_and_help(self):
        data = copy.deepcopy(BASE)
        data[0]["Plan"]["Node Type"] = "SECRET_SENTINEL"
        self.assertEqual(self.run_plan(data)["nodes"][0]["node_type"], "Other")
        result = subprocess.run([sys.executable, str(SCRIPT), "--help"], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0)
        self.assertIn("never executes SQL", result.stdout)
        self.run_plan(BASE, 2, extra=("--high-loops", "nan"))

    def test_captured_limit_is_not_a_definite_estimate_error(self):
        data = json.loads((HERE / "captured-loops.json").read_text())
        result = self.run_plan(data)
        scan = result["nodes"][-1]
        self.assertEqual(scan["estimated_rows"], 15)
        self.assertEqual(scan["actual_rows_per_loop"], 1)
        self.assertIn("possibly_stopped_early", scan["flags"])
        self.assertNotIn("estimate_error", scan["flags"])
        self.assertEqual(result["root_buffers_inclusive"]["Shared Read Blocks"], 1151)

    def test_worker_shortfall_and_genuine_underestimate_stay_distinct(self):
        data = [{"Plan": {"Node Type": "Limit", "Plan Rows": 1, "Actual Rows": 1,
                          "Actual Loops": 1, "Workers Planned": 2, "Workers Launched": 1,
                          "Plans": [{"Node Type": "Seq Scan", "Plan Rows": 1,
                                     "Actual Rows": 20, "Actual Loops": 1}]}, "Execution Time": 3}]
        result = self.run_plan(data)
        self.assertIn("fewer_workers", result["nodes"][0]["flags"])
        self.assertEqual(result["nodes"][0]["workers_planned"], 2)
        self.assertIn("estimate_error", result["nodes"][1]["flags"])
        self.assertNotIn("possibly_stopped_early", result["nodes"][1]["flags"])


if __name__ == "__main__":
    unittest.main()
