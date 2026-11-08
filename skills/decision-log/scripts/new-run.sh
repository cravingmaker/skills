#!/bin/sh
# POSIX shell and standard utilities. Preview by default; --apply creates files.
# Exit: 0 success, 1 findings/write failure, 2 usage. No network or agent calls.
set -eu

usage() {
  echo "usage: new-run.sh [--dry-run|--apply] RUN_DIR" >&2
  echo "Preview is the default. --apply creates missing files and preserves existing records." >&2
}

mode=preview
case "${1:-}" in
  --help|-h) usage; exit 0 ;;
  --apply) mode=apply; shift ;;
  --dry-run) shift ;;
esac
if [ "$#" -ne 1 ] || [ -z "$1" ]; then usage; exit 2; fi
case "$1" in -*) usage; exit 2 ;; esac
case "$1" in
  /*) run_dir=$1 ;;
  *) run_dir=$PWD/$1 ;;
esac
# Remove trailing slashes so an existing symlink remains visible to -L.
while [ "$run_dir" != / ] && [ "${run_dir%/}" != "$run_dir" ]; do run_dir=${run_dir%/}; done
script_dir=$(CDPATH='' cd -P "$(dirname "$0")" && pwd)
assets=$script_dir/../assets

fail() { echo "FAIL: $*" >&2; exit 1; }
check_dir() {
  [ ! -L "$1" ] || fail "$1 is a symlink; select a real run directory"
  if [ -e "$1" ] && [ ! -d "$1" ]; then fail "$1 is a file; select a directory"; fi
}

# Check all collisions before the first write.
check_dir "$run_dir"
for directory in raw briefs drafts; do check_dir "$run_dir/$directory"; done
for file in PLAN.md LOG.md DECISIONS.md; do
  [ -f "$assets/$file" ] || fail "missing template $assets/$file; reinstall the complete skill"
  [ ! -L "$run_dir/$file" ] || fail "$run_dir/$file is a symlink; reconcile it before scaffolding"
  if [ -e "$run_dir/$file" ] && [ ! -f "$run_dir/$file" ]; then
    fail "$run_dir/$file is not a regular file; reconcile it before scaffolding"
  fi
done

if [ "$mode" = apply ]; then
  mkdir -p "$run_dir/raw" "$run_dir/briefs" "$run_dir/drafts" || fail "cannot create $run_dir; check path permissions"
fi
for file in PLAN.md LOG.md DECISIONS.md; do
  if [ -f "$run_dir/$file" ]; then
    echo "KEEP: $run_dir/$file"
  elif [ "$mode" = preview ]; then
    echo "CREATE: $run_dir/$file"
  else
    # noclobber also protects a file that appears after preflight.
    (set -C; cat "$assets/$file" > "$run_dir/$file") || fail "cannot create $run_dir/$file; inspect it and reconcile before retrying"
    echo "CREATED: $run_dir/$file"
  fi
done
if [ "$mode" = preview ]; then
  echo "PREVIEW: raw/, briefs/, drafts/; rerun with --apply to scaffold $run_dir"
else
  echo "READY: $run_dir; populate PLAN.md before dispatch; no result reports were created"
fi
