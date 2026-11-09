#!/bin/sh
set -eu
cd "$(dirname "$0")/.."
python3 -B scripts/tooling.py check
