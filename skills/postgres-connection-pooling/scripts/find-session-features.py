#!/usr/bin/env python3
"""Find session-level PostgreSQL features in code that runs on a transaction-mode pooler.

Usage: find-session-features.py PATH...
       find-session-features.py --help

Pass only the files or directories whose connections go through a transaction-pooled
URL (PgBouncer transaction mode, a provider's pooled endpoint). Each PATH is scanned
recursively, skipping .git, node_modules, target, dist, build, and vendor.

Flags, with the fix for each:
  session SET / RESET            use SET LOCAL inside the transaction, or ALTER ROLE ... SET
  set_config(..., false)         pass true (transaction-local)
  LISTEN                         listen on a direct connection
  session advisory locks         pg_advisory_xact_lock, or a direct connection
  SQL PREPARE / DEALLOCATE       protocol-level prepared statements, if the pooler supports them
  DECLARE ... WITH HOLD          a cursor inside one transaction, or a direct connection
  temporary table kept past one transaction   ON COMMIT DROP, or a direct connection
  LOAD                           a direct connection
A line containing "pooler-ok:" followed by a reason is not reported.

Requires Python 3.12+ and the standard library.
This is a heuristic over text: it reads statement starts after a quote, backtick,
parenthesis, or semicolon, across line breaks. It cannot see which URL a code path
uses. Confirm each finding.
Output: "path:line: feature: fix" lines on stdout.
Exit: 0 none found, 1 findings, 2 usage or unreadable/empty scope. Reads only; writes nothing.
"""

import os
import re
import sys

SKIP_DIRS = {".git", "node_modules", "target", "dist", "build", "vendor", ".venv", "__pycache__"}
START = r"(?:\A|[`'\";(]|\bsql\s*`)\s*"
RULES = [
    ("session SET", START + r"(?P<k>SET\s+(?!LOCAL\b)(?!TRANSACTION\b)(?:SESSION\s+CHARACTERISTICS\s+AS\s+TRANSACTION\b|(?:SESSION\s+(?!CHARACTERISTICS\b))?(?:ROLE\b|AUTHORIZATION\b|TIME\s+ZONE\b|[A-Za-z_][\w.]*\s*(?:=|\bTO\b))))",
     "use SET LOCAL inside the transaction, or ALTER ROLE ... SET for a role default"),
    ("RESET", START + r"(?P<k>RESET\s+(?:ALL\b|[A-Za-z_][\w.]*))",
     "drop the RESET; SET LOCAL settings end with the transaction"),
    ("session set_config", r"(?P<k>\bset_config\s*\([^)]*,\s*false\s*\))",
     "pass true as the third argument so the setting is transaction-local"),
    ("LISTEN", START + r"(?P<k>LISTEN\s+[\"\w])",
     "run LISTEN on a dedicated direct connection"),
    ("session advisory lock", r"(?P<k>\bpg_(?:try_)?advisory_(?:un)?lock(?:_shared)?\s*\()",
     "use pg_advisory_xact_lock inside the transaction, or a direct connection"),
    ("SQL PREPARE", START + r"(?P<k>PREPARE\s+(?!TRANSACTION\b)\w+|DEALLOCATE\b)",
     "use the driver's protocol-level prepared statements, after checking pooler support"),
    ("cursor WITH HOLD", r"(?P<k>\bWITH\s+HOLD\b)",
     "keep the cursor inside one transaction, or use a direct connection"),
    ("temporary table", START + r"(?P<k>CREATE\s+(?:(?:GLOBAL|LOCAL)\s+)?TEMP(?:ORARY)?\s+TABLE\b)(?![^;`'\"]*ON\s+COMMIT\s+DROP)",
     "add ON COMMIT DROP and use it within one transaction, or use a direct connection"),
    ("LOAD", START + r"(?P<k>LOAD\s+')",
     "run LOAD on a direct connection"),
]
RULES = [(feature, re.compile(pattern, re.I), fix) for feature, pattern, fix in RULES]


def files(paths):
    for path in paths:
        if os.path.isfile(path):
            yield path
            continue
        for root, dirs, names in os.walk(path):
            dirs[:] = sorted(d for d in dirs if d not in SKIP_DIRS)
            for name in sorted(names):
                yield os.path.join(root, name)


def scan(path):
    try:
        with open(path, encoding="utf-8") as handle:
            text = handle.read()
    except UnicodeDecodeError:
        return []
    lines = text.splitlines()
    found = []
    for feature, pattern, fix in RULES:
        for match in pattern.finditer(text):
            number = text.count("\n", 0, match.start("k")) + 1
            if not re.search(r"pooler-ok:\s*\S", lines[number - 1]):
                found.append((number, f"{path}:{number}: {feature}: {fix}"))
    return [line for _, line in sorted(found)]


def main(argv):
    if argv in (["--help"], ["-h"]):
        print(__doc__.strip())
        return 0
    if not argv or any(arg.startswith("-") for arg in argv):
        print("usage: find-session-features.py PATH... (see --help)", file=sys.stderr)
        return 2
    missing = [path for path in argv if not os.path.exists(path)]
    if missing:
        print(f"find-session-features: no such path: {', '.join(missing)}", file=sys.stderr)
        return 2
    findings, scanned = [], 0
    try:
        for path in files(argv):
            scanned += 1
            findings.extend(scan(path))
    except OSError as error:
        print(f"find-session-features: {error}", file=sys.stderr)
        return 2
    if not scanned:
        print("find-session-features: no files scanned; supply the actual pooled code paths", file=sys.stderr)
        return 2
    for finding in findings:
        print(finding)
    print(f"{len(findings)} session feature(s) found on pooled paths", file=sys.stderr)
    return 1 if findings else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
