"""Offline native-parser fixtures; all scratch writes stay under this test folder."""
import json
import os
from pathlib import Path
import shlex
import shutil
import subprocess
import sys
import tempfile
import unittest

HERE = Path(__file__).resolve().parent
CHECK = HERE.parents[1] / "skills/shell-scripting/scripts/check-shell.py"


class ShellCheck(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="fixtures-", dir=HERE)
        self.work = Path(self.temp.name)

    def tearDown(self):
        self.temp.cleanup()

    def call(self, *args, env=None):
        return subprocess.run([sys.executable, str(CHECK), *map(str, args)],
                              capture_output=True, text=True, cwd=self.work, env=env, timeout=15)

    def check(self, dialect, path, **kwargs):
        shell = shutil.which(dialect)
        if not shell:
            self.skipTest(f"Skipped native {dialect} fixture: install {dialect} to run it.")
        return self.call("--dialect", dialect, "--interpreter", shell, path, **kwargs)

    def test_help_has_no_effect(self):
        result = self.call("--help")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("Exit:", result.stdout)
        self.assertEqual(list(self.work.iterdir()), [])

    def test_real_parsers_accept_repeat_without_execution_or_output_leak(self):
        for dialect in ("sh", "bash", "zsh"):
            with self.subTest(dialect=dialect):
                path = self.work / ("- space\tnewline\n" + dialect)
                sentinel = self.work / "must-not-exist"
                path.write_text(f"#!/bin/{dialect}\nprintf 'SYNTHETIC_CREDENTIAL\\n'\n: > {shlex.quote(str(sentinel))}\n")
                before = path.read_bytes()
                first = self.check(dialect, path)
                second = self.check(dialect, path)
                self.assertEqual(first.returncode, 0, first.stderr)
                self.assertEqual(first.stdout, second.stdout)
                self.assertEqual(path.read_bytes(), before)
                self.assertFalse(sentinel.exists())
                self.assertNotIn("SYNTHETIC_CREDENTIAL", first.stdout + first.stderr)
                self.assertEqual(json.loads(first.stdout)["scope"], "native_syntax_only")

    def test_syntax_failure_does_not_echo_source(self):
        path = self.work / "bad"
        path.write_text("#!/bin/bash\nif ; then\nSYNTHETIC_CREDENTIAL\n")
        result = self.check("bash", path)
        self.assertEqual(result.returncode, 1)
        self.assertEqual(json.loads(result.stdout)["findings"][0]["code"], "syntax_failed")
        self.assertNotIn("SYNTHETIC_CREDENTIAL", result.stdout + result.stderr)

    def test_dialect_mismatch_and_missing_shebang(self):
        path = self.work / "mismatch"
        for content in ("#!/bin/sh\nitems=(one two)\n", "printf 'hello\\n'\n"):
            path.write_text(content)
            result = self.check("bash", path)
            self.assertEqual(result.returncode, 1)
            self.assertEqual(json.loads(result.stdout)["files"], [])
            self.assertIn("shebang_dialect_mismatch", result.stdout)

    def test_env_shebang_and_startup_environment_is_not_inherited(self):
        path, startup, sentinel = self.work / "env-script", self.work / "startup", self.work / "startup-sentinel"
        path.write_text("#!/usr/bin/env -S bash -eu\nprintf '%s\\n' ok\n")
        startup.write_text(f": > {shlex.quote(str(sentinel))}\n")
        env = dict(os.environ, BASH_ENV=str(startup), ENV=str(startup))
        result = self.check("bash", path, env=env)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertFalse(sentinel.exists())

    def test_syntax_pass_does_not_claim_failure_semantics(self):
        path = self.work / "masked-failure"
        path.write_text("#!/bin/bash\nset -e\nf() { false; printf continued; }\nif f; then :; fi\n")
        result = self.check("bash", path)
        self.assertEqual(result.returncode, 0)
        self.assertEqual(json.loads(result.stdout)["scope"], "native_syntax_only")

    def test_bad_input_and_missing_interpreter(self):
        for path in (self.work, self.work / "absent"):
            result = self.check("sh", path)
            self.assertEqual(result.returncode, 2)
            self.assertEqual(result.stdout, "")
        result = self.call("--dialect", "sh", "--interpreter", "/absent/interpreter", "absent")
        self.assertEqual(result.returncode, 2)
        self.assertEqual(self.call().returncode, 2)

    def test_non_shell_interpreter_refused(self):
        path = self.work / "bad"
        path.write_text("#!/bin/bash\nif ; then\n")
        non_shell = shutil.which("true")
        self.assertEqual(self.call("--dialect", "bash", "--interpreter", non_shell, path).returncode, 2)

    def test_bash_comparison_asset_help_usage_failure_and_repeat(self):
        asset = HERE.parents[1] / "skills/shell-scripting/assets/template.bash"
        bash = shutil.which("bash")
        if not bash:
            self.skipTest("Install bash to check the Bash starter")
        def invoke(*args, env=None):
            return subprocess.run([bash, str(asset), *map(str, args)], cwd=self.work,
                                  env=env, text=True, capture_output=True, timeout=5)
        before = set(self.work.iterdir())
        self.assertEqual(invoke("--help").returncode, 0)
        self.assertEqual(set(self.work.iterdir()), before)
        self.assertEqual(invoke().returncode, 2)
        self.assertEqual(invoke("--disposable-dir", self.work / "absent").returncode, 2)
        for _ in range(2):
            result = invoke("--disposable-dir", self.work)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(result.stdout, "No operation configured.\n")
            self.assertEqual(set(self.work.iterdir()), before)
        bindir = self.work / "stub-bin"
        bindir.mkdir()
        failing = bindir / "mktemp"
        failing.write_text("#!/bin/sh\nexit 7\n")
        failing.chmod(0o755)
        result = invoke("--disposable-dir", self.work, env={"PATH": str(bindir), "LC_ALL": "C"})
        self.assertEqual(result.returncode, 1)
        self.assertEqual(result.stdout, "")


if __name__ == "__main__":
    unittest.main()
