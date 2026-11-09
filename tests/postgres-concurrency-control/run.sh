#!/bin/sh
set -eu
test_dir=$(CDPATH='' cd -P "$(dirname "$0")" && pwd)
if ! command -v node >/dev/null 2>&1; then
  echo 'Skipped concurrency starter control-flow tests: install a Node runtime with TypeScript stripping, then rerun.'
  exit 0
fi
if ! node --experimental-strip-types --eval '' >/dev/null 2>&1; then
  echo 'Skipped concurrency starter control-flow tests: use a Node runtime with TypeScript stripping, then rerun.'
  exit 0
fi
exec node --experimental-strip-types --test "$test_dir/retry.test.mjs"
