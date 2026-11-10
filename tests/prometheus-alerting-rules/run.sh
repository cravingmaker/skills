#!/bin/sh
set -eu
case "${1:-}" in
  --help|-h) echo 'Usage: run.sh; offline native fixtures, no network or real database. PROMTOOL/AMTOOL may name explicit binaries. Exit 0 pass/declared tool skip; nonzero test failure.'; exit 0 ;;
  '') ;;
  *) echo 'error: run without arguments or use --help' >&2; exit 2 ;;
esac
test_dir=$(CDPATH='' cd -P "$(dirname "$0")" && pwd)
exec "${PYTHON:-python3}" "$test_dir/test_native.py"
