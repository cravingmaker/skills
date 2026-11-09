"""Exercise the actual SQL fragments in an owned, socket-free PostgreSQL cluster.

Single-user backends check sequential transitions and real commit/rollback. They
do not prove multi-connection locking, concurrent delivery, or broker behavior.
"""
from pathlib import Path
import shutil
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[2]
SQL = ROOT / "skills/async-messaging/assets/outbox-inbox.sql"
INITDB, POSTGRES = shutil.which("initdb"), shutil.which("postgres")
if not INITDB or not POSTGRES:
    print("Skipped messaging SQL fixtures: install initdb and postgres on PATH; each run creates its own disposable cluster.")
    raise SystemExit(0)

source = SQL.read_text()
markers = ["-- Claim:", "-- Complete:", "-- Consumer admission:", "-- Final-attempt crash sweep:"]
for marker in markers:
    assert source.count(marker) == 1, "SQL starter section missing: " + marker
sections = []
remaining = source
for marker in markers:
    before, remaining = remaining.split(marker, 1)
    sections.append(before)
sections.append(remaining)
# The first line of each section after the schema is a heading continuation.
sections[1:] = [part.split("\n", 1)[1] for part in sections[1:]]
sections = ["\n".join(line for line in part.splitlines() if not line.lstrip().startswith("--"))
            for part in sections]

with tempfile.TemporaryDirectory(prefix="messaging-sql-") as directory:
    data = Path(directory) / "data"
    subprocess.run([INITDB, "-D", str(data), "-U", "postgres", "-A", "trust", "--no-sync"],
                   check=True, capture_output=True, timeout=30)

    def sql(text, expect_error=False):
        # Asset comments are whole lines; preserve SQL literals as written.
        text = " ".join(line for line in text.splitlines() if not line.lstrip().startswith("--"))
        result = subprocess.run([POSTGRES, "--single", "-D", str(data), "postgres"],
                                input=text + "\n", capture_output=True, text=True, timeout=15)
        failed = result.returncode != 0 or "ERROR:" in result.stderr or "FATAL:" in result.stderr
        assert failed == expect_error, result.stdout + result.stderr

    def check(name, predicate):
        sql("DO $$ BEGIN IF NOT (" + predicate + ") THEN RAISE EXCEPTION 'fixture: " + name + "'; END IF; END $$;")

    sql(sections[0])
    for name, args, returns, body in [
        ("fixture_claim", "integer, interval", "SETOF outbox_messages", sections[1]),
        ("fixture_complete", "text, uuid, bigint", "SETOF uuid", sections[2]),
        ("fixture_admit", "text, text, uuid, text", "SETOF uuid", sections[3]),
        ("fixture_sweep", "", "TABLE (tenant_id text, event_id uuid)", sections[4]),
    ]:
        sql(f"CREATE FUNCTION {name}({args}) RETURNS {returns} LANGUAGE sql AS $$ {body} $$;")
    event = "00000000-0000-0000-0000-000000000001"
    sql(f"INSERT INTO outbox_messages (tenant_id,event_id,aggregate_key,aggregate_sequence,event_type,schema_version,payload,payload_fingerprint,max_attempts) VALUES ('t','{event}','order',1,'paid',1,'{{}}','fp',2);")
    check("claim one", "(SELECT count(*) FROM fixture_claim(1, interval '30 seconds')) = 1")
    check("live lease not reclaimed", "(SELECT count(*) FROM fixture_claim(1, interval '30 seconds')) = 0")
    sql("UPDATE outbox_messages SET lease_until = clock_timestamp() - interval '1 second';")
    check("expired owner cannot complete", f"(SELECT count(*) FROM fixture_complete('t','{event}',1)) = 0")
    check("reclaim", "(SELECT count(*) FROM fixture_claim(1, interval '30 seconds')) = 1")
    check("generation increment", "(SELECT lease_generation = 2 AND attempts = 2 FROM outbox_messages)")
    check("old generation cannot complete", f"(SELECT count(*) FROM fixture_complete('t','{event}',1)) = 0")
    sql("UPDATE outbox_messages SET lease_until = clock_timestamp() - interval '1 second';")
    check("exhausted claim refused", "(SELECT count(*) FROM fixture_claim(1, interval '30 seconds')) = 0")
    check("sweep final attempt", "(SELECT count(*) FROM fixture_sweep()) = 1")
    check("retained terminal row", "(SELECT state = 'dead' AND failure_code = 'attempts_exhausted' FROM outbox_messages)")
    sql("CREATE TABLE fixture_effect (n integer); INSERT INTO fixture_effect VALUES (0);")
    admission = f"fixture_admit('consumer','t','{event}','fp')"
    sql(f"BEGIN; SELECT * FROM {admission}; UPDATE fixture_effect SET n = n + 1; ROLLBACK;")
    check("rollback removes inbox and effect", "(SELECT count(*) FROM consumer_inbox) = 0 AND (SELECT n FROM fixture_effect) = 0")
    sql(f"BEGIN; WITH admitted AS (SELECT * FROM {admission}) UPDATE fixture_effect SET n = n + 1 WHERE EXISTS (SELECT 1 FROM admitted); COMMIT;")
    sql(f"WITH admitted AS (SELECT * FROM {admission}) UPDATE fixture_effect SET n = n + 1 WHERE EXISTS (SELECT 1 FROM admitted);")
    check("duplicate leaves one committed effect", "(SELECT n FROM fixture_effect) = 1")
    check("fingerprint retained", "(SELECT payload_fingerprint = 'fp' FROM consumer_inbox)")
    check("tenant scopes admission", f"(SELECT count(*) FROM fixture_admit('consumer','other','{event}','fp')) = 1")
    sql(f"BEGIN; UPDATE fixture_effect SET n = n + 1; DO $$ BEGIN IF NOT EXISTS (SELECT 1 FROM fixture_complete('t','{event}',1)) THEN RAISE EXCEPTION 'lost ownership'; END IF; END $$; COMMIT;", expect_error=True)
    check("lost ownership rolls back effect", "(SELECT n FROM fixture_effect) = 1")
print("Messaging SQL fixtures passed: actual fragments, sequential fencing and commit/rollback; concurrency remains an application test.")
