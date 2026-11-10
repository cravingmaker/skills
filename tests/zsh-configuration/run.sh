#!/bin/sh
set -eu
test_dir=$(CDPATH='' cd -P "$(dirname "$0")" && pwd)
export PYTHONDONTWRITEBYTECODE=1
exec "${PYTHON:-python3}" "$test_dir/test_helper.py"
