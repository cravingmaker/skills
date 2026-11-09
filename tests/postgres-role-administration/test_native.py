"""Actual-login, native reachability and real-creator tests on an owned cluster."""
import copy
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[2]
SKILL = ROOT / "skills/postgres-role-administration"


def sql(statement, login="fixture", check=True):
    return subprocess.run(["psql", "-X", "-w", "-q", "-A", "-t", "-v", "ON_ERROR_STOP=1", "-v", "VERBOSITY=sqlstate"],
                          input=statement, env=os.environ | {"PGUSER": login}, capture_output=True, text=True, check=check)


def audit():
    result = subprocess.run(["psql", "-X", "-w", "-q", "-A", "-t", "-F", "\t", "-v", "ON_ERROR_STOP=1",
                             "-v", "role=fixture_reader", "-v", "schema=fixture_app",
                             "-f", str(SKILL / "references/privilege-audit.sql")], capture_output=True, text=True, check=True)
    return [line.split("\t") for line in result.stdout.splitlines()]


class NativeAccess(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        sql((Path(__file__).parent / "native-fixture.sql").read_text())
        sql("""SET ROLE fixture_owner;
CREATE TABLE fixture_app.future (id bigint PRIMARY KEY, tenant_id integer NOT NULL);
CREATE SEQUENCE fixture_app.future_issued;
CREATE FUNCTION fixture_app.future_ping() RETURNS integer LANGUAGE sql AS 'SELECT 42';
RESET ROLE;""", login="fixture_migrator")

    def test_native_metadata_and_effective_paths(self):
        rows = audit()
        role = next(row for row in rows if row[0] == "fixture_reader")
        self.assertEqual(role[1:6], ["t", "f", "f", "f", "f"])
        reaches = {row[1]: row[2:] for row in rows if row[0] == "reach"}
        self.assertEqual(reaches["fixture_read_group"], ["t", "t"])
        self.assertNotIn("fixture_owner", reaches)
        orders = next(row for row in rows if row[:3] == ["object", "fixture_app", "orders"])
        # Columns after the native ACL are SELECT, INSERT, UPDATE, DELETE, TRUNCATE.
        self.assertEqual(orders[8:13], ["t", "f", "f", "f", "f"])
        future = next(row for row in rows if row[:3] == ["object", "fixture_app", "future"])
        self.assertEqual(future[3], "fixture_owner")
        self.assertEqual(audit(), rows)
        sql("GRANT fixture_owner TO fixture_reader")
        try:
            changed = {row[1]: row[2:] for row in audit() if row[0] == "reach"}
            self.assertEqual(changed["fixture_owner"], ["t", "t"])
        finally:
            sql("REVOKE fixture_owner FROM fixture_reader")

    def test_actual_reader_denials_and_bound_receipts(self):
        probes = [
            ("select", "SELECT id FROM fixture_app.orders ORDER BY id;", "allow"),
            ("insert", "INSERT INTO fixture_app.orders VALUES (3, 1, 1);", "deny"),
            ("ddl", "CREATE TABLE fixture_app.forbidden (id int);", "deny"),
            ("switch", "SET ROLE fixture_owner;", "deny"),
            ("sequence", "SELECT nextval('fixture_app.issued');", "deny"),
            ("function", "SELECT fixture_app.bump();", "deny"),
            ("future-table", "SELECT id FROM fixture_app.future;", "allow"),
            ("future-sequence", "SELECT nextval('fixture_app.future_issued');", "deny"),
            ("future-function", "SELECT fixture_app.future_ping();", "deny"),
        ]
        policy = {"target_id": "owned-cluster/postgres", "checks": []}
        results = {"target_id": policy["target_id"], "checks": []}
        identity_sql = """SELECT json_build_object(
  'authenticated_login', session_user, 'session_role', current_user,
  'reachable_roles', (SELECT json_agg(rolname ORDER BY rolname) FROM pg_roles
    WHERE pg_has_role(current_user, oid, 'USAGE') OR
      CASE WHEN current_setting('server_version_num')::integer >= 160000
           THEN pg_has_role(current_user, oid, 'SET') ELSE pg_has_role(current_user, oid, 'MEMBER') END),
  'role_flags', (SELECT json_build_object('superuser', rolsuper, 'bypassrls', rolbypassrls,
    'createrole', rolcreaterole, 'createdb', rolcreatedb) FROM pg_roles WHERE rolname = current_user));"""
        for name, statement, expected in probes:
            probe = "SET fixture.tenant = '1'; SET default_transaction_read_only = off; " + identity_sql + statement
            result = sql(probe,
                         login="fixture_reader", check=False)
            success = result.returncode == 0
            code = "00000" if success else re.search(r"ERROR:\s+([A-Z0-9]{5})", result.stderr).group(1)
            self.assertEqual((success, code), (expected == "allow", "00000" if expected == "allow" else "42501"), name)
            identity = json.loads(result.stdout.splitlines()[0])
            self.assertEqual(identity["authenticated_login"], "fixture_reader")
            self.assertEqual(identity["session_role"], "fixture_reader")
            digest = hashlib.sha256(probe.encode()).hexdigest()
            check = {"id": name, "login": "fixture_reader", "session_role": "fixture_reader", "phase": "future" if name.startswith("future") else "existing",
                     "kind": "sql", "probe_sha256": digest, "expected": expected, "codes": [code],
                     "forbidden_roles": ["fixture_owner", "fixture_migrator"]}
            policy["checks"].append(check)
            results["checks"].append({**check, "result": "allow" if success else "deny", "code": code,
                                      "fresh_attempt": True, "adapter": "actual-client", **identity})
        self.assertEqual(sql("SET fixture.tenant = '1'; SELECT id FROM fixture_app.orders ORDER BY id;", login="fixture_reader").stdout.strip(), "1")
        self.assertEqual(sql("SELECT fixture_app.future_ping();", login="fixture_runtime").stdout.strip(), "42")
        with tempfile.TemporaryDirectory() as directory:
            p, r = Path(directory) / "policy.json", Path(directory) / "results.json"
            p.write_text(json.dumps(policy)); results["policy_sha256"] = hashlib.sha256(p.read_bytes()).hexdigest()
            r.write_text(json.dumps(results))
            command = [sys.executable, str(SKILL / "scripts/check-privileges.py"), str(p), str(r)]
            first = subprocess.run(command, capture_output=True, text=True)
            self.assertEqual(first.returncode, 0, first.stderr)
            self.assertEqual(subprocess.run(command, capture_output=True, text=True).stdout, first.stdout)
            altered = copy.deepcopy(results); altered["checks"][1]["code"] = "42601"; r.write_text(json.dumps(altered))
            self.assertEqual(subprocess.run(command, capture_output=True).returncode, 1)


if __name__ == "__main__":
    unittest.main()
