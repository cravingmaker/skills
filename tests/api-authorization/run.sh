#!/bin/sh
set -eu
case "${1-}" in
  --help|-h) printf '%s\n' 'Usage: run.sh [--help]. Run offline fixtures; exits 0 pass, 1 test failure, 2 usage.'; exit 0 ;;
  '') ;;
  *) printf '%s\n' 'error: use run.sh without arguments or with --help' >&2; exit 2 ;;
esac
test_dir=$(CDPATH='' cd -P "$(dirname "$0")" && pwd)
"${PYTHON:-python3}" "$test_dir/test_script.py"
. "$test_dir/pg.sh"
if pg_start; then :; else
  code=$?
  [ "$code" -eq 1 ] && exit 0
  exit "$code"
fi
cat "$test_dir/rls-setup.sql" "$test_dir/../../skills/api-authorization/assets/rls-policy.sql" | pg_sql
pg_sql app_api < "$test_dir/rls-runtime.sql"
pg_sql app_jobs <<'SQL'
SELECT expect('actual job login', session_user::text, 'app_jobs'::text);
SELECT expect('job missing context', (SELECT count(*) FROM invoices), 0::bigint);
BEGIN;
SELECT set_config('app.tenant_id', '00000000-0000-0000-0000-00000000000b', true);
SELECT expect('job tenant scope', (SELECT count(*) FROM invoices), 1::bigint);
COMMIT;
SQL
pg_sql bi_reader <<'SQL'
SELECT expect('BYPASSRLS even with FORCE', (SELECT count(*) FROM invoices), 3::bigint);
SQL
pg_sql < "$test_dir/rls-exceptions.sql"
pg_sql app_api < "$test_dir/rls-views.sql"
echo 'PASS: RLS starter row operations, real runtime logins, reused context and selected privileged/view/function exceptions'

