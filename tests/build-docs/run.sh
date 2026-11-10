#!/bin/sh
# Offline documentation generation and reject/accept/repeat fixtures.
set -eu
cd "$(dirname "$0")/../.."
exec uv run --quiet --python '>=3.12' python tests/build-docs/test_build_docs.py
