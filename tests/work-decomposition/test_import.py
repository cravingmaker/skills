"""Accept, reject, and repeat fixtures for importing to-tickets files into a plan."""

import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
SCRIPTS = HERE.parents[1] / "skills/work-decomposition/scripts"
IMPORTER = SCRIPTS / "import-tickets.py"
CHECKER = SCRIPTS / "check-plan.py"


def run(*arguments):
    return subprocess.run([sys.executable, *map(str, arguments)], text=True, capture_output=True)


def fill(plan):
    """Make the coordinator's decisions the importer leaves open."""
    plan["integration_owner"] = "coordinator"
    for task in plan["tasks"]:
        task.update(owner="coordinator", execution="direct", write_paths=[f"src/{task['id']}"],
                    outputs=[f"src/{task['id']}"], shared_resources=[])
        del task["reason"]
    budget = plan["budget"]
    budget["coordinator"] = "coordinator"
    for name in ("worker_starts", "retries", "review_rounds"):
        budget[name]["limit"] = 0
    budget["concurrency"]["ceiling"] = 1
    budget["reserve"].update(worker_starts=0, plan="Coordinator integrates and verifies")
    return plan


class ImportTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name).resolve()
        shutil.copytree(HERE / "feature", self.root / ".scratch/search")
        self.issues = self.root / ".scratch/search/issues"

    def tearDown(self):
        self.temporary.cleanup()

    def ticket(self, name, text, proof=True):
        if proof and "Proof:" not in text:
            text += "\nProof: Open the search page; the expected products are listed\n"
        (self.issues / name).write_text(text)

    def imported(self, expected=0, fragment=""):
        before = {p: p.read_bytes() for p in self.root.rglob("*") if p.is_file()}
        results = [run(IMPORTER, self.issues) for _ in range(2)]
        for result in results:
            self.assertEqual(result.returncode, expected, result.stdout + result.stderr)
            self.assertIn(fragment, result.stdout + result.stderr)
            self.assertNotIn("Traceback", result.stderr)
        self.assertEqual(results[0].stdout, results[1].stdout)
        self.assertEqual({p: p.read_bytes() for p in self.root.rglob("*") if p.is_file()}, before)
        return json.loads(results[0].stdout) if expected == 0 else None

    def check(self, plan):
        path = self.root / "PLAN.md"
        path.write_text(f"# Plan\n\n```json\n{json.dumps(plan)}\n```\n")
        return run(CHECKER, path)

    def test_tickets_become_the_task_graph(self):
        plan = self.imported()
        self.assertEqual(plan["run_id"], "search")
        self.assertEqual(plan["workspace"], str(self.root))
        self.assertEqual(plan["source"], {"tickets": ".scratch/search/issues", "finished": ["04-price-field"]})
        tasks = {task["id"]: task for task in plan["tasks"]}
        self.assertEqual(list(tasks), ["01-index-products", "02-search-page", "03-filter-by-price"])
        self.assertEqual(tasks["01-index-products"]["depends_on"], [])
        self.assertEqual(tasks["02-search-page"]["depends_on"], ["01-index-products"])
        # A title resolves to its ticket; a finished blocker is already satisfied.
        self.assertEqual(tasks["03-filter-by-price"]["depends_on"], ["02-search-page"])
        self.assertEqual(tasks["03-filter-by-price"]["ticket_status"], "ready-for-human")
        self.assertEqual(tasks["03-filter-by-price"]["acceptance"], ["Results outside the range are hidden"])
        self.assertEqual(tasks["01-index-products"]["title"], "Index products")
        self.assertEqual(tasks["01-index-products"]["proof"], 'save a product named Lamp, then search "lamp"; Lamp is the first result')
        self.assertEqual(tasks["02-search-page"]["proof"], "Open the search page and enter lamp; Lamp is listed")
        ticket_input, spec_input = tasks["02-search-page"]["inputs"]
        self.assertRegex(ticket_input, r"^\.scratch/search/issues/02-search-page\.md sha256:[0-9a-f]{64}$")
        self.assertRegex(spec_input, r"^\.scratch/search/spec\.md sha256:[0-9a-f]{64}$")

    def test_checker_rejects_the_skeleton_until_filled(self):
        plan = self.imported()
        result = self.check(plan)
        self.assertEqual(result.returncode, 1, result.stdout)
        for fragment in ("integration_owner", ".owner", ".execution", ".write_paths", "01-index-products.outputs[0]: replace the placeholder",
                         "03-filter-by-price.shared_resources[0]", "02-search-page.reason", "budget.worker_starts", "budget.concurrency", "budget.reserve"):
            self.assertIn(fragment, result.stdout)
        result = self.check(fill(plan))
        self.assertEqual(result.returncode, 0, result.stdout)

    def test_plain_lines_and_list_blockers(self):
        self.ticket("02-search-page.md", "# 02: Search page\n\nBlocked by:\n\n- 01: Index products\n\nStatus: ready-for-agent\n\n"
                    "Proof:\n\n- open /search?q=lamp\n- Lamp is listed\n\n- [ ] Query works\n")
        plan = self.imported()
        self.assertEqual(plan["tasks"][1]["depends_on"], ["01-index-products"])
        self.assertEqual(plan["tasks"][1]["proof"], "open /search?q=lamp; Lamp is listed")
        self.assertEqual(plan["tasks"][1]["acceptance"], ["Query works"])

    def test_ticket_findings(self):
        cases = [
            ("02-search-page.md", "# 02: Search page\n\nStatus: ready-for-agent\n\n- [ ] Works\n", "add a 'Blocked by:' line"),
            ("02-search-page.md", "# 02: Search page\n\nBlocked by: 09\n\nStatus: ready-for-agent\n\n- [ ] Works\n", "cannot resolve blocker '09'"),
            ("02-search-page.md", "# 02: Search page\n\nBlocked by: Missing title\n\nStatus: ready-for-agent\n\n- [ ] Works\n", "cannot resolve blocker 'Missing title'"),
            ("02-search-page.md", "# 02: Search page\n\nBlocked by: 02\n\nStatus: ready-for-agent\n\n- [ ] Works\n", "cannot block itself"),
            ("02-search-page.md", "# 02: Search page\n\nBlocked by: None\n\n- [ ] Works\n", "add a 'Status:' line"),
            ("02-search-page.md", "# 02: Search page\n\nBlocked by: None\n\nStatus: needs-triage\n\n- [ ] Works\n", "needs-triage is not ready"),
            ("02-search-page.md", "# 02: Search page\n\nBlocked by: None\n\nStatus: ready-for-agent\n", "acceptance checkbox"),
            ("02-search-page.md", "Blocked by: None\n\nStatus: ready-for-agent\n\n- [ ] Works\n", "Title"),
            ("2-search-copy.md", "# 2: Copy\n\nBlocked by: None\n\nStatus: ready-for-agent\n\n- [ ] Works\n", "repeats"),
            ("notes.md", "# Notes\n", "rename it to NN-slug.md"),
        ]
        for name, text, fragment in cases:
            with self.subTest(fragment=fragment):
                original = (self.issues / name).read_bytes() if (self.issues / name).exists() else None
                self.ticket(name, text)
                self.imported(1, fragment)
                if original is None:
                    (self.issues / name).unlink()
                else:
                    (self.issues / name).write_bytes(original)

    def test_blockers_never_silently_drop_or_guess_an_edge(self):
        for value in ("01 02", "01 / 02", "None, 01", "01: wrong title"):
            with self.subTest(value=value):
                self.ticket("03-filter-by-price.md", "# 03: Filter by price\nStatus: ready-for-agent\n"
                            f"Blocked by: {value}\n- [ ] Results are filtered\n")
                self.imported(1, "cannot resolve blocker")
        self.ticket("02-search-page.md", "# 02: Index products\nStatus: ready-for-agent\n"
                    "Blocked by: 01\n- [ ] Search works\n")
        self.ticket("03-filter-by-price.md", "# 03: Filter by price\nStatus: ready-for-agent\n"
                    "Blocked by: Index products\n- [ ] Results are filtered\n")
        self.imported(1, "unambiguous exact title")
        self.ticket("03-filter-by-price.md", "# 03: Filter by price\nStatus: ready-for-agent\n"
                    "Blocked by: 01, 02\n- [ ] Results are filtered\n")
        plan = self.imported()
        self.assertEqual(plan["tasks"][2]["depends_on"], ["01-index-products", "02-search-page"])

    def test_blocker_continuations_are_fully_consumed_or_rejected(self):
        for blocked in ("01\n- 02", "None\n- 02", "\n- 01\n2. 02",
                        "\n- 01\n+ 02", "01\n02"):
            with self.subTest(blocked=blocked):
                self.ticket("03-filter-by-price.md", "# 03: Filter by price\nStatus: ready-for-agent\n"
                            f"Blocked by: {blocked}\n- [ ] Results are filtered\n")
                self.imported(1, "unsupported continuation of 'blocked by'")
        self.ticket("03-filter-by-price.md", "# 03: Filter by price\nStatus: ready-for-agent\n"
                    "Blocked by:\n- 01\n* 02\n\n## Acceptance\n- [ ] Results are filtered\n")
        self.assertEqual(self.imported()["tasks"][2]["depends_on"],
                         ["01-index-products", "02-search-page"])

    def test_nothing_left_to_plan(self):
        for path in self.issues.iterdir():
            path.write_text(path.read_text().replace("ready-for-agent", "done").replace("ready-for-human", "closed"))
        self.imported(1, "nothing left to plan")

    def test_missing_empty_and_placeholder_proof_reject_before_json(self):
        path = self.issues / "02-search-page.md"
        original = path.read_text()
        for value in (None, "", "   ", "{{drive the real surface}}"):
            with self.subTest(value=value):
                without = "\n".join(line for line in original.splitlines() if not line.startswith("Proof:")) + "\n"
                if value is not None:
                    without += f"Proof: {value}\n"
                path.write_text(without)
                self.imported(1, "non-empty 'Proof:'")
        path.write_text(original)
        self.imported()

    def test_proof_and_status_are_preserved_verbatim(self):
        proof = '`search --query="lamp"` → **Lamp** is listed with price 10.00'
        self.ticket("02-search-page.md", "# 02: Search page\nStatus: Ready-for-agent\n"
                    f"Blocked by: 01\nProof: {proof}\n- [ ] Search works\n")
        task = self.imported()["tasks"][1]
        self.assertEqual(task["proof"], proof)
        self.assertEqual(task["ticket_status"], "Ready-for-agent")

    def test_duplicate_fields_never_choose_an_arbitrary_value(self):
        path = self.issues / "02-search-page.md"
        original = path.read_text()
        for field in ("Proof: Another observation", "Status: done", "Blocked by: None"):
            path.write_text(original + "\n" + field + "\n")
            self.imported(1, "repeated")
        path.write_text(original)
        self.imported()

    def test_blocker_order_and_documented_numeric_forms(self):
        for blocked in ("02, 01", "ticket 02; #01", "02 and 01", "02: Search page, 01: Index products"):
            with self.subTest(blocked=blocked):
                self.ticket("03-filter-by-price.md", "# 03: Filter by price\nStatus: ready-for-human\n"
                            f"Blocked by: {blocked}\n- [ ] Results are filtered\n")
                self.assertEqual(self.imported()["tasks"][2]["depends_on"],
                                 ["02-search-page", "01-index-products"])

    def test_numeric_references_cannot_be_shadowed_by_titles(self):
        path = self.issues / "01-index-products.md"
        original = path.read_text()
        for title, blocked in (("02", "02"), ("#02", "#02"), ("ticket 02", "ticket 02"),
                               ("02, 04", "02, 04"), ("02 and 04", "02 and 04"),
                               ("02: Search page", "02: Search page"),
                               ("99", "99"), ("99", "02, 99")):
            with self.subTest(title=title, blocked=blocked):
                path.write_text(original.replace("# 01: Index products", f"# 01: {title}"))
                self.ticket("03-filter-by-price.md", "# 03: Filter by price\nStatus: ready-for-agent\n"
                            f"Blocked by: {blocked}\n- [ ] Results are filtered\n")
                if "99" in blocked:
                    self.imported(1, "cannot resolve blocker '99'")
                else:
                    self.assertEqual(self.imported()["tasks"][2]["depends_on"], ["02-search-page"])

    def test_duplicate_empty_and_partially_consumed_blockers_fail(self):
        for blocked in ("01, 01", "1, 01", "01,,02", "01,", ",01", "01/02", "01 02", "01_", "01: wrong title"):
            with self.subTest(blocked=blocked):
                self.ticket("03-filter-by-price.md", "# 03: Filter by price\nStatus: ready-for-agent\n"
                            f"Blocked by: {blocked}\n- [ ] Results are filtered\n")
                self.imported(1)

    def test_active_cycle_rejects_before_json(self):
        self.ticket("01-index-products.md", "# 01: Index products\nStatus: ready-for-agent\n"
                    "Blocked by: 02\n- [ ] Index works\n")
        self.imported(1, "dependency cycle")

    def test_fenced_examples_do_not_supply_fields(self):
        path = self.issues / "02-search-page.md"
        original = path.read_text()
        fake = "```markdown\nStatus: done\nBlocked by: 99\nProof: Fake\n- [ ] Fake acceptance\n```\n"
        path.write_text(original + "\n" + fake)
        task = self.imported()["tasks"][1]
        self.assertEqual(task["ticket_status"], "ready-for-agent")
        self.assertNotIn("Fake acceptance", task["acceptance"])
        path.write_text("\n".join(line for line in original.splitlines() if not line.startswith("Proof:")) + "\n" + fake)
        self.imported(1, "non-empty 'Proof:'")

    def test_html_comments_do_not_supply_proof_or_other_fields(self):
        path = self.issues / "02-search-page.md"
        original = path.read_text()
        without = "\n".join(line for line in original.splitlines() if not line.startswith("Proof:")) + "\n"
        fake = "<!--\nProof: Open the search page; Lamp is listed\n-->\n"
        path.write_text(without + fake)
        self.imported(1, "non-empty 'Proof:'")
        path.write_text(without + "Proof: <!-- Open the search page; Lamp is listed -->\n")
        self.imported(1, "non-empty 'Proof:'")
        path.write_text(original + "\n<!--\nStatus: done\nBlocked by: 99\nProof: Fake\n"
                        "- [ ] Fake acceptance\n## Comments\n-->\n")
        task = self.imported()["tasks"][1]
        self.assertEqual(task["ticket_status"], "ready-for-agent")
        self.assertEqual(task["depends_on"], ["01-index-products"])
        self.assertEqual(task["proof"], "Open the search page and enter lamp; Lamp is listed")
        self.assertNotIn("Fake acceptance", task["acceptance"])

    def test_literal_comment_markers_in_code_do_not_hide_real_fields(self):
        proof = "Read the template; its literal marker is `<!-- placeholder -->`"
        self.ticket("02-search-page.md", "# 02: Search page\nStatus: ready-for-agent\n"
                    f"Blocked by: 01\nProof: {proof}\n- [ ] Search works\n")
        self.assertEqual(self.imported()["tasks"][1]["proof"], proof)
        path = self.issues / "02-search-page.md"
        path.write_text("```html\n<!--\n```\n" + path.read_text())
        self.assertEqual(self.imported()["tasks"][1]["proof"], proof)

    def test_usage_and_unreadable_input(self):
        empty = self.root / "empty"
        empty.mkdir()
        for arguments in ([], [self.root / "missing"], [empty], ["--unknown"]):
            result = run(IMPORTER, *arguments)
            self.assertEqual(result.returncode, 2, result.stdout + result.stderr)
            self.assertNotIn("Traceback", result.stderr)

    def test_configured_spec_path_and_missing_spec(self):
        spec = self.root / "requirements" / "approved.md"
        spec.parent.mkdir()
        (self.issues.parent / "spec.md").rename(spec)
        before = {p: p.read_bytes() for p in self.root.rglob("*") if p.is_file()}
        missing = run(IMPORTER, self.issues)
        self.assertEqual(missing.returncode, 2)
        self.assertEqual(missing.stdout, "")
        self.assertIn("pass --spec", missing.stderr)
        first = run(IMPORTER, self.issues, "--spec", spec)
        second = run(IMPORTER, self.issues, "--spec", spec)
        self.assertEqual(first.returncode, 0, first.stderr)
        self.assertEqual(first.stdout, second.stdout)
        for task in json.loads(first.stdout)["tasks"]:
            self.assertRegex(task["inputs"][-1], r"^requirements/approved\.md sha256:[0-9a-f]{64}$")
        self.assertEqual({p: p.read_bytes() for p in self.root.rglob("*") if p.is_file()}, before)
        self.ticket("03-filter-by-price.md", "# 03: Bad status\nBlocked by: None\nStatus: unsure\n")
        invalid = run(IMPORTER, self.issues, "--spec", spec)
        self.assertEqual(invalid.returncode, 1)
        self.assertEqual(invalid.stdout, "")
        self.assertIn("status unsure", invalid.stderr)

    def test_outside_scratch_needs_explicit_identity(self):
        other = self.root / "tickets"
        shutil.copytree(self.issues, other)
        result = run(IMPORTER, other, "--spec", self.issues.parent / "spec.md")
        self.assertEqual(result.returncode, 0, result.stderr)
        plan = json.loads(result.stdout)
        self.assertEqual((plan["run_id"], plan["workspace"]), ("{{run id}}", "{{absolute workspace}}"))
        result = run(IMPORTER, other, "--run-id", "search-01", "--workspace", self.root,
                     "--spec", self.issues.parent / "spec.md")
        plan = json.loads(result.stdout)
        self.assertEqual((plan["run_id"], plan["workspace"]), ("search-01", str(self.root)))


if __name__ == "__main__":
    unittest.main()
