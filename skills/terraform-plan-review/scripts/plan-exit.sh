#!/bin/sh
# Classify a captured plan -detailed-exitcode status; never invoke a command.
# Usage: sh plan-exit.sh STATUS
# Stdout: plan_changes=false|true for successful planning. Diagnostics: stderr.
# Exits: 0 successful planning (status 0 or 2), 1 engine error or unexpected
# numeric status, 2 usage. --help exits 0 without reading files or writing.
case "${1:-}" in
    --help|-h) sed -n '2,6p' "$0" | sed 's/^# \{0,1\}//'; exit 0 ;;
esac
if [ "$#" -ne 1 ]; then
    echo 'usage: plan-exit.sh STATUS; pass the captured plan status' >&2
    exit 2
fi
case "$1" in
    0) echo 'plan_changes=false' ;;
    2) echo 'plan_changes=true' ;;
    ''|*[!0-9]*) echo 'usage: plan-exit.sh STATUS; pass a numeric captured status' >&2; exit 2 ;;
    *) echo 'planning failed; inspect protected diagnostics and regenerate before review' >&2; exit 1 ;;
esac
