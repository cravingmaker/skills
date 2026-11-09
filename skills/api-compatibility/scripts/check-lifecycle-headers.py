#!/usr/bin/env python3
"""Check a canonical emission profile for Deprecation and Sunset response fields.

Python 3.12+, standard library only. Read-only; no network or host inspection.
Input: a nonempty JSON object containing only Deprecation and/or Sunset string
values, with case-insensitive names. Extract these fields from a safe fixture.
Profile: Deprecation is a bare Structured Field Date, with no parameters;
Sunset is IMF-fixdate with GMT. This is not a general Structured Fields parser.
Output: JSON findings on stdout; input diagnostics on stderr, without values.
Exit: 0 pass, 1 profile or chronology findings, 2 usage or unreadable input.
"""

import argparse
import calendar
import json
import re
import sys
from email.utils import format_datetime, parsedate_to_datetime
from pathlib import Path

DATE = re.compile(r"@(-?[0-9]{1,15})", re.ASCII)
HTTP_DATE = re.compile(
    r"(Mon|Tue|Wed|Thu|Fri|Sat|Sun), [0-9]{2} "
    r"(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec) "
    r"[0-9]{4} [0-9]{2}:[0-9]{2}:[0-9]{2} GMT", re.ASCII
)


def unique_headers(pairs):
    result = {}
    for key, value in pairs:
        name = key.lower()
        if name in result:
            raise ValueError("duplicate field")
        result[name] = value
    return result


def check(headers):
    if not isinstance(headers, dict) or not headers or set(headers) - {"deprecation", "sunset"}:
        raise ValueError("extract only the lifecycle fields into a nonempty JSON object")
    findings, times = [], {}
    for name, raw in headers.items():
        value = raw.strip(" \t") if isinstance(raw, str) else ""
        if name == "deprecation":
            match = DATE.fullmatch(value)
            if match:
                times[name] = int(match[1])
            else:
                findings.append({"field": name, "rule": "date-profile", "fix": "Emit a bare Structured Field Date (@ followed by integer seconds), without parameters."})
        else:
            try:
                if not HTTP_DATE.fullmatch(value):
                    raise ValueError("not the emission profile")
                date = parsedate_to_datetime(value)
                if format_datetime(date, usegmt=True) != value:
                    raise ValueError("noncanonical date or wrong weekday")
                times[name] = calendar.timegm(date.utctimetuple())
            except (ValueError, TypeError, OverflowError):
                findings.append({"field": name, "rule": "http-date-profile", "fix": "Emit a valid IMF-fixdate with its correct weekday and GMT timezone."})
    if set(times) == {"deprecation", "sunset"} and times["sunset"] < times["deprecation"]:
        findings.append({"field": "sunset", "rule": "chronology", "fix": "Move Sunset to the Deprecation instant or later."})
    return {"checked": len(headers), "findings": findings}


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("headers", type=Path, help="JSON with only Deprecation and/or Sunset; exclude other headers")
    args = parser.parse_args()
    if sys.version_info < (3, 12):
        print("error: use Python 3.12 or later to run check-lifecycle-headers.py", file=sys.stderr)
        return 2
    try:
        with args.headers.open(encoding="utf-8") as source:
            headers = json.load(source, object_pairs_hook=unique_headers)
        report = check(headers)
    except (OSError, UnicodeError, ValueError, RecursionError):
        print("error: pass readable UTF-8 JSON containing only unique lifecycle field names; see --help", file=sys.stderr)
        return 2
    print(json.dumps(report, indent=2))
    return 1 if report["findings"] else 0


if __name__ == "__main__":
    sys.exit(main())
