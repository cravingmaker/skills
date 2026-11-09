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

work="$(mktemp -d)"
trap 'rm -rf "$work"' EXIT
cp -R pass/consistent "$work/repo"
sed 's/status: unevaluated/status: evaluated/' "$work/repo/catalog/skills.yaml" > "$work/repo/catalog/new.yaml"
# Only cap-a is under evaluation; keep the other two entries unevaluated.
awk '/cap-b:|role-one:/ { sub(/status: evaluated/, "status: unevaluated") } { print }' "$work/repo/catalog/new.yaml" > "$work/repo/catalog/skills.yaml"
records="$work/repo/skills/cap-a/evals/results"
mkdir -p "$records"
printf '%s\n' 'Comparison: **invalid**.' > "$records/invalid.md"
if out="$("$scripts/check-catalog.py" --root "$work/repo" 2>&1)"; then
  fail "an invalid record must not satisfy evaluated status"
elif ! grep -q 'missing valid completed paired runs' <<<"$out"; then
  fail "invalid-record rejection gave another reason: $out"
fi
for example in activation-1 near-miss-1; do
  cat > "$records/$example.md" <<EOF
Comparison: **valid**.
- **Source example.** \`$example\` in \`evals/examples.md\`.
| treatment | true | false | 0 | 0 |
| baseline | false | false | 0 | 0 |
EOF
  if [ "$example" = activation-1 ] && "$scripts/check-catalog.py" --root "$work/repo" >/dev/null; then
    fail "activation coverage alone must not satisfy evaluated status"
  fi
done
out="$("$scripts/check-catalog.py" --root "$work/repo" 2>&1)" || fail "valid paired coverage should pass even when activation failed: $out"

cp -R pass/consistent "$work/missing"
sed 's/requires: "cap-b"/requires: "missing"/' "$work/missing/skills/cap-a/SKILL.md" > "$work/missing/skills/cap-a/new.md"
mv "$work/missing/skills/cap-a/new.md" "$work/missing/skills/cap-a/SKILL.md"
for check in '' '--check'; do
  if out="$("$scripts/build-profiles.py" $check --root "$work/missing" 2>&1)"; then
    fail "profile generation should reject an unresolved transitive dependency"
  elif ! grep -q 'missing required skills missing' <<<"$out"; then
    fail "profile failure must name the missing dependency: $out"
  fi
  cmp pass/consistent/catalog/profiles/role-one.txt "$work/missing/catalog/profiles/role-one.txt" || fail "failed profile generation changed the previous profile"
done

[ "$status" -eq 0 ] && echo "check-catalog fixtures behave as expected."
exit "$status"
