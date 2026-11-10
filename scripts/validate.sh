#!/usr/bin/env bash
# Validate the template and every skill:
#   1. skills-ref, the Agent Skills reference validator, pinned to a commit.
#   2. scripts/check-skills.py, the repository rules skills-ref does not enforce.
#   3. Fixture tests for the checker and for the ClearCommunication Vale style.
#   4. The catalog: entries, dependencies, reserved names, generated install profiles,
#      and the installer, with fixture tests.
#      The eval harness's offline isolation tests (no model calls).
#   5. Freshness: skills whose metadata.verified date is older than six months (report only).
#   6. zizmor, a static analyzer for the GitHub Actions workflows.
#   7. The ClearCommunication style on this repository's own docs.
# Requires uv. The prose tests need Vale 3.26.0; set REQUIRE_VALE=1 to fail without it (CI does).
set -euo pipefail

cd "$(dirname "$0")/.."

SKILLS_REF_REVISION=f130f348f502d9804278a617f86929846896d2e9
SKILLS_REF="git+https://github.com/agentskills/agentskills@${SKILLS_REF_REVISION}#subdirectory=skills-ref"
# Pinned releases at least seven days old, matching the user's dependency policy.
ZIZMOR_VERSION=1.31.1

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

scripts/check-catalog.py || status=1
scripts/build-profiles.py --check || status=1
scripts/build-host-config.py --check || status=1
tests/adoption-tooling/run.sh || status=1
tests/check-catalog/run.sh || status=1
tests/install/run.sh || status=1
tests/eval-harness/run.sh || status=1
uv run --quiet --script tests/discovery-cost.py || status=1

# Each skill's own tests (tests/<skill>/run.sh); the Vale-dependent one runs below.
for test in tests/*/run.sh; do
  skill="$(basename "$(dirname "$test")")"
  [ -d "skills/$skill" ] && [ "$skill" != clear-communication ] || continue
  "$test" || status=1
done
scripts/check-freshness.py || status=1
uvx --quiet "zizmor@${ZIZMOR_VERSION}" --offline .github/workflows || status=1

if command -v "${VALE_BIN:-vale}" >/dev/null 2>&1; then
  tests/clear-communication/run.sh || status=1
  skills/clear-communication/scripts/check-prose.sh README.md AGENTS.md docs/*.md catalog/*.md skills/*/SKILL.md skills/*/references/*.md skills/*/evals/*.md || status=1
elif [ "${REQUIRE_VALE:-0}" = "1" ]; then
  echo "error: Vale is required (REQUIRE_VALE=1) but not installed." >&2
  status=1
else
  echo "Skipped the prose tests: Vale is not installed."
fi

exit "$status"
