#!/usr/bin/env bash
# Validate every skill (and the template) against the Agent Skills spec
# using the reference validator, skills-ref. Requires uv.
set -euo pipefail

cd "$(dirname "$0")/.."

SKILLS_REF="git+https://github.com/agentskills/agentskills#subdirectory=skills-ref"

if ! command -v uvx >/dev/null 2>&1; then
  echo "error: uvx not found. Install uv: https://docs.astral.sh/uv/" >&2
  exit 1
fi

shopt -s nullglob
dirs=(template skills/*/)

status=0
for dir in "${dirs[@]}"; do
  dir="${dir%/}"
  if uvx --quiet --from "$SKILLS_REF" skills-ref validate "$dir"; then
    :
  else
    status=1
  fi
done

if [ "${#dirs[@]}" -eq 1 ]; then
  echo "No skills in skills/ yet; validated the template only."
fi

exit "$status"
