"""Accept, reject, and repeat fixtures for the standalone brief contract."""

import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
CHECKER = HERE.parents[1] / "skills/agent-briefing/scripts/check-brief.py"
BASE = (HERE / "valid.md").read_text()
SECTIONS = re.findall(r"^## (.+)$", BASE, re.M)
RETURN = (
    "Result first", "Evidence", "Artifacts and revisions", "Commands and results",
    "Unresolved claims", "Decisions needed", "Assumptions and surprises", "Usage",
)


def remove_section(text, heading):
    return re.sub(rf"^## {re.escape(heading)}\n.*?(?=^## |\Z)", "", text, flags=re.M | re.S)


class BriefTests(unittest.TestCase):
    def check(self, text, expected=0, fragments=("PASS",)):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "brief.md"
            path.write_text(text)
            before = path.read_bytes()
            for _ in range(2):
                result = subprocess.run([sys.executable, str(CHECKER), str(path)], text=True, capture_output=True)
                self.assertEqual(result.returncode, expected, result.stdout + result.stderr)
                self.assertNotIn("Traceback", result.stderr)
                for fragment in fragments:
                    self.assertIn(fragment, result.stdout + result.stderr)
                self.assertEqual(path.read_bytes(), before)
                self.assertEqual([p.name for p in Path(directory).iterdir()], ["brief.md"])

    def test_valid_leaf_repeat(self):
        self.check(BASE)

    def test_every_missing_section_is_named(self):
        self.assertEqual(len(SECTIONS), 19)
        for heading in SECTIONS:
            with self.subTest(heading=heading):
                self.check(remove_section(BASE, heading), 1, (heading, "missing field"))

    def test_empty_and_comment_only_field(self):
        for value in ("", "<!-- supplied later -->", "- "):
            text = re.sub(r"^## Goal\n.*?(?=^## )", f"## Goal\n\n{value}\n\n", BASE, flags=re.M | re.S)
            self.check(text, 1, ("Goal", "missing field"))

    def test_names_all_missing_fields_in_one_run(self):
        text = BASE
        for heading in ("Goal", "Permissions", "Capability skills", "Raw report path"):
            text = remove_section(text, heading)
        self.check(text, 1, ("Goal", "Permissions", "Capability skills", "Raw report path"))

    def test_fenced_heading_is_not_a_field(self):
        text = remove_section(BASE, "Goal") + "\n```markdown\n## Goal\nA decoy.\n```\n"
        self.check(text, 1, ("Goal: missing field",))
        text = remove_section(BASE, "Goal") + "\n~~~markdown\n## Goal\nA decoy.\n~~~\n"
        self.check(text, 1, ("Goal: missing field",))

    def test_duplicate_and_placeholder_fields(self):
        self.check(BASE + "\n## Goal\nAnother goal.\n", 1, ("duplicate heading",))
        self.check(BASE.replace("Determine whether", "{{fill goal}} Determine whether"), 1, ("Goal", "placeholders"))
        self.check(BASE.replace("Determine whether", "TBD Determine whether"), 1, ("Goal", "placeholders"))

    def test_each_return_obligation(self):
        for name in RETURN:
            text = re.sub(rf"^- {re.escape(name)}:.*\n", "", BASE, flags=re.M)
            self.check(text, 1, (f"Return contract / {name}",))

    def test_each_permission_obligation(self):
        for name in ("Read", "Write", "External actions"):
            text = re.sub(rf"^- {re.escape(name)}:.*\n", "", BASE, flags=re.M)
            self.check(text, 1, (f"Permissions / {name}",))

    def test_raw_path_shape(self):
        for path in ("relative/report.md", "/workspace/run/raw/", "/workspace/../report.md", "/one.md\n/two.md"):
            text = BASE.replace("## Raw report path\n\n/workspace/run/raw/inspect-r1.md", f"## Raw report path\n\n{path}")
            self.check(text, 1, ("Raw report path",))

    def child_budget(self):
        return BASE.replace(
            "Delegation: no",
            "Delegation: yes\nWorker starts: 2\nRetries: 1\nReview rounds: 1\nConcurrency ceiling: 2\nLedger: /workspace/run/BUDGET.md",
        )

    def test_explicit_child_allocation(self):
        self.check(self.child_budget())
        for name in ("Worker starts", "Retries", "Review rounds", "Concurrency ceiling", "Ledger"):
            text = re.sub(rf"^{re.escape(name)}:.*\n", "", self.child_budget(), flags=re.M)
            self.check(text, 1, (f"Budget / {name}",))

    def test_child_ceiling_and_finite_counters(self):
        for text, name in (
            (self.child_budget().replace("ceiling: 2", "ceiling: 9"), "Concurrency ceiling"),
            (self.child_budget().replace("Worker starts: 2", "Worker starts: 0"), "Worker starts"),
            (self.child_budget().replace("Retries: 1", "Retries: -1"), "Retries"),
            (self.child_budget().replace("Review rounds: 1", "Review rounds: unlimited"), "Review rounds"),
            (self.child_budget().replace("Ledger: /workspace", "Ledger: relative/workspace"), "Ledger"),
        ):
            self.check(text, 1, (f"Budget / {name}",))

    def test_delegation_and_stop_are_explicit(self):
        self.check(BASE.replace("Delegation: no", "Delegation: maybe"), 1, ("Budget / Delegation",))
        self.check(re.sub(r"^Stop after:.*\n", "", BASE, flags=re.M), 1, ("Budget / Stop after",))

    def test_template_is_not_ready_to_dispatch(self):
        template = HERE.parents[1] / "skills/agent-briefing/assets/brief.md"
        self.check(template.read_text(), 1, ("placeholders",))

    def test_usage(self):
        for arguments in ([], ["/missing/brief.md"], ["--unknown"]):
            result = subprocess.run([sys.executable, str(CHECKER), *arguments], capture_output=True, text=True)
            self.assertEqual(result.returncode, 2, result.stdout + result.stderr)


if __name__ == "__main__":
    unittest.main()
