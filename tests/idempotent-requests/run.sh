#!/bin/sh
# Test the SQL starter's constraints and unique admission on a disposable server.
# This does not execute an application retry/recovery protocol or a provider call.
set -eu
case "${1-}" in
  --help|-h) printf '%s\n' 'Usage: run.sh [--help]. Offline disposable SQL-asset fixtures; set PG_IMAGE to a local PostgreSQL image. Exits 0 pass/explicit skip, 1 test failure, 2 setup/usage.'; exit 0 ;;
  '') ;;
  *) printf '%s\n' 'error: use run.sh without arguments or with --help' >&2; exit 2 ;;
esac
test_dir=$(CDPATH='' cd -P "$(dirname "$0")" && pwd)
. "$test_dir/pg.sh"
if pg_start; then :; else
  code=$?
  [ "$code" -eq 1 ] && exit 0
  exit "$code"
fi
pg_sql < "$test_dir/../../skills/idempotent-requests/assets/idempotency.sql"
pg_sql < "$test_dir/cases.sql"
# Observable lock-state barrier, with a deadline; polling does not choose the schedule.
wait_for() {
  pg_sql <<SQL
SET statement_timeout = '20s';
DO \$\$
BEGIN
  LOOP
    PERFORM pg_stat_clear_snapshot();
    EXIT WHEN EXISTS (SELECT 1 FROM pg_stat_activity WHERE application_name = '$1' AND $2);
    PERFORM pg_sleep(0.05);
  END LOOP;
END \$\$;
SQL
}
race="INSERT INTO request_idempotency (tenant_id,principal_id,operation,idempotency_key,request_fingerprint,expires_at) VALUES ('race','u','create','k',decode(repeat('00',32),'hex'),CURRENT_TIMESTAMP + interval '1 day') ON CONFLICT DO NOTHING RETURNING 'new';"
mkfifo "$pg_tmp/a.fifo"
pg_query < "$pg_tmp/a.fifo" > "$pg_tmp/a.out" 2>&1 &
a_pid=$!
exec 3>"$pg_tmp/a.fifo"
printf "SET application_name='asset_a';\nBEGIN;\n%s\n" "$race" >&3
wait_for asset_a "state = 'idle in transaction'"
printf "SET application_name='asset_b';\n%s\n" "$race" | pg_query > "$pg_tmp/b.out" 2>&1 &
b_pid=$!
wait_for asset_b "wait_event_type = 'Lock'"
printf 'COMMIT;\n' >&3
exec 3>&-
wait "$a_pid"
wait "$b_pid"
if [ "$(cat "$pg_tmp/a.out")" != new ] || [ -s "$pg_tmp/b.out" ]; then
  echo 'FAIL: unique scope did not serialize competing inserts' >&2
  exit 1
fi
pg_sql <<'SQL'
SELECT expect('one committed key under concurrency', (SELECT count(*) FROM request_idempotency WHERE tenant_id='race'), 1::bigint);
SQL
echo 'PASS: SQL starter scope, state/result constraints and barrier-controlled concurrent insert; application/provider recovery remains untested'
