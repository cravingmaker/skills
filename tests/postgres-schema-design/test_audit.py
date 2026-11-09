"""Scoped audit rejects bad catalogs, accepts good ones, and withholds raw errors."""
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import time
import unittest

ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "skills/postgres-schema-design/scripts/audit-schema.py"


class OfflineAudit(unittest.TestCase):
    def setUp(self):
        self.work = tempfile.TemporaryDirectory(prefix="audit-test-")
        self.addCleanup(self.work.cleanup)
        self.root = Path(self.work.name)
        self.fake = self.root / "psql"
        self.fake.write_text("#!/bin/sh\nprintf '%s\\n' \"$FAKE_DATA\"\nprintf '%s\\n' DO_NOT_ECHO >&2\nexit \"${FAKE_EXIT:-0}\"\n".replace('\\"', '"'))
        self.fake.chmod(0o755)

    def run_check(self, *args, code="0", data=None):
        env = os.environ | {"PATH": str(self.root), "FAKE_EXIT": code,
                            "FAKE_DATA": json.dumps(data or {"objects_scanned": 1, "findings": []})}
        return subprocess.run([sys.executable, str(SCRIPT), *args], env=env, capture_output=True, text=True)

    def test_help_usage_and_hidden_errors(self):
        self.assertEqual(self.run_check("--help").returncode, 0)
        for args in ((), ("--schema", ""), ("--schema", "x", "--tenant-column", ""),
                     ("--unknown", "postgres://DO_NOT_ECHO")):
            result = self.run_check(*args)
            self.assertEqual(result.returncode, 2)
            self.assertNotIn("DO_NOT_ECHO", result.stdout + result.stderr)
        for code in ("1", "2", "3"):
            result = self.run_check("--schema", "app", code=code)
            self.assertEqual(result.returncode, 2)
            self.assertNotIn("DO_NOT_ECHO", result.stdout + result.stderr)

    def test_accept_reject_repeat_and_no_writes(self):
        before = self.fake.read_bytes()
        first = self.run_check("--schema", "app")
        second = self.run_check("--schema", "app")
        self.assertEqual(first.returncode, 0, first.stderr)
        self.assertEqual(first.stdout, second.stdout)
        self.assertEqual(before, self.fake.read_bytes())
        self.assertNotIn("DO_NOT_ECHO", first.stdout + first.stderr)
        for data in ({"objects_scanned": 1, "findings": [{"check": "fixture"}]},
                     {"objects_scanned": 0, "findings": []}):
            self.assertEqual(self.run_check("--schema", "app", data=data).returncode, 1)


@unittest.skipUnless(os.environ.get("SKILL_TEST_PG") == "owned", "native suite requires its owned cluster")
class NativeAudit(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.psql((Path(__file__).parent / "catalog-fixture.sql").read_text())
        result = cls.psql("CREATE UNIQUE INDEX CONCURRENTLY invalid_cover ON bad.invalid_fk (tenant_id, account_id);", check=False)
        if result.returncode == 0:
            raise AssertionError("duplicate concurrent index fixture must leave an invalid index")
        invalid = cls.psql("SELECT indisvalid FROM pg_index WHERE indexrelid = 'bad.invalid_cover'::regclass;")
        if invalid.stdout.strip() != "f":
            raise AssertionError("fixture did not produce an invalid index")
        # Hold an old snapshot so the concurrent build waits after becoming ready.
        # Cancellation there leaves the real ready-but-invalid artifact the audit must reject.
        reader = subprocess.Popen(["psql", "-X", "-w", "-q", "-A", "-t", "-v", "ON_ERROR_STOP=1"],
                                  stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        builder = None
        try:
            reader.stdin.write('BEGIN ISOLATION LEVEL REPEATABLE READ; SELECT id FROM bad.ready_fk;\n\\echo snapshot-ready\n')
            reader.stdin.flush()
            if reader.stdout.readline().strip() != "1" or reader.stdout.readline().strip() != "snapshot-ready":
                raise AssertionError("snapshot barrier failed")
            builder = subprocess.Popen(["psql", "-X", "-w", "-q", "-v", "ON_ERROR_STOP=1", "-c",
                                        "CREATE INDEX CONCURRENTLY invalid_ready_cover ON bad.ready_fk (tenant_id, account_id)"],
                                       env=os.environ | {"PGAPPNAME": "fixture-index-build"},
                                       stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            deadline = time.monotonic() + 5
            while True:
                state = cls.psql("SELECT indisready::text || ',' || indisvalid::text FROM pg_index WHERE indexrelid = to_regclass('bad.invalid_ready_cover');").stdout.strip()
                if state == "true,false":
                    break
                if time.monotonic() >= deadline or builder.poll() is not None:
                    raise AssertionError("concurrent build never reached its ready/invalid barrier")
                time.sleep(0.02)
            cls.psql("SELECT pg_cancel_backend(pid) FROM pg_stat_activity WHERE application_name = 'fixture-index-build';")
            builder.communicate(timeout=5)
            if builder.returncode == 0:
                raise AssertionError("concurrent index cancellation did not occur")
        finally:
            reader.communicate("ROLLBACK;\n", timeout=5)
            if builder is not None and builder.poll() is None:
                builder.communicate(timeout=5)
        state = cls.psql("SELECT indisready::text || ',' || indisvalid::text FROM pg_index WHERE indexrelid = 'bad.invalid_ready_cover'::regclass;").stdout.strip()
        if state != "true,false":
            raise AssertionError("fixture did not retain its ready-but-invalid index")

    @staticmethod
    def psql(sql, check=True):
        return subprocess.run(["psql", "-X", "-w", "-q", "-A", "-t", "-v", "ON_ERROR_STOP=1"],
                              input=sql, capture_output=True, text=True, check=check)

    def audit(self, schema):
        result = subprocess.run([sys.executable, str(SCRIPT), "--schema", schema], capture_output=True, text=True)
        return result, json.loads(result.stdout)

    def test_bad_schema_and_false_index_coverage(self):
        result, data = self.audit("bad")
        self.assertEqual(result.returncode, 1, result.stderr)
        findings = {(row["check"], row["object"]) for row in data["findings"]}
        expected = {("fk-without-index", "bad.payment.payment_account_id_tenant_id_fkey"),
                    ("fk-without-index", "bad.included.included_tenant_id_account_id_fkey"),
                    ("fk-without-index", "bad.invalid_fk.invalid_fk_tenant_id_account_id_fkey"),
                    ("fk-without-index", "bad.ready_fk.ready_fk_tenant_id_account_id_fkey"),
                    ("tenant-missing-from-fk", "bad.wrong_pair.wrong_pair_tenant_id_account_id_fkey"),
                    ("table-without-primary-key", "bad.log_line"),
                    ("column-review", "bad.payment.balance"), ("column-review", "bad.payment.opened_at")}
        self.assertTrue(expected <= findings, expected - findings)
        self.assertFalse(any(check == "tenant-missing-from-fk" and "bad.payment." in name for check, name in findings))

    def test_good_schema_repeat_and_empty_scope(self):
        first, data = self.audit("good")
        second, repeated = self.audit("good")
        self.assertEqual(first.returncode, 0, first.stderr)
        self.assertEqual(data, repeated)
        self.assertEqual(second.returncode, 0)
        self.assertEqual(data["findings"], [])
        empty, data = self.audit("missing")
        self.assertEqual(empty.returncode, 1)
        self.assertEqual(data["findings"][0]["check"], "empty-scope")


if __name__ == "__main__":
    unittest.main()
