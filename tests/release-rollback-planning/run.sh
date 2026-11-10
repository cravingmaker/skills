#!/bin/sh
set -eu
export PYTHONDONTWRITEBYTECODE=1
test_dir=$(CDPATH='' cd -P "$(dirname "$0")" && pwd)
exec "${PYTHON:-python3}" "$test_dir/test_check_rollback_plan.py"
