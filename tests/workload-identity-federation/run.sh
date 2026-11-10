#!/bin/sh
set -eu
test_dir=$(CDPATH='' cd -P "$(dirname "$0")" && pwd)
exec "${PYTHON:-python3}" "$test_dir/test_trust.py"
