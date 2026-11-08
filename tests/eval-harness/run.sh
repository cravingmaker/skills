#!/usr/bin/env bash
# Deterministic preparation and isolation checks. Never call a model or read auth.
set -euo pipefail
here="$(cd "$(dirname "$0")" && pwd)"
exec uv run --script "$here/check.py"
