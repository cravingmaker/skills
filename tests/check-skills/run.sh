#!/usr/bin/env bash
# Prove the repository checker accepts the pass fixtures and rejects each fail fixture.
set -euo pipefail

cd "$(dirname "$0")"
checker=../../scripts/check-skills.py
status=0

for dir in pass/*/; do
  if ! "$checker" "$dir" >/dev/null; then
    echo "check-skills fixture should pass but failed: $dir" >&2
    status=1
  fi
done

for dir in fail/*/; do
  if "$checker" "$dir" >/dev/null; then
    echo "check-skills fixture should fail but passed: $dir" >&2
    status=1
  fi
done

[ "$status" -eq 0 ] && echo "check-skills fixtures behave as expected."
exit "$status"
