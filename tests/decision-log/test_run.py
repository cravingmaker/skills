"""Accept, reject, and repeat fixtures for the non-destructive scaffolder."""

import subprocess
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
SKILL = HERE.parents[1] / "skills/decision-log"
SCRIPT = SKILL / "scripts/new-run.sh"


class RunTests(unittest.TestCase):
    def run_script(self, *arguments, expected=0, fragment="", cwd=None):
        result = subprocess.run(["sh", str(SCRIPT), *map(str, arguments)], capture_output=True, text=True, cwd=cwd)
        self.assertEqual(result.returncode, expected, result.stdout + result.stderr)
        self.assertIn(fragment, result.stdout + result.stderr)
        return result

    def test_preview_is_read_only(self):
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / "run with spaces"
            self.run_script(target, fragment="PREVIEW")
            self.assertFalse(target.exists())
            self.run_script("--dry-run", target, fragment="PREVIEW")
            self.assertFalse(target.exists())

    def test_apply_scaffold_and_preserve_on_repeat(self):
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / "run with spaces"
            self.run_script("--apply", target, fragment="READY")
            self.assertEqual({p.name for p in target.iterdir()}, {"PLAN.md", "LOG.md", "DECISIONS.md", "raw", "briefs", "drafts"})
            for name in ("PLAN.md", "LOG.md", "DECISIONS.md"):
                self.assertEqual((target / name).read_bytes(), (SKILL / "assets" / name).read_bytes())
                (target / name).write_text(f"Existing completed work: {name}\n")
            (target / "raw/worker-r1.md").write_text("COMPLETE: actual worker result\n")
            (target / "drafts/v1.md").write_text("Frozen first draft\n")
            before = {str(p.relative_to(target)): p.read_bytes() for p in target.rglob("*") if p.is_file()}
            self.run_script("--apply", target, fragment="KEEP")
            self.run_script(target, fragment="PREVIEW")
            after = {str(p.relative_to(target)): p.read_bytes() for p in target.rglob("*") if p.is_file()}
            self.assertEqual(before, after)

    def test_empty_storage_is_not_a_fake_result(self):
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / "run"
            self.run_script("--apply", target)
            for name in ("raw", "briefs", "drafts"):
                self.assertEqual(list((target / name).iterdir()), [])
            self.assertIn('"tasks": []', (target / "PLAN.md").read_text())

    def test_missing_file_is_restored_without_resetting_others(self):
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / "run"
            target.mkdir()
            (target / "PLAN.md").write_text("Existing state\n")
            self.run_script("--apply", target)
            self.assertEqual((target / "PLAN.md").read_text(), "Existing state\n")
            self.assertTrue((target / "LOG.md").is_file())

    def test_root_file_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / "run"
            target.write_text("Keep me")
            self.run_script("--apply", target, expected=1, fragment="select a directory")
            self.assertEqual(target.read_text(), "Keep me")

    def test_late_collision_preflight_has_no_partial_scaffold(self):
        for name in ("raw", "briefs", "drafts", "PLAN.md", "LOG.md", "DECISIONS.md"):
            with self.subTest(name=name), tempfile.TemporaryDirectory() as directory:
                target = Path(directory) / "run"
                target.mkdir()
                collision = target / name
                if name.endswith(".md"):
                    collision.mkdir()
                else:
                    collision.write_text("Keep me")
                self.run_script("--apply", target, expected=1, fragment="FAIL")
                self.assertEqual(list(target.iterdir()), [collision])

    def test_symlinks_are_rejected_and_not_followed(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            outside = root / "outside"
            outside.mkdir()
            (outside / "sentinel").write_text("Keep me")
            target = root / "run"
            target.symlink_to(outside, target_is_directory=True)
            self.run_script("--apply", str(target) + "/", expected=1, fragment="symlink")
            self.assertEqual([p.name for p in outside.iterdir()], ["sentinel"])
        for name in ("raw", "PLAN.md", "DECISIONS.md"):
            with tempfile.TemporaryDirectory() as directory:
                root = Path(directory)
                target = root / "run"
                target.mkdir()
                sentinel = root / "sentinel"
                sentinel.write_text("Keep me")
                (target / name).symlink_to(sentinel)
                self.run_script("--apply", target, expected=1, fragment="symlink")
                self.assertEqual(sentinel.read_text(), "Keep me")
                self.assertEqual([p.name for p in target.iterdir()], [name])

    def test_relative_path_and_help_usage(self):
        with tempfile.TemporaryDirectory() as directory:
            self.run_script("--apply", "relative run", cwd=directory)
            self.assertTrue((Path(directory) / "relative run/PLAN.md").is_file())
        self.run_script("--help", fragment="usage")
        for arguments in ((), ("",), ("--apply",), ("--unknown",), ("one", "two")):
            self.run_script(*arguments, expected=2, fragment="usage")


if __name__ == "__main__":
    unittest.main()
