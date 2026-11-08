#!/usr/bin/env bash
# Prove the installer: a role installs its whole requires closure by copy and by
# symlink, works when run from outside the checkout, lists upstream prerequisites,
# refuses to overwrite without --force, and fails clearly on a missing dependency.
set -uo pipefail

here="$(cd "$(dirname "$0")" && pwd)"
installer="$here/../../scripts/install-skills.py"
fixtures="$here/../check-catalog"
work="$(mktemp -d)"
trap 'rm -rf "$work"' EXIT
status=0
fail() { echo "install test failed: $1" >&2; status=1; }

# Run from an unrelated directory to prove the installer does not depend on the working directory.
cd "$work" || exit 1

out="$("$installer" --root "$fixtures/pass/consistent" --target "$work/copy" role-one 2>&1)" || fail "copy install failed: $out"
for name in role-one cap-a cap-b; do
  [ -f "$work/copy/$name/SKILL.md" ] && [ ! -L "$work/copy/$name" ] || fail "copy install is missing $name as a real folder"
done
grep -q "prerequisite: install ext-x from upstream" <<<"$out" || fail "copy install should list the external prerequisite ext-x"

out="$("$installer" --root "$fixtures/pass/consistent" --target "$work/link" --mode symlink cap-a 2>&1)" || fail "symlink install failed: $out"
[ -L "$work/link/cap-a" ] && [ -L "$work/link/cap-b" ] || fail "symlink install should link cap-a and its requirement cap-b"
[ ! -e "$work/link/role-one" ] || fail "installing cap-a must not install the role that uses it"

if out="$("$installer" --root "$fixtures/pass/consistent" --target "$work/copy" role-one 2>&1)"; then
  fail "a second install without --force should refuse to overwrite"
fi
out="$("$installer" --root "$fixtures/pass/consistent" --target "$work/copy" --force role-one 2>&1)" || fail "--force reinstall failed: $out"

if out="$("$installer" --root "$fixtures/fail/unknown-requires" --target "$work/missing" cap-c 2>&1)"; then
  fail "a missing required skill should fail the install"
elif ! grep -q "nope is required" <<<"$out"; then
  fail "the missing-dependency error should name the missing skill: $out"
fi
[ ! -e "$work/missing" ] || fail "a failed install must not create the target"

[ "$status" -eq 0 ] && echo "Installer behaves as expected."
exit "$status"
