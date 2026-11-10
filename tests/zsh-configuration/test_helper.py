"""Controlled startup fixtures, never personal configuration or a real home."""
import json
from pathlib import Path
import shlex
import shutil
import subprocess
import sys
import tempfile
import unittest

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
CHECK = ROOT / "skills/zsh-configuration/scripts/zsh-startup-probe.py"
NAMES = (".zshenv", ".zprofile", ".zshrc", ".zlogin", ".zlogout")


class Startup(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="fixtures-", dir=HERE)
        self.work = Path(self.temp.name)
        self.probe = self.work / "probe"
        self.probe.mkdir()
        for name in ("candidate", "baseline"):
            (self.probe / name).mkdir()
        (self.probe / ".zsh-probe-disposable").write_text("zsh-startup-probe\n")

    def tearDown(self):
        self.temp.cleanup()

    def call(self, *args):
        return subprocess.run([sys.executable, str(CHECK), *map(str, args)],
                              capture_output=True, text=True, cwd=self.work, timeout=20)

    def run_probe(self, *args):
        zsh = shutil.which("zsh")
        if not zsh:
            self.skipTest("Skipped zsh runtime fixture: install zsh to run it.")
        return self.call("--zsh", zsh, "--run", "--disposable-root", self.probe, *args)

    def test_help_and_default_plan_inspect_nothing(self):
        before = sorted(str(p.relative_to(self.work)) for p in self.work.rglob("*"))
        for args in (("--help",), ("--zsh", "/absent/zsh")):
            result = self.call(*args)
            self.assertEqual(result.returncode, 0, result.stderr)
        result = self.call()
        self.assertEqual(json.loads(result.stdout)["shells_executed"], 0)
        self.assertEqual(sorted(str(p.relative_to(self.work)) for p in self.work.rglob("*")), before)

    def test_missing_marker_refuses_before_startup(self):
        (self.probe / ".zsh-probe-disposable").unlink()
        (self.probe / "candidate/.zshenv").write_text(": > \"$TMPDIR/must-not-exist\"\n")
        result = self.run_probe()
        self.assertEqual(result.returncode, 2)
        self.assertEqual(result.stdout, "")
        self.assertFalse((self.probe / "must-not-exist").exists())

    def test_real_modes_order_hashes_and_private_output(self):
        for name in NAMES:
            (self.probe / "candidate" / name).write_text(":\n")
        (self.probe / "candidate/.zprofile").write_text("export PATH=/synthetic-login:$PATH\n")
        (self.probe / "candidate/.zshrc").write_text("setopt shwordsplit\nprintf 'SYNTHETIC_CREDENTIAL'\nprintf 'SYNTHETIC_CREDENTIAL' >&2\n")
        first = self.run_probe()
        self.assertEqual(first.returncode, 0, first.stderr)
        self.assertNotIn("SYNTHETIC_CREDENTIAL", first.stdout + first.stderr)
        self.assertNotIn("/synthetic-login", first.stdout + first.stderr)
        rows = {(r["variant"], r["mode"]): r for r in json.loads(first.stdout)["rows"]}
        expected = {
            "noninteractive": [".zshenv"],
            "login": [".zshenv", ".zprofile", ".zlogin"],
            "interactive": [".zshenv", ".zshrc"],
            "login_interactive": list(NAMES),
        }
        for mode, order in expected.items():
            row = rows["candidate", mode]
            if mode == "login":
                # Noninteractive login exit behavior varies with the runtime;
                # the observed order must still match the startup contract.
                self.assertIn(row["startup_order"], [order, order + [".zlogout"]])
            else:
                self.assertEqual(row["startup_order"], order)
            self.assertEqual(row["protocol_complete"], True)
            same_path = row["path_sha256"] == rows["baseline", mode]["path_sha256"]
            self.assertEqual(same_path, "login" not in mode)
            if "interactive" in mode and mode != "noninteractive":
                self.assertGreater(row["extra_stdout_bytes"], 0)
                self.assertGreater(row["extra_stderr_bytes"], 0)
                self.assertEqual(row["options"]["shwordsplit"], "on")
        again = json.loads(self.run_probe().stdout)["rows"]
        for left, right in zip(json.loads(first.stdout)["rows"], again):
            left.pop("elapsed_ms")
            right.pop("elapsed_ms")
            self.assertEqual(left, right)

    def test_path_diagnostics_preserve_order_without_values(self):
        for name in NAMES:
            (self.probe / "candidate" / name).write_text(":\n")
        (self.probe / "candidate/.zprofile").write_text("export PATH=/synthetic-missing:/synthetic-missing::$PATH\n")
        result = self.run_probe()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertNotIn("/synthetic-missing", result.stdout + result.stderr)
        rows = {(r["variant"],r["mode"]):r for r in json.loads(result.stdout)["rows"]}
        row = rows["candidate","login"]
        self.assertEqual(row["path_entry_sha256"][0], row["path_entry_sha256"][1])
        self.assertGreaterEqual(row["duplicate_path_entries"], 1)
        self.assertEqual(row["empty_path_entries"], 1)
        self.assertGreaterEqual(row["missing_path_entries"], 2)

    def test_relative_path_entries_use_the_observed_shell_directory(self):
        (self.probe / "local-bin").mkdir()
        (self.probe / "child").mkdir()
        (self.probe / "child/local-bin").mkdir()
        (self.work / "parent-only").mkdir()
        startup = self.probe / "candidate/.zshenv"
        for prefix in ("", 'builtin cd "$TMPDIR/child"\n'):
            for entry, missing in (("local-bin", 0), ("parent-only", 1)):
                startup.write_text(prefix + f"export PATH={entry}:/usr/bin:/bin\n")
                result = self.run_probe()
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertNotIn(str(self.probe), result.stdout + result.stderr)
                self.assertNotIn(entry, result.stdout + result.stderr)
                for row in json.loads(result.stdout)["rows"]:
                    if row["variant"] == "candidate":
                        self.assertEqual(row["missing_path_entries"], missing)

    def test_reject_symlink_and_nonempty_baseline(self):
        marker = self.probe / ".zsh-probe-disposable"
        marker.unlink()
        actual = self.probe / "marker"
        actual.write_text("zsh-startup-probe\n")
        marker.symlink_to(actual)
        self.assertEqual(self.run_probe().returncode, 2)
        marker.unlink()
        marker.write_text("zsh-startup-probe\n")
        (self.probe / "baseline/.zshenv").write_text(":\n")
        self.assertEqual(self.run_probe().returncode, 2)

    def test_failed_startup_and_timeout_are_findings(self):
        startup = self.probe / "candidate/.zshenv"
        startup.write_text("exit 9\n")
        result = self.run_probe()
        self.assertEqual(result.returncode, 1)
        rows = json.loads(result.stdout)["rows"]
        self.assertTrue(all(r["exit_code"] == 9 for r in rows if r["variant"] == "candidate"))
        startup.write_text("/bin/sleep 20\n")
        result = self.run_probe("--timeout-seconds", "1")
        self.assertEqual(result.returncode, 1, result.stderr + result.stdout)
        self.assertTrue(all(r["timeout"] for r in json.loads(result.stdout)["rows"] if r["variant"] == "candidate"))

    def test_function_scopes_options_and_preserves_literal(self):
        zsh = shutil.which("zsh")
        if not zsh:
            self.skipTest("Skipped function fixture: install zsh.")
        asset = ROOT / "skills/zsh-configuration/assets/zsh-function.zsh"
        command = ("setopt shwordsplit; source " + shlex.quote(str(asset)) +
                   "; show_literal 'literal * two words'; show_literal >/dev/null 2>&1; rc=$?; "
                   "printf '%s,%s\\n' \"$rc\" \"$options[shwordsplit]\"")
        result = subprocess.run([zsh, "-d", "-f", "-c", command], capture_output=True, text=True, timeout=5)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout, "literal * two words\n2,on\n")


if __name__ == "__main__":
    unittest.main()
