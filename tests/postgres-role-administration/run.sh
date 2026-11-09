#!/bin/sh
set -eu
test_dir=$(CDPATH='' cd -P "$(dirname "$0")" && pwd)
"${PYTHON:-python3}" "$test_dir/test_check.py"
for native_tool in initdb pg_ctl psql; do
  if ! command -v "$native_tool" >/dev/null 2>&1; then
    echo 'Skipped native access fixtures: install matching initdb, pg_ctl and psql on PATH; offline receipt tests passed.'
    exit 0
  fi
done
work=$(mktemp -d "${TMPDIR:-/tmp}/postgres-access-test.XXXXXX")
cleanup() {
  if [ -d "$work/data" ]; then pg_ctl -D "$work/data" -m immediate -w stop >/dev/null 2>&1 || :; fi
  rm -rf "$work"
}
trap cleanup 0
trap 'exit 1' HUP INT TERM
port=$("${PYTHON:-python3}" -c 'import socket; s=socket.socket(); s.bind(("127.0.0.1",0)); print(s.getsockname()[1]); s.close()')
initdb -D "$work/data" -A trust -U fixture --no-locale >/dev/null
pg_ctl -D "$work/data" -l "$work/server.log" -o "-F -h 127.0.0.1 -k '' -p $port" -w start >/dev/null
export PGHOST=127.0.0.1 PGPORT="$port" PGUSER=fixture PGDATABASE=postgres
export PGPASSFILE=/dev/null PGSERVICEFILE=/dev/null
unset PGSERVICE PGOPTIONS || :
"${PYTHON:-python3}" "$test_dir/test_native.py"
echo 'Passed native access, future-object and receipt fixtures on an owned disposable cluster.'
