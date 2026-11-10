#!/bin/sh
set -eu
case "${1-}" in
  --help|-h) printf '%s\n' 'Usage: run.sh [--help]. Offline fixture checks. Exits: 0 pass or named missing-tool skip, 1 test failure, 2 usage.'; exit 0 ;;
  '') ;;
  *) printf '%s\n' 'error: run without arguments or use --help' >&2; exit 2 ;;
esac
test_dir=$(CDPATH='' cd -P "$(dirname "$0")" && pwd)
exec "${PYTHON:-python3}" "$test_dir/test_script.py"
