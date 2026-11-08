#!/usr/bin/env bash
# Offline reject/accept/repeat fixtures; no model calls or real host configuration.
set -euo pipefail
cd "$(dirname "$0")/../.."
uv run --quiet --script tests/adoption-tooling/check.py
