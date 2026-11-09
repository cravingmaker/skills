"""Offline candidate scan; endpoint compatibility still needs the real transport."""
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
SCRIPT = HERE.parents[1] / "skills/postgres-connection-pooling/scripts/find-session-features.py"


class SessionTests(unittest.TestCase):
    def scan(self, *paths, code=0):
        results = [subprocess.run([sys.executable, str(SCRIPT), *map(str, paths)],
                                  capture_output=True, text=True) for _ in range(2)]
        self.assertEqual(results[0].stdout, results[1].stdout)
        self.assertEqual(results[0].stderr, results[1].stderr)
        for result in results:
            self.assertEqual(result.returncode, code, result.stdout + result.stderr)
            self.assertNotIn("Traceback", result.stderr)
            self.assertNotIn("SECRET_SENTINEL", result.stdout + result.stderr)
        return results[0]

    def test_pooled_candidates_and_transaction_local_acceptance(self):
        result = self.scan(HERE / "fixtures/pooled", code=1)
        lines = result.stdout.splitlines()
        self.assertEqual(len(lines), 12)
        for expected in ("session SET", "session set_config", "LISTEN", "session advisory lock",
                         "SQL PREPARE", "cursor WITH HOLD", "temporary table", "RESET", "LOAD"):
            self.assertTrue(any(expected in line for line in lines), expected)
        self.assertEqual(self.scan(HERE / "fixtures/clean").stdout, "")

    def test_suppression_needs_reason_and_session_defaults_are_candidates(self):
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / "pooled.ts"
            path.write_text('client.query("SET search_path TO app"); // pooler-ok:\n'
                            'client.query("SET SESSION CHARACTERISTICS AS TRANSACTION READ ONLY");\n'
                            '// SECRET_SENTINEL\n')
            before = path.read_bytes()
            self.assertEqual(len(self.scan(path, code=1).stdout.splitlines()), 2)
            self.assertEqual(path.read_bytes(), before)
            path.write_text("SET search_path TO app; -- pooler-ok: reviewed direct-only module\n")
            self.assertEqual(self.scan(path).stdout, "")

    def test_empty_missing_scope_and_inert_help(self):
        with tempfile.TemporaryDirectory() as temporary:
            work = Path(temporary)
            result = self.scan(work, code=2)
            self.assertIn("no files scanned", result.stderr)
            self.scan(work / "missing", code=2)
            self.assertIn("Usage", self.scan("--help").stdout)
            self.scan(code=2)
            self.assertEqual(list(work.iterdir()), [])


if __name__ == "__main__":
    unittest.main()
