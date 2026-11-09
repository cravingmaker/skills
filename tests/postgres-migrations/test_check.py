"""Test wrapper delegation and failure handling; fake lint is not Squawk proof."""
import os
import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "skills/postgres-migrations/scripts/check-migration.sh"


class WrapperTests(unittest.TestCase):
    def setUp(self):
        self.work = tempfile.TemporaryDirectory(prefix="migration-lint-test-")
        self.addCleanup(self.work.cleanup)
        self.root = Path(self.work.name)
        self.sql = self.root / "migration with spaces.sql"
        self.sql.write_text("SELECT 1;\n")
        self.fake = self.root / "pinned-squawk"
        self.fake.write_text('''#!/bin/sh
if [ "$#" -ne 1 ] || [ ! -f "$1" ]; then exit 7; fi
printf '%s\\n' 'native lint output DO_NOT_ECHO'
printf '%s\\n' 'native error DO_NOT_ECHO' >&2
exit "${FAKE_LINT_STATUS:-0}"
''')
        self.fake.chmod(0o755)

    def run_check(self, *args, status="0"):
        return subprocess.run(["sh", str(SCRIPT), *map(str, args)], capture_output=True, text=True,
                              env={"PATH": os.environ["PATH"], "FAKE_LINT_STATUS": status})

    def test_help_without_tool_or_input(self):
        result = self.run_check("--help")
        self.assertEqual(result.returncode, 0)
        self.assertIn("Lint only", result.stdout)

    def test_accept_repeat_argument_boundaries_and_no_write(self):
        before = {p.name: p.read_bytes() for p in self.root.iterdir()}
        args = ("--squawk", self.fake, "--", self.sql)
        first, second = self.run_check(*args), self.run_check(*args)
        self.assertEqual(first.returncode, 0, first.stderr)
        self.assertEqual(first.stdout, '{"ok":true,"tool":"squawk"}\n')
        self.assertNotIn("DO_NOT_ECHO", first.stdout + first.stderr)
        self.assertEqual(second.stdout, first.stdout)
        self.assertEqual({p.name: p.read_bytes() for p in self.root.iterdir()}, before)

    def test_lint_and_setup_failure_are_distinct(self):
        args = ("--squawk", self.fake, "--", self.sql)
        for native, expected in (("1", 1), ("9", 2)):
            result = self.run_check(*args, status=native)
            self.assertEqual(result.returncode, expected)
            self.assertIn('"ok":false', result.stdout)
            self.assertNotIn("DO_NOT_ECHO", result.stdout + result.stderr)
            self.assertIn("error:", result.stderr)

    def test_bad_inputs_do_not_reach_linter_or_echo_secrets(self):
        for args in ((), ("--squawk", self.fake, "--"),
                     ("--squawk", self.root / "missing", "--", self.sql),
                     ("--squawk", self.fake, "--", "missing.sql"),
                     ("--squawk", self.fake, "--", "postgres://DO_NOT_ECHO@example/db"),
                     ("--squawk", self.fake, "--", "--version")):
            result = self.run_check(*args)
            self.assertEqual(result.returncode, 2)
            self.assertNotIn("native lint output", result.stdout)
            self.assertNotIn("DO_NOT_ECHO", result.stderr + result.stdout)


if __name__ == "__main__":
    unittest.main()
