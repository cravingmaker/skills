#!/usr/bin/env bash
# Prove check-ownership.sh in throwaway repositories: a clean tree passes the
# read-only check; committed, staged, unstaged, untracked, deleted, and
# changed-back paths outside the boundary fail; paths inside it pass; usage
# errors exit 2.
set -uo pipefail

here="$(cd "$(dirname "$0")" && pwd)"
check="$here/../../skills/result-verification/scripts/check-ownership.sh"
work="$(mktemp -d)"
trap 'rm -rf "$work"' EXIT
status=0
output=""

# Isolate git from the user's configuration, hooks, and signing.
export GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_NOSYSTEM=1
export GIT_AUTHOR_NAME=test GIT_AUTHOR_EMAIL=test@example.com
export GIT_COMMITTER_NAME=test GIT_COMMITTER_EMAIL=test@example.com

fail() { echo "result-verification fixture failed: $1" >&2; status=1; }

# expect EXIT "MESSAGE" ARGS...: the check exits EXIT and prints MESSAGE.
expect() {
  local want="$1" message="$2"; shift 2
  local got
  output="$(sh "$check" "$@" 2>&1)"; got=$?
  if [ "$got" -ne "$want" ]; then
    fail "check-ownership.sh $* exited $got, want $want. Output: $output"
  elif ! grep -qF -- "$message" <<<"$output"; then
    fail "check-ownership.sh $* should print \"$message\". Output: $output"
  fi
}

# fresh NAME: a new repository with one commit; prints nothing, sets $repo and $base.
fresh() {
  repo="$work/$1"
  mkdir -p "$repo/src" "$repo/docs" "$repo/my dir"
  git -C "$repo" init -q
  printf 'build/\n' > "$repo/.gitignore"
  printf 'a\n' > "$repo/src/app.txt"
  printf 'a\n' > "$repo/docs/guide.md"
  printf 'a\n' > "$repo/my dir/notes.txt"
  git -C "$repo" add -A
  git -C "$repo" commit -q -m base
  base="$(git -C "$repo" rev-parse HEAD)"
}

fresh clean
expect 0 "No changes since" -C "$repo" "$base"
expect 0 "No changes since" -C "$repo" "$base" "src/*"
(cd "$repo" && sh "$check" "$base" >/dev/null) || fail "the check should work from inside the repository without -C"

fresh untracked
printf 'x\n' > "$repo/new.txt"
expect 1 "untracked    new.txt" -C "$repo" "$base"
expect 0 "inside the write boundary" -C "$repo" "$base" new.txt

fresh unstaged
printf 'b\n' >> "$repo/docs/guide.md"
expect 1 "uncommitted  docs/guide.md" -C "$repo" "$base" "src/*"
expect 0 "inside the write boundary" -C "$repo" "$base" "docs/"

fresh staged
printf 'b\n' >> "$repo/docs/guide.md"
git -C "$repo" add docs/guide.md
git -C "$repo" show HEAD:docs/guide.md > "$repo/docs/guide.md"
[ -z "$(git -C "$repo" diff --name-only HEAD -- docs/guide.md)" ] || fail "fixture setup: the change should be staged only"
expect 1 "uncommitted  docs/guide.md" -C "$repo" "$base" "src/*"

fresh committed
printf 'b\n' >> "$repo/src/app.txt"
printf 'b\n' >> "$repo/docs/guide.md"
git -C "$repo" commit -q -am change
expect 1 "committed    docs/guide.md" -C "$repo" "$base" "src/*"
grep -qF "src/app.txt" <<<"$output" && fail "src/app.txt is inside src/* and must not be reported"
expect 0 "inside the write boundary" -C "$repo" "$base" "src/*" docs/guide.md
expect 0 "inside the write boundary" -C "$repo" "$base" "./src/*" "./docs/*"

fresh changed-back
printf 'b\n' >> "$repo/docs/guide.md"
git -C "$repo" commit -q -am touch
git -C "$repo" revert --no-edit HEAD >/dev/null
[ -z "$(git -C "$repo" diff --name-only "$base" HEAD)" ] || fail "fixture setup: the revert should leave no net change"
expect 1 "committed    docs/guide.md" -C "$repo" "$base"

fresh deleted
git -C "$repo" rm -q docs/guide.md
expect 1 "uncommitted  docs/guide.md" -C "$repo" "$base" "src/*"

fresh spaces
printf 'b\n' >> "$repo/my dir/notes.txt"
expect 0 "inside the write boundary" -C "$repo" "$base" "my dir/*"
expect 1 "my dir/notes.txt" -C "$repo" "$base" "src/*"

fresh ignored
mkdir -p "$repo/build"
printf 'x\n' > "$repo/build/out.bin"
expect 0 "No changes since" -C "$repo" "$base"
expect 1 "untracked    build/out.bin" --ignored -C "$repo" "$base"

fresh damaged-index
printf 'outside change\n' >> "$repo/docs/guide.md"
printf 'broken index\n' > "$repo/.git/index"
expect 2 "Git inspection failed" -C "$repo" "$base" "src/*"

fresh rewritten
git -C "$repo" checkout -q -b side
printf 'b\n' >> "$repo/src/app.txt"
git -C "$repo" commit -q -am side
side="$(git -C "$repo" rev-parse HEAD)"
git -C "$repo" checkout -q -
git -C "$repo" reset -q --hard "$base"
printf 'c\n' >> "$repo/src/app.txt"
git -C "$repo" commit -q -am other
expect 1 "HEAD does not descend from" -C "$repo" "$side" "src/*"

expect 2 "usage:" -C "$work/clean"
expect 2 "base revision not found" -C "$work/clean" no-such-revision
expect 2 "not inside a git working tree" -C "$work" HEAD
expect 2 "is absolute" -C "$work/clean" HEAD /etc/passwd
expect 2 "unknown option" --bogus HEAD

if command -v dash >/dev/null 2>&1; then
  dash "$check" -C "$work/committed" "$(git -C "$work/committed" rev-parse HEAD~1)" "src/*" "docs/*" >/dev/null \
    || fail "the check should pass under dash"
fi

[ "$status" -eq 0 ] && echo "check-ownership.sh fixtures behave as expected."
exit "$status"
