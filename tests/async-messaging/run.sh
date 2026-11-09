#!/bin/sh
set -eu
test_dir=$(CDPATH='' cd -P "$(dirname "$0")" && pwd)
"${PYTHON:-python3}" "$test_dir/test_contract.py"
exec "${PYTHON:-python3}" "$test_dir/test_sql.py"
