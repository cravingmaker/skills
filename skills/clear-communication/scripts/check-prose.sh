#!/usr/bin/env bash
# Lint prose with the ClearCommunication Vale style.
#
# Usage: check-prose.sh [--config FILE] FILE... | -
#   FILE...        Markdown files or .txt drafts parsed as Markdown.
#   -              Read Markdown from stdin.
#   --config FILE  Use another Vale config (for example, one that enables EmDash).
#
# Exit status: 0 no errors (suggestions and warnings are advice), 1 errors found,
# 2 usage problem or Vale missing.
set -euo pipefail

PINNED_VALE_VERSION=3.26.0
skill_dir="$(cd "$(dirname "$0")/.." && pwd)"
config="$skill_dir/assets/vale/vale.ini"

case "${1:-}" in
  --help|-h)
    echo "usage: check-prose.sh [--config FILE] FILE... | -"
    echo "Lint prose with the ClearCommunication Vale style. Exit: 0 no errors, 1 errors, 2 usage or Vale missing."
    exit 0 ;;
esac

if [ "${1:-}" = "--config" ]; then
  if [ "$#" -lt 2 ] || [ -z "$2" ]; then
    echo "error: --config needs a file" >&2
    exit 2
  fi
  config="$2"
  shift 2
fi

if [ "$#" -eq 0 ]; then
  echo "usage: check-prose.sh [--config FILE] FILE... | -" >&2
  exit 2
fi

if [ "$1" = "-" ]; then
  if [ "$#" -ne 1 ]; then
    echo "error: use - alone for stdin, or provide file paths" >&2
    exit 2
  fi
else
  files=()
  for file in "$@"; do
    if [ "$file" = "-" ] || [ ! -f "$file" ]; then
      echo "error: expected an existing file, got: $file" >&2
      exit 2
    fi
    case "$file" in
      /*) files+=("$file") ;;
      *) files+=("$PWD/$file") ;;
    esac
  done
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
exec "$vale_bin" --config="$config" --output=line "${files[@]}"
