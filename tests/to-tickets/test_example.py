"""Import the to-tickets worked example with the work-decomposition importer.

The example in skills/to-tickets/references/ticket-template.md is the owned
template's contract with the importer: if either side drifts, these tests fail.
"""

import hashlib
import json
import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
TEMPLATE = ROOT / "skills/to-tickets/references/ticket-template.md"
IMPORTER = ROOT / "skills/work-decomposition/scripts/import-tickets.py"
BLOCK = re.compile(r"<!-- ticket-file: (\S+) -->\n```markdown\n(.*?)\n```", re.DOTALL)


def example_tickets():
    """Return {file name: text} for every worked-example block in the template."""
    tickets = {name: body + "\n" for name, body in BLOCK.findall(TEMPLATE.read_text(encoding="utf-8"))}
    if not tickets:
        raise AssertionError(f"no '<!-- ticket-file: NN-slug.md -->' blocks in {TEMPLATE}")
    return tickets


def field(text, name):
    match = re.search(rf"^\*\*{name}:\*\* (.+)$", text, re.MULTILINE)
    return match[1] if match else None


class ExampleImportTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name).resolve()
        self.issues = self.root / ".scratch/saved-searches/issues"
        self.issues.mkdir(parents=True)
        self.tickets = example_tickets()
        for name, text in self.tickets.items():
            (self.issues / name).write_text(text, encoding="utf-8")
        # The approved spec is not the sibling spec.md, so the importer must be told where it is.
        self.spec = self.root / "docs/specs/saved-searches.md"
        self.spec.parent.mkdir(parents=True)
        self.spec.write_bytes((HERE / "spec.md").read_bytes())

    def tearDown(self):
        self.temporary.cleanup()

    def run_importer(self, *extra):
        return subprocess.run([sys.executable, str(IMPORTER), str(self.issues), *extra],
                              text=True, capture_output=True)

    def snapshot(self):
        return {p: p.read_bytes() for p in self.root.rglob("*") if p.is_file()}

    def test_example_imports_exactly(self):
        before = self.snapshot()
        results = [self.run_importer("--spec", str(self.spec)) for _ in range(2)]
        for result in results:
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(result.stderr, "")
        self.assertEqual(results[0].stdout, results[1].stdout, "repeat import must print the same plan")
        self.assertEqual(self.snapshot(), before, "the importer must not write")

        plan = json.loads(results[0].stdout)
        tasks = {task["id"]: task for task in plan["tasks"]}
        self.assertEqual(sorted(tasks), sorted(Path(name).stem for name in self.tickets))
        spec_digest = "sha256:" + hashlib.sha256(self.spec.read_bytes()).hexdigest()
        stems = {int(Path(name).stem.split("-")[0]): Path(name).stem for name in self.tickets}
        for name, text in self.tickets.items():
            task = tasks[Path(name).stem]
            self.assertEqual(task["title"], re.match(r"# \d+: (.+)", text)[1])
            self.assertEqual(task["ticket_status"], field(text, "Status"))
            self.assertEqual(task["proof"], field(text, "Proof"), "the Proof line must be carried verbatim")
            self.assertEqual(task["acceptance"], re.findall(r"^- \[ \] (.+)$", text, re.MULTILINE))
            blocked = field(text, "Blocked by")
            expected = [] if blocked == "None" else [stems[int(n)] for n in blocked.split(", ")]
            self.assertEqual(task["depends_on"], expected)
            self.assertTrue(any(item.endswith(spec_digest) for item in task["inputs"]),
                            f"{name}: the explicitly passed spec must be bound by hash")

    def test_every_example_field_uses_the_strict_form(self):
        for name, text in self.tickets.items():
            self.assertRegex(text, r"^# \d{2}: \S", name)
            self.assertRegex(field(text, "Blocked by") or "", r"^(None|\d{2}(, \d{2})*)$", name)
            self.assertIn(field(text, "Status"), {"ready-for-agent", "ready-for-human"}, name)
            self.assertIn("→", field(text, "Proof") or "", f"{name}: Proof names a surface and a result")

    def test_space_separated_blockers_are_rejected(self):
        path = self.issues / "03-rerun-a-saved-search.md"
        path.write_text(path.read_text().replace("**Blocked by:** 01, 02", "**Blocked by:** 01 02"))
        result = self.run_importer("--spec", str(self.spec))
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertEqual(result.stdout, "")
        self.assertIn("cannot resolve blocker", result.stderr)

    def test_unknown_blocker_is_rejected(self):
        path = self.issues / "02-list-saved-searches.md"
        path.write_text(path.read_text().replace("**Blocked by:** 01", "**Blocked by:** 07"))
        result = self.run_importer("--spec", str(self.spec))
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertEqual(result.stdout, "")

    def test_missing_proof_in_the_owned_example_is_rejected(self):
        path = self.issues / "01-save-a-search.md"
        if not path.exists():
            path = self.issues / sorted(self.tickets)[0]
        original = path.read_text()
        path.write_text("\n".join(line for line in original.splitlines() if not line.startswith("**Proof:**")) + "\n")
        result = self.run_importer("--spec", str(self.spec))
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertEqual(result.stdout, "")
        self.assertIn("non-empty 'Proof:'", result.stderr)
        path.write_text(original)
        restored = self.run_importer("--spec", str(self.spec))
        self.assertEqual(restored.returncode, 0, restored.stderr)

    def test_missing_spec_is_rejected(self):
        result = self.run_importer()
        self.assertEqual(result.returncode, 2, result.stdout + result.stderr)
        self.assertEqual(result.stdout, "")
        self.assertIn("spec not found", result.stderr)


if __name__ == "__main__":
    if not IMPORTER.is_file():
        print(f"error: {IMPORTER} is missing; install the work-decomposition importer first", file=sys.stderr)
        sys.exit(2)
    unittest.main(verbosity=2)
