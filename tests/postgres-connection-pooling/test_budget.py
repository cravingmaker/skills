"""Offline arithmetic, malformed-input, secrecy and read-only fixture checks."""
import copy
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "skills/postgres-connection-pooling/scripts/pool-budget.py"
EXAMPLE = ROOT / "skills/postgres-connection-pooling/assets/budget.json"
BASE = json.loads(EXAMPLE.read_text())


class BudgetTests(unittest.TestCase):
    def run_budget(self, data, code=0, raw=False):
        with tempfile.TemporaryDirectory() as temporary:
            work = Path(temporary)
            path = work / "budget.json"
            path.write_text(data if raw else json.dumps(data))
            before = path.read_bytes()
            results = [subprocess.run([sys.executable, str(SCRIPT), str(path)], cwd=work,
                                      capture_output=True, text=True) for _ in range(2)]
            self.assertEqual(results[0].stdout, results[1].stdout)
            self.assertEqual(results[0].stderr, results[1].stderr)
            for result in results:
                self.assertEqual(result.returncode, code, result.stdout + result.stderr)
                self.assertNotIn("Traceback", result.stderr)
                self.assertNotIn("SECRET_SENTINEL", result.stdout + result.stderr)
            self.assertEqual(path.read_bytes(), before)
            self.assertEqual(sorted(p.name for p in work.iterdir()), ["budget.json"])
            return json.loads(results[0].stdout) if code != 2 else None

    def test_example_and_both_connection_layers(self):
        result = self.run_budget(BASE)
        self.assertEqual(result["database_total"], 33)
        self.assertEqual(result["direct_sessions"], 12)
        self.assertEqual(result["pooled_backend_slots"], 10)
        self.assertEqual(result["database_headroom"], 47)
        self.assertEqual(result["poolers"][0]["clients"], 40)
        self.assertEqual(result["poolers"][0]["client_headroom"], 60)

    def test_peak_workers_and_rollout_overlap(self):
        data = copy.deepcopy(BASE)
        data["direct_groups"].append({"instances": 12, "pool_max": 4})
        result = self.run_budget(data, 1)
        self.assertEqual(result["database_total"], 81)
        self.assertEqual(result["database_headroom"], -1)
        self.assertEqual(result["findings"], [{"kind": "database_limit"}])

    def test_independent_limits_and_exact_boundary(self):
        data = copy.deepcopy(BASE)
        data["poolers"][0]["client_limit"] = 39
        result = self.run_budget(data, 1)
        self.assertEqual(result["database_total"], 33)
        self.assertEqual(result["findings"], [{"index": 0, "kind": "pooler_client_limit"}])
        data["poolers"][0]["client_limit"] = 40
        data["database_limit"] = 33
        self.assertEqual(self.run_budget(data)["database_headroom"], 0)

    def test_each_pooler_and_server_allocation(self):
        data = copy.deepcopy(BASE)
        data["poolers"].append({"client_groups": [{"instances": 2, "pool_max": 3}],
                                "client_limit": 5, "backend_slots": 9})
        result = self.run_budget(data, 1)
        self.assertEqual(result["database_total"], 42)
        self.assertEqual(result["findings"], [{"index": 1, "kind": "pooler_client_limit"}])

    def test_invalid_counts_missing_fields_and_unknown_keys(self):
        for value in (True, -1, 1.5, "SECRET_SENTINEL", None):
            data = copy.deepcopy(BASE)
            data["direct_groups"][0]["instances"] = value
            self.run_budget(data, 2)
        for key in BASE:
            data = copy.deepcopy(BASE)
            del data[key]
            self.run_budget(data, 2)
        data = copy.deepcopy(BASE)
        data["SECRET_SENTINEL"] = "SECRET_SENTINEL"
        self.run_budget(data, 2)
        for value in (0, False):
            data = copy.deepcopy(BASE)
            data["operator_reserve"] = value
            self.run_budget(data, 2)

    def test_invalid_json_duplicate_keys_empty_topology(self):
        for raw in ('{"SECRET_SENTINEL":', '{"a":1,"a":2}', '[]'):
            self.run_budget(raw, 2, raw=True)
        data = copy.deepcopy(BASE)
        data["direct_groups"] = []
        data["poolers"] = []
        self.run_budget(data, 2)

    def test_help_and_missing_file(self):
        result = subprocess.run([sys.executable, str(SCRIPT), "--help"], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0)
        self.assertIn("stdout", result.stdout)
        result = subprocess.run([sys.executable, str(SCRIPT), "/missing/SECRET_SENTINEL"], capture_output=True, text=True)
        self.assertEqual(result.returncode, 2)
        self.assertNotIn("SECRET_SENTINEL", result.stderr)


if __name__ == "__main__":
    unittest.main()
