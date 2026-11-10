#!/bin/sh
set -eu
case "${1-}" in
  --help|-h) printf '%s\n' 'Usage: run.sh [--help]. Run offline fixtures; exits 0 pass, 1 test failure, 2 usage.'; exit 0 ;;
  '') ;;
  *) printf '%s\n' 'error: run without arguments or with --help' >&2; exit 2 ;;
esac
test_dir=$(CDPATH='' cd -P "$(dirname "$0")" && pwd)
exec "${PYTHON:-python3}" "$test_dir/test_script.py"
