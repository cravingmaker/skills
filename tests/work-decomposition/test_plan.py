"""Accept, reject, and repeat fixtures for the recorded plan invariants."""

import copy
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
CHECKER = HERE.parents[1] / "skills/work-decomposition/scripts/check-plan.py"
BASE = json.loads((HERE / "valid.json").read_text())


class PlanTests(unittest.TestCase):
    def run_source(self, source, expected, fragment="", markdown=False):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "PLAN.md"
            path.write_text(f"# Plan\n\n```json\n{source}\n```\n" if markdown else source)
            before = path.read_bytes()
            for _ in range(2):
                result = subprocess.run([sys.executable, str(CHECKER), str(path)], text=True, capture_output=True)
                self.assertEqual(result.returncode, expected, result.stdout + result.stderr)
                self.assertIn(fragment, result.stdout + result.stderr)
                self.assertNotIn("Traceback", result.stderr)
                self.assertEqual(path.read_bytes(), before)
                self.assertEqual([p.name for p in Path(directory).iterdir()], ["PLAN.md"])

    def check(self, value, expected=0, fragment="PASS", markdown=False):
        self.run_source(json.dumps(value), expected, fragment, markdown)

    def test_valid_json_and_markdown_repeat(self):
        self.check(BASE)
        self.check(BASE, markdown=True)

    def test_direct_zero_start_budget(self):
        value = copy.deepcopy(BASE)
        value["tasks"] = [value["tasks"][0]]
        value["budget"]["worker_starts"]["limit"] = 0
        value["budget"]["reserve"]["worker_starts"] = 0
        self.check(value)

    def test_each_delegation_reason(self):
        for reason in ("context-isolation", "independent-parallel-work", "independent-verification", "different-capability"):
            with self.subTest(reason=reason):
                value = copy.deepcopy(BASE)
                value["tasks"][1]["execution"] = reason
                self.check(value)

    def test_missing_task_fields(self):
        for field in ("id", "owner", "execution", "depends_on", "write_paths", "reason"):
            with self.subTest(field=field):
                value = copy.deepcopy(BASE)
                del value["tasks"][1][field]
                self.check(value, 1, field)

    def test_empty_task_list_and_identity(self):
        for field, replacement in (("tasks", []), ("run_id", ""), ("integration_owner", []), ("workspace", "relative")):
            value = copy.deepcopy(BASE)
            value[field] = replacement
            self.check(value, 1, field)

    def test_invalid_dependency_graph(self):
        variants = [
            ("unknown", lambda v: v["tasks"][1].update(depends_on=["missing"])),
            ("cycle", lambda v: v["tasks"][0].update(depends_on=["join"])),
            ("duplicate task ID", lambda v: v["tasks"][1].update(id="contract")),
            ("duplicate dependencies", lambda v: v["tasks"][1].update(depends_on=["contract", "contract"])),
        ]
        for fragment, mutate in variants:
            with self.subTest(fragment=fragment):
                value = copy.deepcopy(BASE)
                mutate(value)
                self.check(value, 1, fragment)

    def test_parallel_parent_child_same_path_and_same_owner(self):
        for path in ("src/a", "src/a/file.ts", "."):
            value = copy.deepcopy(BASE)
            value["tasks"][2]["write_paths"] = [path]
            value["tasks"][2]["owner"] = value["tasks"][1]["owner"]
            self.check(value, 1, "parallel writers a and b overlap")

    def test_ordered_and_transitively_ordered_writers(self):
        value = copy.deepcopy(BASE)
        value["tasks"][2]["depends_on"] = ["a"]
        value["tasks"][2]["write_paths"] = ["src/a/file.ts"]
        self.check(value)
        # join writes the same subtree as contract through the intervening tasks.

    def test_readers_and_literal_path_components(self):
        value = copy.deepcopy(BASE)
        value["tasks"][1]["write_paths"] = []
        self.check(value)
        self.check(BASE)  # src/a and src/ab are disjoint.

    def test_invalid_path_patterns(self):
        for path in ("src/**", "src/../shared", "src\\a", "src/[ab]", "src/a\nother", ""):
            value = copy.deepcopy(BASE)
            value["tasks"][1]["write_paths"] = [path]
            self.check(value, 1, "write_paths")

    def test_existing_symlink_and_absolute_alias_overlap(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "real").mkdir()
            (root / "alias").symlink_to(root / "real", target_is_directory=True)
            value = copy.deepcopy(BASE)
            value["workspace"] = directory
            value["tasks"][1]["write_paths"] = ["alias"]
            value["tasks"][2]["write_paths"] = [str(root / "real/file")]
            self.check(value, 1, "overlap")

    def test_budget_required_fields_and_counter_types(self):
        value = copy.deepcopy(BASE)
        del value["budget"]
        self.check(value, 1, "budget")
        for field in ("coordinator", "worker_starts", "retries", "review_rounds", "concurrency", "reserve"):
            value = copy.deepcopy(BASE)
            del value["budget"][field]
            self.check(value, 1, field)
        for name in ("worker_starts", "retries", "review_rounds"):
            for invalid in (True, -1, 1.5, "3", None):
                value = copy.deepcopy(BASE)
                value["budget"][name]["limit"] = invalid
                self.check(value, 1, name)

    def test_ninth_active_and_lower_host_ceiling(self):
        value = copy.deepcopy(BASE)
        value["budget"]["worker_starts"].update(limit=20, used=9)
        value["budget"]["concurrency"]["active"] = 9
        self.check(value, 1, "active exceeds ceiling")
        value["budget"]["concurrency"].update(ceiling=2, active=3)
        self.check(value, 1, "active exceeds ceiling")
        value["budget"]["concurrency"].update(ceiling=9, active=0)
        self.check(value, 1, "ceiling")

    def test_active_runs_need_shared_start_charges(self):
        value = copy.deepcopy(BASE)
        value["budget"]["concurrency"]["active"] = 1
        self.check(value, 1, "including descendants and evals")

    def test_fresh_findings_do_not_bypass_total_start_limit(self):
        value = copy.deepcopy(BASE)
        value["budget"]["worker_starts"]["used"] = 6
        value["budget"]["concurrency"]["active"] = 1
        self.check(value, 1, "used exceeds limit")

    def test_retry_and_round_caps(self):
        for name in ("retries", "review_rounds"):
            value = copy.deepcopy(BASE)
            value["budget"][name]["used"] = value["budget"][name]["limit"] + 1
            self.check(value, 1, name)

    def test_reserve_and_allocations(self):
        value = copy.deepcopy(BASE)
        value["budget"]["worker_starts"]["used"] = 5
        self.check(value, 1, "consumed the reserve")
        value["budget"]["worker_starts"].update(limit=2, used=0)
        self.check(value, 1, "task allocations exceed limit")

    def test_invalid_input_and_usage(self):
        self.run_source('{"tasks": [}', 1, "fix the input")
        self.run_source('{"tasks": [], "tasks": []}', 1, "duplicate key")
        self.run_source('{"budget": NaN}', 1, "non-finite")
        self.run_source("[]", 1, "fenced json")
        self.run_source("```json\n{}\n```\n```json\n{}\n```", 1, "exactly one")
        for arguments in ([], ["/missing/plan.json"], ["--unknown"]):
            result = subprocess.run([sys.executable, str(CHECKER), *arguments], capture_output=True, text=True)
            self.assertEqual(result.returncode, 2, result.stdout + result.stderr)


if __name__ == "__main__":
    unittest.main()
