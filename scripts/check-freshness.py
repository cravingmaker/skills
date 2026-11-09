#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.12"
# dependencies = ["pyyaml==6.0.3"]
# ///
"""List skills whose version-specific facts are due for re-verification.

A skill that states versions records metadata.verified as "YYYY-MM". This
script reports every skill verified more than MONTHS months ago (default 6) and
fails only on a malformed date, so stale skills are visible without blocking CI.

Usage: check-freshness.py [--months N] [--root DIR]
Exit status: 0 on success (stale skills are reported, not failed), 1 on a malformed date, 2 on usage errors.
"""

import argparse
import re
import sys
from datetime import date
from pathlib import Path

import skillcatalog

VERIFIED = re.compile(r"(\d{4})-(0[1-9]|1[0-2])")


def main(arguments: list[str]) -> int:
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("--months", type=int, default=6)
    parser.add_argument("--root", default=".")
    try:
        options = parser.parse_args(arguments)
    except SystemExit:
        print(__doc__.strip(), file=sys.stderr)
        return 2

    today = date.today()
    current = today.year * 12 + today.month
    repo = skillcatalog.load(Path(options.root))
    malformed, stale = [], []
    for name, frontmatter in sorted(repo.frontmatter.items()):
        metadata = frontmatter.get("metadata") if isinstance(frontmatter.get("metadata"), dict) else {}
        value = metadata.get("verified")
        if value is None:
            continue
        match = VERIFIED.fullmatch(value) if isinstance(value, str) else None
        if match is None:
            malformed.append(f"{name}: metadata.verified must be a quoted \"YYYY-MM\", got {value!r}")
            continue
        age = current - (int(match.group(1)) * 12 + int(match.group(2)))
        if age > options.months:
            stale.append(f"{name}: verified {value}, {age} months ago")

    for line in malformed:
        print(f"  - {line}")
    if stale:
        print(f"Due for re-verification (older than {options.months} months):")
        for line in stale:
            print(f"  - {line}")
    else:
        print("Freshness: no skill is due for re-verification.")
    return 1 if malformed else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
