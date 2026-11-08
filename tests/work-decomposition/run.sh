#!/bin/sh
set -eu
test_dir=$(CDPATH='' cd -P "$(dirname "$0")" && pwd)
"${PYTHON:-python3}" "$test_dir/test_plan.py"
exec "${PYTHON:-python3}" "$test_dir/test_import.py"
