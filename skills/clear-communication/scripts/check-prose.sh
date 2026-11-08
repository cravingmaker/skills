#!/usr/bin/env bash
# Lint prose with the ClearCommunication Vale style.
#
# Usage: check-prose.sh [--config FILE] FILE... | -
#   FILE...        Markdown or text files to check.
#   -              Read Markdown from stdin.
#   --config FILE  Use another Vale config (for example, one that enables EmDash).
#
# Exit status: 0 no errors (suggestions and warnings are advice), 1 errors found,
# 2 usage problem or Vale missing.
set -euo pipefail

PINNED_VALE_VERSION=3.26.0
skill_dir="$(cd "$(dirname "$0")/.." && pwd)"
config="$skill_dir/assets/vale/vale.ini"

if [ "${1:-}" = "--config" ]; then
  config="${2:?--config needs a file}"
  shift 2
fi

if [ "$#" -eq 0 ]; then
  echo "usage: check-prose.sh [--config FILE] FILE... | -" >&2
  exit 2
fi

vale_bin="${VALE_BIN:-vale}"
if ! command -v "$vale_bin" >/dev/null 2>&1; then
  echo "error: Vale is not installed. Install Vale $PINNED_VALE_VERSION (https://vale.sh/docs/install) or set VALE_BIN." >&2
  exit 2
fi

installed="$("$vale_bin" --version | awk '{print $NF}')"
if [ "$installed" != "$PINNED_VALE_VERSION" ]; then
  echo "warning: Vale $installed found; this style is tested with $PINNED_VALE_VERSION." >&2
fi

if [ "$1" = "-" ]; then
  exec "$vale_bin" --config="$config" --output=line --ext=.md
fi
exec "$vale_bin" --config="$config" --output=line "$@"
