#!/usr/bin/env bash
# Prove the catalog checker and the profile generator accept the consistent
# fixture and reject each broken one, each for its own reason.
set -uo pipefail

cd "$(dirname "$0")"
scripts=../../scripts
status=0
fail() { echo "check-catalog fixture failed: $1" >&2; status=1; }

out="$("$scripts/check-catalog.py" --root pass/consistent 2>&1)" || fail "pass/consistent should pass: $out"
out="$("$scripts/build-profiles.py" --check --root pass/consistent 2>&1)" || fail "pass/consistent profiles should be current: $out"

expect() { # case, script, expected message fragment
  local out
  if out="$("$scripts/$2" --root "fail/$1" 2>&1)"; then
    fail "fail/$1 should fail $2"
  elif ! grep -q -- "$3" <<<"$out"; then
    fail "fail/$1 failed for another reason: $out"
  fi
}

expect missing-entry check-catalog.py "skills/cap-c has no entry"
expect unknown-requires check-catalog.py "names nope"
expect reserved-name check-catalog.py "reserved-one is a reserved name"
expect role-without-requires check-catalog.py "needs metadata.requires"
expect evaluated-without-results check-catalog.py "no recorded runs"
expect unknown-role check-catalog.py "unknown role ghost-role"
expect self-requires check-catalog.py "names the skill itself"
expect external-duplicate check-catalog.py "also exists in skills/"

if out="$("$scripts/build-profiles.py" --check --root fail/profile-drift 2>&1)"; then
  fail "fail/profile-drift should report drift"
elif ! grep -q "role-one.txt is out of date" <<<"$out"; then
  fail "fail/profile-drift failed for another reason: $out"
fi

[ "$status" -eq 0 ] && echo "check-catalog fixtures behave as expected."
exit "$status"
