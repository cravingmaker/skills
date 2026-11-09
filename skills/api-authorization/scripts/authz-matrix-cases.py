#!/usr/bin/env python3
"""Expand explicit authorization cases, or compare their observed results.

Python 3.12+, standard library only. Read-only; no requests or database access.
CSV columns: role,tenant,operation,object,property,entrypoint,identity,expect.
The first six columns hold synthetic labels separated by | for expansion.
identity is one declared runtime identity per row; expect is allow or deny.
No blanks, wildcards or repeated cells. Include an allow control and a denial.
Output: JSON on stdout; input diagnostics on stderr without input labels.
With --results FILE, require CSV columns id,observed,identity. Every generated
ID must occur once, with its expected outcome and observed runtime identity.
IDs bind the cell, expected outcome and identity; changed cases need new results.
This checks recorded evidence, not the truth of a test runner's assertions.
Exit: 0 pass, 1 matrix/result findings, 2 usage, unreadable input or bad schema.
"""

import argparse
import csv
import hashlib
import itertools
import json
import re
import sys
from pathlib import Path

DIMENSIONS = ("role", "tenant", "operation", "object", "property", "entrypoint")
COLUMNS = (*DIMENSIONS, "identity", "expect")
LABEL = re.compile(r"[A-Za-z0-9][A-Za-z0-9_.:-]{0,79}", re.ASCII)


def positive_integer(value):
    number = int(value)
    if number <= 0:
        raise argparse.ArgumentTypeError("choose a positive --max-cases value")
    return number


def expand(source, limit):
    reader = csv.DictReader(source, strict=True)
    if reader.fieldnames != list(COLUMNS):
        raise ValueError("use the exact CSV columns from --help")
    cases, seen, errors, expectations = [], set(), [], set()
    for row_index, row in enumerate(reader, 2):
        if None in row or any(value is None for value in row.values()):
            raise ValueError("each row must have exactly eight fields")
        expect, identity = row["expect"].strip(), row["identity"].strip()
        if expect not in {"allow", "deny"}:
            errors.append(f"row {row_index}: choose one expect value, allow or deny")
            continue
        if not LABEL.fullmatch(identity):
            errors.append(f"row {row_index}: declare one synthetic runtime identity")
            continue
        dimensions = [[part.strip() for part in row[name].split("|")] for name in DIMENSIONS]
        if any(not all(LABEL.fullmatch(part) for part in parts) or len(set(parts)) != len(parts) for parts in dimensions):
            errors.append(f"row {row_index}: use unique synthetic labels per dimension; fill blanks and expand wildcards explicitly")
            continue
        count = 1
        for parts in dimensions:
            count *= len(parts)
        if len(cases) + count > limit:
            errors.append(f"row {row_index}: expansion exceeds --max-cases; narrow the matrix or set an explicit larger bound")
            break
        expectations.add(expect)
        for values in itertools.product(*dimensions):
            if values in seen:
                errors.append(f"row {row_index}: repeated cell; keep one expectation and runtime identity for each combination")
                continue
            seen.add(values)
            bound = json.dumps([*values, identity, expect], separators=(",", ":")).encode("utf-8")
            case_id = "case-" + hashlib.sha256(bound).hexdigest()
            cases.append({"id": case_id, **dict(zip(DIMENSIONS, values)), "identity": identity, "expect": expect})
    if not cases:
        errors.append("matrix is empty; add the real entry points with explicit expectations")
    if expectations != {"allow", "deny"}:
        errors.append("include both an allowed control and a denied case; a deny-all implementation must fail")
    return cases, errors


def check_results(cases, source):
    reader = csv.DictReader(source, strict=True)
    if reader.fieldnames != ["id", "observed", "identity"]:
        raise ValueError("results need the exact id,observed,identity header")
    expected = {case["id"]: case for case in cases}
    seen, findings = set(), []
    for row_index, row in enumerate(reader, 2):
        if None in row or any(value is None for value in row.values()):
            raise ValueError("each result row needs exactly three fields")
        if row_index > len(cases) + 2:
            findings.append({"row": row_index, "rule": "result-bound", "fix": "Keep exactly one result per generated case."})
            break
        case_id = row["id"].strip()
        case = expected.get(case_id)
        if case_id in seen:
            findings.append({"row": row_index, "rule": "duplicate-result", "fix": "Keep one observed result per case."})
            continue
        seen.add(case_id)
        if case is None:
            findings.append({"row": row_index, "rule": "unknown-result", "fix": "Regenerate cases and rerun tests for this exact policy."})
            continue
        observed = row["observed"].strip()
        if observed not in {"allow", "deny"}:
            findings.append({"case": case_id, "rule": "bad-result", "fix": "Record allow or deny from the real entry-point assertions."})
        elif observed != case["expect"]:
            rule = "denial-failed" if observed == "allow" else "over-denied"
            findings.append({"case": case_id, "rule": rule, "fix": "Fix the observed access decision and rerun the actual entry point."})
        if row["identity"].strip() != case["identity"]:
            findings.append({"case": case_id, "rule": "wrong-identity", "fix": "Exercise the declared runtime identity and record its observed label."})
    for case_id in expected.keys() - seen:
        findings.append({"case": case_id, "rule": "missing-result", "fix": "Run the missing case through its real entry point."})
    findings.sort(key=lambda item: (item.get("case", ""), item.get("row", 0), item["rule"]))
    return {"checked": len(cases), "findings": findings}


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("matrix", type=Path, help="CSV with synthetic fixture labels, never credentials or personal records")
    parser.add_argument("--results", type=Path, help="CSV of actual id,observed,identity assertions; omit to expand cases")
    parser.add_argument("--max-cases", type=positive_integer, default=10000, help="local expansion bound (default: 10000); this is not a service limit")
    args = parser.parse_args()
    if sys.version_info < (3, 12):
        print("error: use Python 3.12 or later to run authz-matrix-cases.py", file=sys.stderr)
        return 2
    try:
        with args.matrix.open(encoding="utf-8", newline="") as source:
            cases, errors = expand(source, args.max_cases)
        if errors:
            for error in errors:
                print(f"FAIL: {error}", file=sys.stderr)
            return 1
        if args.results is None:
            report = {"count": len(cases), "cases": cases}
        else:
            with args.results.open(encoding="utf-8", newline="") as source:
                report = check_results(cases, source)
    except (OSError, UnicodeError, ValueError, csv.Error):
        print("error: pass readable UTF-8 CSV with the exact headers and fields; see --help", file=sys.stderr)
        return 2
    print(json.dumps(report, indent=2))
    return 1 if report.get("findings") else 0


if __name__ == "__main__":
    sys.exit(main())
