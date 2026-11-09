#!/usr/bin/env python3
"""Check nonempty JUnit results against an independent expected case selection.

Python 3.12+, standard library. Read-only local files; no database or network.
JSON counts on stdout, diagnostics on stderr; no report names, logs or errors
are echoed. Exits: 0 complete passing selection, 1 result findings, 2 invalid
input/usage. --help exits 0 without reading files or writing anything.
"""

import argparse
import json
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path


def tag(element):
    return element.tag.rsplit("}", 1)[-1]


def state(case):
    children = {tag(child) for child in case}
    states = {case.get(key, "").casefold() for key in ("status", "result")}
    supported = {"", "run", "passed", "success", "completed", "failed", "failure", "error",
                 "skipped", "notrun", "disabled", "suppressed"}
    if states - supported:
        raise ValueError("unknown runner status; normalize with the supported adapter")
    return ("failure" in children or bool(states & {"failed", "failure"}),
            "error" in children or "error" in states,
            "skipped" in children or bool(states & {"skipped", "notrun", "disabled", "suppressed"}))


def report(path):
    raw = path.read_bytes()
    if re.search(rb"<!\s*(?:DOCTYPE|ENTITY)\b", raw, re.I) or b"\x00" in raw:
        raise ValueError("DTD/entities or non-UTF-8 input")
    root = ET.fromstring(raw.decode("utf-8"))
    if tag(root) not in ("testsuite", "testsuites"):
        raise ValueError("expected JUnit")
    cases = [element for element in root.iter() if tag(element) == "testcase"]
    mismatches = 0
    for suite in root.iter():
        if tag(suite) not in ("testsuite", "testsuites"):
            continue
        nested = [element for element in suite.iter() if tag(element) == "testcase"]
        observed = {"tests": len(nested), "failures": sum(state(case)[0] for case in nested),
                    "errors": sum(state(case)[1] for case in nested),
                    "skipped": sum(state(case)[2] for case in nested)}
        for key, actual in observed.items():
            if key in suite.attrib:
                declared = suite.attrib[key]
                if re.fullmatch(r"[0-9]+", declared) is None:
                    raise ValueError("invalid counts")
                mismatches += int(int(declared) != actual)
        # Some adapters report setup failures directly on the suite.
        mismatches += sum(tag(child) in ("failure", "error") for child in suite)
    rows = []
    for case in cases:
        if any(tag(child) == "testcase" for child in list(case.iter())[1:]):
            raise ValueError("nested testcase")
        name = case.get("name", "")
        if not name.strip():
            raise ValueError("missing testcase name")
        failure, error, skipped = state(case)
        rows.append((case.get("classname", "") + "::" + name, failure, error, skipped))
    return rows, mismatches


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("reports", type=Path, nargs="+", help="fresh JUnit XML files for this run")
    parser.add_argument("--expected-file", type=Path, required=True,
                        help="nonempty JSON array of unique classname::name IDs chosen before the run")
    args = parser.parse_args()
    if sys.version_info < (3, 12):
        print("error: use Python 3.12+ to run check-results.py", file=sys.stderr)
        return 2
    try:
        expected = json.loads(args.expected_file.read_text(encoding="utf-8"))
        if not isinstance(expected, list) or not expected or any(
                not isinstance(value, str) or "::" not in value or not value.rsplit("::", 1)[1].strip()
                for value in expected):
            raise ValueError("invalid selection")
        if len(set(expected)) != len(expected):
            raise ValueError("duplicate expected ID")
        rows, mismatches = [], 0
        for path in args.reports:
            more, invalid = report(path)
            rows.extend(more)
            mismatches += invalid
        ids = [row[0] for row in rows]
        passing = {name for name, failed, error, skipped in rows if not (failed or error or skipped)}
        failed = sum(failed or error for _, failed, error, _ in rows)
        skipped = sum(skipped for _, _, _, skipped in rows)
        duplicates = len(ids) - len(set(ids))
        missing = len(set(expected) - passing)
        findings = []
        for condition, label in ((not rows, "empty_selection"), (not passing, "no_passing_cases"),
                                 (failed, "failed_cases"), (skipped, "skipped_cases"),
                                 (duplicates, "duplicate_cases"), (missing, "expected_cases_not_passed"),
                                 (mismatches, "suite_count_or_setup_error")):
            if condition:
                findings.append(label)
        result = {"cases": len(rows), "passed": sum(not (f or e or s) for _, f, e, s in rows),
                  "failed": failed, "skipped": skipped, "expected": len(expected),
                  "expected_not_passed": missing, "duplicates": duplicates,
                  "count_or_setup_errors": mismatches, "findings": findings}
    except (OSError, UnicodeError, ValueError, TypeError, ET.ParseError, RecursionError, OverflowError):
        print("error: supply UTF-8 JUnit XML without DTD/entities, valid counts, and a nonempty JSON selection of unique classname::name IDs", file=sys.stderr)
        return 2
    print(json.dumps(result, sort_keys=True))
    return int(bool(findings))


if __name__ == "__main__":
    sys.exit(main())
