#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
python3 -B -c 'from word_count import count_words; assert count_words("three short words") == 3; assert count_words("") == 0'
