#!/usr/bin/env bash
# Prove the installer: a role installs its whole requires closure by copy and by
# symlink, works when run from outside the checkout, lists upstream prerequisites,
# refuses foreign destinations even with --force, and fails clearly on a missing dependency.
set -uo pipefail

here="$(cd "$(dirname "$0")" && pwd)"
installer="$here/../../scripts/install-skills.py"
fixtures="$here/../check-catalog"
work="$(mktemp -d)"
export HOME="$work/home" CLAUDE_CONFIG_DIR="$work/home/.claude" CODEX_HOME="$work/home/.codex" XDG_CONFIG_HOME="$work/config"
mkdir -p "$HOME" "$CLAUDE_CONFIG_DIR" "$CODEX_HOME" "$XDG_CONFIG_HOME"
trap 'rm -rf "$work"' EXIT
status=0
fail() { echo "install test failed: $1" >&2; status=1; }

# Run from an unrelated directory to prove the installer does not depend on the working directory.
cd "$work" || exit 1

out="$("$installer" --apply --root "$fixtures/pass/consistent" --target "$work/copy" role-one 2>&1)" || fail "copy install failed: $out"
for name in role-one cap-a cap-b; do
  [ -f "$work/copy/$name/SKILL.md" ] && [ ! -L "$work/copy/$name" ] || fail "copy install is missing $name as a real folder"
done
grep -q '"provider": "upstream"' <<<"$out" || fail "copy install should list the external prerequisite ext-x"

out="$("$installer" --apply --root "$fixtures/pass/consistent" --target "$work/link" --mode symlink cap-a 2>&1)" || fail "symlink install failed: $out"
[ -L "$work/link/cap-a" ] && [ -L "$work/link/cap-b" ] || fail "symlink install should link cap-a and its requirement cap-b"
[ ! -e "$work/link/role-one" ] || fail "installing cap-a must not install the role that uses it"

out="$("$installer" --apply --root "$fixtures/pass/consistent" --target "$work/copy" role-one 2>&1)" || fail "an unchanged owned install should be idempotent: $out"
out="$("$installer" --apply --root "$fixtures/pass/consistent" --target "$work/copy" --force role-one 2>&1)" || fail "--force reinstall failed: $out"

if out="$("$installer" --apply --root "$fixtures/fail/unknown-requires" --target "$work/missing" cap-c 2>&1)"; then
  fail "a missing required skill should fail the install"
elif ! grep -q "nope is required" <<<"$out"; then
  fail "the missing-dependency error should name the missing skill: $out"
fi
[ ! -e "$work/missing" ] || fail "a failed install must not create the target"

# A forced reinstall must never delete its own source, including a parent alias.
cp -R "$fixtures/pass/consistent" "$work/source"
ln -s "$work/source/skills" "$work/source-alias"
for mode in copy symlink; do
  for target in "$work/source/skills" "$work/source-alias" "$work/source/skills/cap-a/nested"; do
    if out="$("$installer" --apply --root "$work/source" --target "$target" --mode "$mode" --force cap-a 2>&1)"; then
      fail "overlapping $mode install should fail: $target"
    elif ! grep -q "overlaps the source" <<<"$out"; then
      fail "overlap should name the safe fix: $out"
    fi
    [ -f "$work/source/skills/cap-a/SKILL.md" ] || fail "overlap rejection deleted its source"
    [ ! -e "$work/source/skills/cap-a/nested" ] || fail "overlap rejection wrote inside its source"
  done
done
# Replacing an installed link with a copy remains supported.
out="$("$installer" --apply --root "$fixtures/pass/consistent" --target "$work/link" --force cap-a 2>&1)" || fail "replacing installed links failed: $out"
[ -f "$work/link/cap-a/SKILL.md" ] && [ ! -L "$work/link/cap-a" ] || fail "link replacement did not create a copy"

# Omit only evals/results; other resources named results are part of the skill.
mkdir -p "$work/source/skills/cap-a/assets/results" "$work/source/skills/cap-a/evals/results"
printf '%s\n' '{"expected": true}' > "$work/source/skills/cap-a/assets/results/expected.json"
printf '%s\n' 'private evaluation evidence' > "$work/source/skills/cap-a/evals/results/private.md"
out="$("$installer" --apply --root "$work/source" --target "$work/assets" cap-a 2>&1)" || fail "resource copy failed: $out"
cmp "$work/source/skills/cap-a/assets/results/expected.json" "$work/assets/cap-a/assets/results/expected.json" || fail "copy omitted or changed a required resource"
[ ! -e "$work/assets/cap-a/evals/results" ] || fail "copy included eval evidence"

[ "$status" -eq 0 ] && echo "Installer behaves as expected."
exit "$status"
