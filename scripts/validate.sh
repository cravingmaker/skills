#!/usr/bin/env bash
# Validate the template and every skill:
#   1. skills-ref, the Agent Skills reference validator, pinned to a commit.
#   2. scripts/check-skills.py, the repository rules skills-ref does not enforce.
#   3. Fixture tests for the checker and for the ClearCommunication Vale style.
#   4. The ClearCommunication style on this repository's own docs.
# Requires uv. The prose tests need Vale 3.26.0; set REQUIRE_VALE=1 to fail without it (CI does).
set -euo pipefail

cd "$(dirname "$0")/.."

SKILLS_REF_REVISION=f130f348f502d9804278a617f86929846896d2e9
SKILLS_REF="git+https://github.com/agentskills/agentskills@${SKILLS_REF_REVISION}#subdirectory=skills-ref"

if ! command -v uvx >/dev/null 2>&1; then
  echo "error: uvx not found. Install uv: https://docs.astral.sh/uv/" >&2
  exit 1
fi

shopt -s nullglob
dirs=(template skills/*/)
dirs=("${dirs[@]%/}")

status=0
for dir in "${dirs[@]}"; do
  uvx --quiet --from "$SKILLS_REF" skills-ref validate "$dir" || status=1
done

scripts/check-skills.py "${dirs[@]}" || status=1
tests/check-skills/run.sh || status=1

if command -v "${VALE_BIN:-vale}" >/dev/null 2>&1; then
  tests/clear-communication/run.sh || status=1
  skills/clear-communication/scripts/check-prose.sh README.md AGENTS.md skills/*/SKILL.md skills/*/references/*.md skills/*/evals/*.md || status=1
elif [ "${REQUIRE_VALE:-0}" = "1" ]; then
  echo "error: Vale is required (REQUIRE_VALE=1) but not installed." >&2
  status=1
else
  echo "Skipped the prose tests: Vale is not installed."
fi

exit "$status"
