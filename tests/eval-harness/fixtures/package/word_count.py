#!/usr/bin/env python3
"""Count words in one command-line argument."""

import sys


def count_words(text: str) -> int:
    return len(text.split())


if __name__ == "__main__":
    print(count_words(sys.argv[1]))
