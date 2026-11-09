#!/bin/sh
# Creates and owns a disposable local cluster; never uses DATABASE_URL.
set -eu
test_dir=$(CDPATH='' cd -P "$(dirname "$0")" && pwd)
"${PYTHON:-python3}" "$test_dir/test_audit.py"
for native_tool in initdb pg_ctl psql; do
  if ! command -v "$native_tool" >/dev/null 2>&1; then
    echo 'Skipped PostgreSQL constraint fixtures: install matching initdb, pg_ctl and psql on PATH; no existing database was used.'
    exit 0
  fi
done
test_dir=$(CDPATH='' cd -P "$(dirname "$0")" && pwd)
repo_dir=$(CDPATH='' cd -P "$test_dir/../.." && pwd)
work=$(mktemp -d "${TMPDIR:-/tmp}/postgres-schema-test.XXXXXX")
cleanup() {
  if [ -d "$work/data" ]; then pg_ctl -D "$work/data" -m immediate -w stop >/dev/null 2>&1 || :; fi
  rm -rf "$work"
}
trap cleanup 0
trap 'exit 1' HUP INT TERM
port=$("${PYTHON:-python3}" -c 'import socket; s=socket.socket(); s.bind(("127.0.0.1",0)); print(s.getsockname()[1]); s.close()')
initdb -D "$work/data" -A trust -U fixture --no-locale >/dev/null
pg_ctl -D "$work/data" -l "$work/server.log" -o "-F -h 127.0.0.1 -k '' -p $port" -w start >/dev/null
cat "$repo_dir/skills/postgres-schema-design/assets/constraint-example.sql" "$test_dir/proof.sql" > "$work/proof.sql"
psql -X -w -h 127.0.0.1 -p "$port" -U fixture -d postgres -v ON_ERROR_STOP=1 -q -f "$work/proof.sql"
export PGHOST=127.0.0.1 PGPORT="$port" PGUSER=fixture PGDATABASE=postgres
export PGPASSFILE=/dev/null PGSERVICEFILE=/dev/null
unset PGSERVICE PGOPTIONS || :
SKILL_TEST_PG=owned "${PYTHON:-python3}" "$test_dir/test_audit.py"
echo 'Passed PostgreSQL constraint and catalog fixtures on an owned disposable cluster.' 
