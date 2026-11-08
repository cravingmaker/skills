#!/bin/sh
# Check that a worker's changes since a base revision stay inside its write boundary.
#
# Usage: check-ownership.sh [--ignored] [-C DIR] BASE [GLOB...]
#   BASE       The revision the worker started from (commit, branch, or tag).
#   GLOB...    Paths the worker may change, relative to the repository root.
#              Shell patterns where * also matches /, so dir/* covers the whole
#              tree under dir; a trailing / means the whole directory.
#              No GLOB means a read-only check: any change fails.
#   --ignored  Also count new files that .gitignore hides (build output, caches).
#   -C DIR     Run in DIR instead of the current directory.
#
# Counted as changes: every path touched by a commit in BASE..HEAD (even when a
# later commit changes it back), committed, staged, and unstaged differences from
# BASE, and untracked files. Files outside the repository are not seen.
# Paths git must quote (tabs, newlines, quotes) never match a glob, so they fail.
#
# Exit status: 0 every change is inside the boundary, 1 a change is outside it or
# HEAD does not descend from BASE, 2 usage error. Reads only; needs git.
set -eu

usage() {
  echo "usage: check-ownership.sh [--ignored] [-C DIR] BASE [GLOB...]" >&2
  exit 2
}

dir=.
ignored=0
while [ "$#" -gt 0 ]; do
  case $1 in
    --ignored) ignored=1; shift ;;
    -C)
      [ "$#" -ge 2 ] || usage
      dir=$2; shift 2 ;;
    --) shift; break ;;
    -*) echo "error: unknown option $1" >&2; usage ;;
    *) break ;;
  esac
done
[ "$#" -ge 1 ] || usage
base=$1
shift

command -v git >/dev/null 2>&1 || { echo "error: git not found. Install git and rerun." >&2; exit 2; }
top=$(git -C "$dir" rev-parse --show-toplevel 2>/dev/null) || {
  echo "error: $dir is not inside a git working tree. Run in the worker's checkout or pass -C DIR." >&2
  exit 2
}
base_commit=$(git -C "$top" rev-parse --verify --quiet "$base^{commit}") || {
  echo "error: base revision not found: $base. Record the worker's start with 'git rev-parse HEAD' before dispatch and pass it." >&2
  exit 2
}

for glob in "$@"; do
  case $glob in
    /*) echo "error: $glob is absolute. Give globs relative to the repository root, $top." >&2; exit 2 ;;
    '') echo "error: an empty glob matches nothing. Remove it." >&2; exit 2 ;;
  esac
done

tmp=$(mktemp -d)
trap 'rm -rf "$tmp"' EXIT
g() { git -C "$top" -c core.quotePath=false "$@"; }

{
  g log --no-renames --name-only --format= "$base_commit..HEAD"
  g diff --no-renames --name-only "$base_commit" HEAD
} | sort -u > "$tmp/committed"
{
  g diff --no-renames --name-only HEAD
  g diff --no-renames --name-only --cached HEAD
} | sort -u > "$tmp/uncommitted"
{
  g ls-files --others --exclude-standard
  if [ "$ignored" -eq 1 ]; then g ls-files --others --ignored --exclude-standard; fi
} | sort -u > "$tmp/untracked"

: > "$tmp/outside"
changed=0
for kind in committed uncommitted untracked; do
  while IFS= read -r path; do
    [ -n "$path" ] || continue
    changed=$((changed + 1))
    inside=0
    for glob in "$@"; do
      glob=${glob#./}
      case $glob in */) glob="${glob}*" ;; esac
      # Unquoted on purpose: the glob is a pattern.
      # shellcheck disable=SC2254
      case $path in $glob) inside=1; break ;; esac
    done
    [ "$inside" -eq 1 ] || printf '  %-12s %s\n' "$kind" "$path" >> "$tmp/outside"
  done < "$tmp/$kind"
done

status=0
short=$(git -C "$top" rev-parse --short "$base_commit")
if ! git -C "$top" merge-base --is-ancestor "$base_commit" HEAD; then
  echo "HEAD does not descend from $base ($short): the history was rewritten or the base is wrong."
  echo "Fix: rerun with the revision the worker started from, or inspect what replaced the base."
  status=1
fi

if [ -s "$tmp/outside" ]; then
  if [ "$#" -eq 0 ]; then
    echo "Read-only check failed: changes since $base ($short):"
  else
    echo "Changes outside the write boundary since $base ($short):"
  fi
  cat "$tmp/outside"
  echo "Fix: revert these paths, or widen the brief's write boundary and record why in the run record."
  status=1
elif [ "$status" -eq 0 ]; then
  if [ "$changed" -eq 0 ]; then
    echo "No changes since $base ($short)."
  else
    echo "All changes since $base ($short) are inside the write boundary."
  fi
fi
exit "$status"
