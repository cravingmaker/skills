#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.12"
# dependencies = ["pyyaml==6.0.3"]
# ///
"""Compare one skill example with and without the candidate in isolated sessions.

Exit status: 0 valid comparison (or dry run), 1 invalid/failed comparison,
2 usage error. A valid comparison can still demonstrate a skill failure.
"""

import sys

sys.dont_write_bytecode = True

from evalharness.runner import main


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
