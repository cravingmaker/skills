#!/bin/sh
set -eu
test_dir=$(CDPATH='' cd -P "$(dirname "$0")" && pwd)
"${PYTHON:-python3}" "$test_dir/test_runner.py"
if ! command -v uv >/dev/null 2>&1; then
  echo 'Skipped wizard parser fixtures: install uv, then seed python-dotenv==1.1.1 with uv sync --script tests/wizard/test_wizard.py.'
  exit 0
fi
# Resolve/install the pinned dependency separately so test failures never become skips.
# Validation never fetches packages; seed the cache once with the command below.
if ! uv sync --offline --quiet --script "$test_dir/test_wizard.py"; then
  echo 'Skipped wizard parser fixtures: python-dotenv==1.1.1 or Python 3.12+ is unavailable offline. Seed once with: uv sync --script tests/wizard/test_wizard.py.'
  exit 0
fi
exec uv run --offline --quiet --script "$test_dir/test_wizard.py"
