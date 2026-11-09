#!/usr/bin/env python3
"""Offline CLI fixtures for ADR history, links, and existing record forms."""

import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
SCRIPT = HERE.parents[1] / "skills/architecture-decisions/scripts/check-adr.py"
ENV = dict(os.environ, GIT_CONFIG_GLOBAL="/dev/null", GIT_CONFIG_SYSTEM="/dev/null",
           GIT_AUTHOR_NAME="Fixture", GIT_AUTHOR_EMAIL="fixture@example.invalid",
           GIT_COMMITTER_NAME="Fixture", GIT_COMMITTER_EMAIL="fixture@example.invalid")


class ADRTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="adr-fixture-")
        self.root = Path(self.temp.name)
        self.adr = self.root / "docs/adr"
        shutil.copytree(HERE / "fixtures/valid", self.adr)

    def tearDown(self):
        self.temp.cleanup()

    def run_cli(self, *args, expected=0):
        before = {path.relative_to(self.adr): path.read_bytes() for path in self.adr.rglob("*") if path.is_file()}
        result = subprocess.run([sys.executable, str(SCRIPT), str(self.adr), *args],
                                cwd=self.root, env=ENV, capture_output=True, text=True)
        self.assertEqual(result.returncode, expected, (result.stdout, result.stderr))
        after = {path.relative_to(self.adr): path.read_bytes() for path in self.adr.rglob("*") if path.is_file()}
        self.assertEqual(before, after, "the checker must not rewrite records")
        if expected == 2:
            self.assertEqual(result.stdout, "")
            self.assertIn("error:", result.stderr)
            self.assertNotIn("Traceback", result.stderr)
            return result
        self.assertEqual(result.stderr, "")
        return json.loads(result.stdout)

    def git(self, *args):
        result = subprocess.run(["git", "-C", str(self.root), *args], env=ENV, capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        return result.stdout.strip()

    def base(self):
        self.git("init", "--quiet")
        self.git("add", "docs")
        self.git("-c", "commit.gpgsign=false", "commit", "--quiet", "-m", "Disposable fixture history")
        return self.git("rev-parse", "HEAD")

    def test_existing_formats_and_repeat(self):
        first = self.run_cli()
        self.assertEqual(first, self.run_cli())
        self.assertEqual(first["scanned"], 3)
        self.assertEqual([row["status"] for row in first["records"]], ["accepted", "proposed", "recorded"])

    def test_confirmation_is_opt_in_and_not_execution_proof(self):
        data = self.run_cli("--require-confirmation", expected=1)
        self.assertEqual(len(data["findings"]), 1)
        self.assertIn("0003-short", data["findings"][0])
        self.assertTrue(data["records"][1]["confirmation"])

    def test_null_confirmation_does_not_satisfy_required_evidence(self):
        for value in ("null", "~", "TBD", "TODO", "N/A", "none", "...", "<check>"):
            path = self.adr / "0003-short.md"
            path.write_text(f"---\nconfirmation: {value}\n---\n# Keep receipts\n\nKeep source receipts.\n")
            data = self.run_cli("--require-confirmation", expected=1)
            self.assertFalse(data["records"][2]["confirmation"])

    def test_placeholder_and_comment_only_confirmation_sections(self):
        path = self.adr / "0003-short.md"
        for contents in ("- TBD", "-", "<!-- evidence to follow -->", ""):
            path.write_text("# Keep receipts\n\nKeep source receipts.\n\n## Confirmation\n\n" + contents + "\n")
            data = self.run_cli("--require-confirmation", expected=1)
            self.assertFalse(data["records"][2]["confirmation"])
        path.write_text("# Keep receipts\n\nKeep source receipts.\n\n## Confirmation\n\nReadback fixture passes locally.\n")
        self.run_cli("--require-confirmation")

    def test_reasoning_edit_and_deletion_fail(self):
        base = self.base()
        path = self.adr / "0001-store.md"
        original = path.read_text()
        path.write_text(original.replace("owns canonical writes", "shares canonical writes"))
        self.assertTrue(any("reasoning changed" in issue for issue in self.run_cli("--base", base, expected=1)["findings"]))
        path.write_text(original)
        self.run_cli("--base", base)
        path.unlink()
        self.run_cli("--base", base, expected=1)

    def test_proposed_successor_does_not_replace_accepted_predecessor(self):
        base = self.base()
        (self.adr / "0004-next.md").write_text(
            "# Proposed writer\n\nStatus: proposed\nSupersedes: ADR-0001\n\nPending owner review.\n")
        data = self.run_cli("--base", base)
        self.assertEqual(data["records"][0]["status"], "accepted")
        self.assertEqual(data["records"][-1]["status"], "proposed")
        path = self.adr / "0001-store.md"
        path.write_text(path.read_text().replace("status: accepted", "status: superseded by ADR-0004"))
        self.assertTrue(any("proposed or rejected successor" in issue
                            for issue in self.run_cli("--base", base, expected=1)["findings"]))

    def test_new_accepted_file_needs_explicit_signoff_acknowledgement(self):
        base = self.base()
        (self.adr / "0004-next.md").write_text("# New choice\n\nStatus: accepted\n\nUse one writer.\n")
        self.assertTrue(any("new acceptance" in issue
                            for issue in self.run_cli("--base", base, expected=1)["findings"]))
        self.run_cli("--base", base, "--signed-off", "4")

    def test_accepting_an_existing_proposal_also_needs_signoff(self):
        base = self.base()
        path = self.adr / "0002-runtime.md"
        path.write_text(path.read_text().replace("Proposed", "Accepted"))
        self.run_cli("--base", base, expected=1)
        self.run_cli("--base", base, "--signed-off", "2")

    def test_multiple_acceptances_require_each_acknowledgement(self):
        base = self.base()
        for number in (4, 5):
            (self.adr / f"{number:04d}-new.md").write_text("# New choice\n\nStatus: accepted\n\nOwned choice.\n")
        self.run_cli("--base", base, "--signed-off", "4", expected=1)
        self.run_cli("--base", base, "--signed-off", "4", "--signed-off", "5")

    def test_signoff_requires_history_and_valid_number(self):
        self.run_cli("--signed-off", "2", expected=2)
        self.run_cli("--base", self.base(), "--signed-off", "-1", expected=2)

    def test_statusless_record_is_protected(self):
        base = self.base()
        path = self.adr / "0003-short.md"
        path.write_text(path.read_text().replace("raw receipts", "rounded receipts"))
        self.run_cli("--base", base, expected=1)

    def test_proposed_reasoning_can_change(self):
        base = self.base()
        path = self.adr / "0002-runtime.md"
        path.write_text(path.read_text().replace("pending the shutdown trial", "until the retry trial"))
        self.run_cli("--base", base)

    def test_lifecycle_only_and_reciprocal_supersession_pass(self):
        base = self.base()
        path = self.adr / "0001-store.md"
        path.write_text(path.read_text().replace("status: accepted", "status: superseded\nsuperseded-by: '[next](0004-next.md)'"))
        (self.adr / "0004-next.md").write_text(
            "# New writer\n\nStatus: accepted\nSupersedes: [old](0001-store.md)\n\nThe owner accepted the new writer.\n")
        self.run_cli("--base", base, expected=1)
        self.run_cli("--base", base, "--signed-off", "4")

    def test_accepted_status_cannot_be_erased(self):
        base = self.base()
        path = self.adr / "0001-store.md"
        path.write_text(path.read_text().replace("status: accepted", "status: proposed"))
        self.run_cli("--base", base, expected=1)

    def test_unclosed_frontmatter_is_invalid_input(self):
        (self.adr / "0001-store.md").write_text("---\nstatus: accepted\n# No closing delimiter\n")
        self.run_cli(expected=2)

    def test_missing_reciprocal_and_escape_fail(self):
        path = self.adr / "0001-store.md"
        original = path.read_text()
        path.write_text(original.replace("status: accepted", "status: superseded by ADR-0002"))
        self.assertTrue(any("reciprocal" in item for item in self.run_cli(expected=1)["findings"]))
        path.write_text(original.replace("status: accepted", "status: superseded\nsuperseded-by: '[out](../../outside.md)'"))
        self.assertTrue(any("inside" in item for item in self.run_cli(expected=1)["findings"]))

    def test_number_collision_and_missing_target_fail(self):
        shutil.copyfile(self.adr / "0001-store.md", self.adr / "01-collision.md")
        self.assertTrue(any("unique number" in item for item in self.run_cli(expected=1)["findings"]))
        (self.adr / "01-collision.md").unlink()
        path = self.adr / "0001-store.md"
        path.write_text(path.read_text().replace("status: accepted", "status: superseded by ADR-0099"))
        self.run_cli(expected=1)

    def test_cycle_and_conflicting_status_fail(self):
        for number, other in (("0001", "0002"), ("0002", "0001")):
            (self.adr / f"{number}-cycle.md").write_text(
                f"# Cycle\nStatus: superseded by ADR-{other}\nSupersedes: ADR-{other}\n")
        (self.adr / "0001-store.md").unlink()
        (self.adr / "0002-runtime.md").unlink()
        self.assertTrue(any("cycle" in item for item in self.run_cli(expected=1)["findings"]))
        (self.adr / "0001-cycle.md").write_text("# Status conflict\nStatus: accepted\n\n## Status\nProposed\n")
        self.run_cli(expected=1)

    def test_fenced_status_text_is_reasoning(self):
        base = self.base()
        path = self.adr / "0001-store.md"
        path.write_text(path.read_text() + "\n" + chr(96) * 3 + "\nStatus: proposed\n" + chr(96) * 3 + "\n")
        self.run_cli("--base", base, expected=1)

    def test_empty_malformed_and_invalid_base(self):
        self.run_cli("--base", "not-a-commit", expected=2)
        for path in self.adr.iterdir():
            path.unlink()
        self.run_cli(expected=1)
        (self.adr / "0001-invalid.md").write_bytes(b"\xff")
        self.run_cli(expected=2)

    def test_help_has_no_effect(self):
        empty = self.root / "help-only"
        empty.mkdir()
        result = subprocess.run([sys.executable, str(SCRIPT), "--help"], cwd=empty, capture_output=True, text=True)
        self.assertEqual(result.returncode, 0)
        self.assertIn("Exits:", result.stdout)
        self.assertEqual(result.stderr, "")
        self.assertEqual(list(empty.iterdir()), [])


if __name__ == "__main__":
    unittest.main()
