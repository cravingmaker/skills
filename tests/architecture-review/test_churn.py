#!/usr/bin/env python3
"""Create disposable Git history; no user config, signing, or network."""

import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
SCRIPT = HERE.parents[1] / "skills/architecture-review/scripts/churn-hotspots.py"
ENV = dict(os.environ, GIT_CONFIG_GLOBAL="/dev/null", GIT_CONFIG_SYSTEM="/dev/null",
           GIT_AUTHOR_NAME="Fixture", GIT_AUTHOR_EMAIL="fixture@example.invalid",
           GIT_COMMITTER_NAME="Fixture", GIT_COMMITTER_EMAIL="fixture@example.invalid",
           GIT_AUTHOR_DATE="2001-01-01T00:00:00Z", GIT_COMMITTER_DATE="2001-01-01T00:00:00Z")


class ChurnTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="churn-fixture-")
        self.root = Path(self.temp.name)
        self.git("init", "--quiet")
        (self.root / "small.txt").write_bytes(b"a\nb\n")
        (self.root / "large.txt").write_bytes(b"BODY-MUST-NOT-APPEAR\n" * 3)
        (self.root / "binary.dat").write_bytes(b"\0binary")
        (self.root / "gone.txt").write_text("removed\n")
        self.odd = "tab\tand\nnewline.txt"
        (self.root / self.odd).write_bytes(b"odd\n")
        (self.root / "link").symlink_to("small.txt")
        self.commit()
        (self.root / "small.txt").write_bytes(b"a\nc\n")
        (self.root / "gone.txt").unlink()
        self.commit()
        self.sha = self.git("rev-parse", "HEAD")

    def tearDown(self):
        self.temp.cleanup()

    def git(self, *args):
        result = subprocess.run(["git", "-C", str(self.root), *args], env=ENV, capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        return result.stdout.strip()

    def commit(self):
        self.git("add", "-A")
        self.git("-c", "commit.gpgsign=false", "commit", "--quiet", "-m", "Disposable fixture")

    def run_cli(self, *args, expected=0):
        result = subprocess.run([sys.executable, str(SCRIPT), "--repo", str(self.root),
                                 "--since", "2000-01-01", *args], env=ENV, capture_output=True, text=True)
        self.assertEqual(result.returncode, expected, (result.stdout, result.stderr))
        self.assertNotIn("BODY-MUST-NOT-APPEAR", result.stdout)
        if expected == 2:
            self.assertEqual(result.stdout, "")
            self.assertNotIn("Traceback", result.stderr)
            return
        self.assertEqual(result.stderr, "")
        return json.loads(result.stdout)

    def test_counts_scores_and_repeat(self):
        data = self.run_cli()
        self.assertEqual(data, self.run_cli())
        self.assertEqual(data["revision"], self.sha)
        rows = {row["path"]: row for row in data["files"]}
        self.assertEqual(rows["small.txt"]["added"], 3)
        self.assertEqual(rows["small.txt"]["deleted"], 1)
        self.assertEqual(rows["small.txt"]["size_bytes"], 4)
        self.assertEqual(rows["small.txt"]["score"], 16)
        self.assertEqual(rows[self.odd]["churn_lines"], 1)
        self.assertEqual(data["files"][0]["path"], "large.txt")
        self.assertNotIn("binary.dat", rows)
        self.assertNotIn("gone.txt", rows)
        self.assertNotIn("link", rows)

    def test_dirty_and_untracked_files_do_not_change_result(self):
        before = self.run_cli()
        (self.root / "small.txt").write_bytes(b"changed" * 100)
        (self.root / "untracked.txt").write_text("untracked\n")
        self.assertEqual(before, self.run_cli())
        self.assertEqual(len(self.run_cli("--limit", "1")["files"]), 1)

    def test_ref_and_empty_window(self):
        self.run_cli("--rev", self.sha)
        self.assertEqual(self.run_cli("--since", "2999-01-01", expected=1)["files"], [])
        self.run_cli("--rev", "not-a-commit", expected=2)
        self.run_cli("--limit", "0", expected=2)
        self.run_cli("--since", "", expected=2)

    def test_rename_uses_new_path_without_following(self):
        (self.root / "small.txt").rename(self.root / "renamed.txt")
        self.commit()
        rows = {row["path"]: row for row in self.run_cli()["files"]}
        self.assertNotIn("small.txt", rows)
        self.assertEqual(rows["renamed.txt"]["churn_lines"], 2)

    def test_lockfiles_generated_outputs_and_explicit_exclusions(self):
        for name in ("pnpm-lock.yaml", "Cargo.lock", "bundle.min.js", "styles.min.css", "data.snap", "bundle.js.map"):
            (self.root / name).write_text("generated\n" * 1000)
        (self.root / "src").mkdir()
        (self.root / "src/generated.txt").write_text("generated source\n" * 1000)
        self.commit()
        data = self.run_cli()
        names = {row["path"] for row in data["files"]}
        self.assertFalse(any(name in names for name in ("pnpm-lock.yaml", "Cargo.lock", "bundle.min.js", "styles.min.css", "data.snap", "bundle.js.map")))
        self.assertIn("src/generated.txt", names)
        filtered = self.run_cli("--exclude", "src/generated.*", "--exclude", "small.txt")
        self.assertNotIn("src/generated.txt", {row["path"] for row in filtered["files"]})
        self.assertNotIn("small.txt", {row["path"] for row in filtered["files"]})
        self.assertIn("src/generated.*", filtered["exclusions"])

    def test_help_is_read_only(self):
        result = subprocess.run([sys.executable, str(SCRIPT), "--help"], cwd=self.root,
                                capture_output=True, text=True)
        self.assertEqual(result.returncode, 0)
        self.assertIn("Exits:", result.stdout)
        self.assertEqual(result.stderr, "")
        self.assertEqual(self.git("rev-parse", "HEAD"), self.sha)


if __name__ == "__main__":
    unittest.main()
