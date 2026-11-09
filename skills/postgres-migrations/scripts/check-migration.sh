#!/bin/sh
# Read-only wrapper around the repository's pinned Squawk executable.
set -eu
case "${1:-}" in
  --help|-h)
    cat <<'HELP'
Usage: check-migration.sh --squawk EXECUTABLE -- FILE.sql [FILE.sql ...]
Use the repository's pinned Squawk binary or project-owned wrapper.
Lint only: no database connection, mutation, downloads or interactive prompts.
Fixed JSON status goes to stdout; wrapper diagnostics go to stderr.
Native output is withheld because a diagnostic may quote sensitive SQL.
Exit: 0 lint passed, 1 lint findings, 2 usage/setup/input failure.
HELP
    exit 0 ;;
esac
if [ "$#" -lt 4 ] || [ "$1" != --squawk ] || [ "$3" != -- ]; then
  echo 'error: use --squawk EXECUTABLE -- FILE.sql; see --help' >&2
  exit 2
fi
squawk_bin=$2
shift 3
if ! command -v "$squawk_bin" >/dev/null 2>&1; then
  echo 'error: resolve the repository-pinned Squawk executable; do not install latest implicitly' >&2
  exit 2
fi
for migration_file do
  case "$migration_file" in
    -*|*://*)
      echo 'error: pass local SQL paths, prefixing a leading hyphen with ./; never pass a connection URL' >&2
      exit 2 ;;
  esac
  if [ ! -f "$migration_file" ]; then
    echo 'error: supply existing migration files' >&2
    exit 2
  fi
done
if "$squawk_bin" "$@" >/dev/null 2>&1; then
  printf '%s\n' '{"ok":true,"tool":"squawk"}'
  exit 0
else
  lint_status=$?
  if [ "$lint_status" -eq 1 ]; then
    printf '%s\n' '{"ok":false,"tool":"squawk","status":"findings"}'
    echo 'error: address the Squawk findings or record a scoped reviewed suppression' >&2
    exit 1
  fi
  printf '%s\n' '{"ok":false,"tool":"squawk","status":"tool_error"}'
  echo 'error: Squawk could not complete; check the pinned CLI and project configuration' >&2
  exit 2
fi
