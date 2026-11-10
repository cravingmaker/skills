#!/bin/sh
set -eu
case "${1:-}" in
  --help|-h) echo 'Usage: run.sh; offline stdlib calculator and optional native-rule fixtures. PROMTOOL may name an explicit binary. Exit 0 pass/declared native skip; nonzero test failure.'; exit 0 ;;
  '') ;;
  *) echo 'error: run without arguments or use --help' >&2; exit 2 ;;
esac
test_dir=$(CDPATH='' cd -P "$(dirname "$0")" && pwd)
exec "${PYTHON:-python3}" "$test_dir/test_burn_rate.py"
