#!/usr/bin/env python3
"""Check sanitized origin-server error examples, pairing HTTP status with body.

Python 3.12+, standard library only. Read-only; no network or host inspection.
Input: a nonempty JSON array of objects with method, http_status, content_type,
and body. body is parsed JSON, or null for a HEAD response without content.
Checks the problem+json policy and common internal diagnostic signatures in
title/detail. This is neither full schema validation nor a complete redaction check.
Output: JSON findings on stdout; input diagnostics on stderr, without values.
Exit: 0 pass, 1 findings, 2 usage, unsupported Python, or unreadable input.
"""

import argparse
import json
import re
import sys
from pathlib import Path


INTERNAL_DIAGNOSTIC = re.compile(
    r"Traceback \(most recent call last\)|\bSQLSTATE\b|duplicate key value violates|"
    r"syntax error at or near|\n\s+at \S+ \(|panicked at ", re.IGNORECASE
)


def unique_members(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("duplicate JSON member")
        result[key] = value
    return result


def reject_constant(_):
    raise ValueError("non-JSON numeric constant")


def check(cases, require_status=False):
    if not isinstance(cases, list) or not cases:
        raise ValueError("provide a nonempty JSON array of sanitized error examples")
    findings = []
    for index, case in enumerate(cases, 1):
        if not isinstance(case, dict) or set(case) != {
            "method", "http_status", "content_type", "body"
        }:
            raise ValueError("each example needs only method, http_status, content_type, and body")
        status = case["http_status"]
        if type(status) is not int or not 400 <= status <= 599:
            raise ValueError("http_status must be an integer error code from 400 through 599")
        method = case["method"]
        if not isinstance(method, str) or not method or not method.isascii() or not method.isalpha() or not method.isupper():
            raise ValueError("method must be an uppercase ASCII method name")
        media = case["content_type"]
        if media is not None and not isinstance(media, str):
            raise ValueError("content_type must be a string or null")

        def finding(rule, fix):
            findings.append({"case": index, "rule": rule, "fix": fix})

        body = case["body"]
        if method == "HEAD":
            if body is not None:
                finding("head-body", "Remove the HEAD response content; retain the error status.")
            continue
        if media is None or media.split(";", 1)[0].strip().lower() != "application/problem+json":
            finding("media-type", "Emit application/problem+json for this operation's problem response.")
        if not isinstance(body, dict):
            finding("problem-object", "Return a JSON object conforming to the operation's error schema.")
            continue
        if "status" in body:
            value = body["status"]
            if type(value) not in (int, float) or value != status:
                finding("status-mismatch", "Make the origin HTTP status and numeric problem status agree.")
        elif require_status:
            finding("missing-status", "Include status as required by this API's chosen error contract.")
        for member in ("type", "title", "detail", "instance"):
            if member in body and not isinstance(body[member], str):
                finding("member-type", "Serialize each standard problem text member as a string.")
                break
        if any(isinstance(body.get(member), str) and INTERNAL_DIAGNOSTIC.search(body[member])
               for member in ("title", "detail")):
            finding("internal-diagnostic", "Remove internal diagnostics from public problem text; retain only safe client guidance.")
    return {"checked": len(cases), "findings": findings}


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("examples", type=Path, help="sanitized JSON error examples; never raw credentials or personal data")
    parser.add_argument("--require-status", action="store_true", help="enforce an API policy requiring the optional problem status member")
    args = parser.parse_args()
    if sys.version_info < (3, 12):
        print("error: use Python 3.12 or later to run check-problem-responses.py", file=sys.stderr)
        return 2
    try:
        with args.examples.open(encoding="utf-8") as source:
            cases = json.load(source, object_pairs_hook=unique_members, parse_constant=reject_constant)
        report = check(cases, args.require_status)
    except (OSError, UnicodeError, ValueError, RecursionError):
        print("error: pass readable UTF-8 JSON with a nonempty error-example array; see --help for its fields", file=sys.stderr)
        return 2
    print(json.dumps(report, indent=2))
    return 1 if report["findings"] else 0


if __name__ == "__main__":
    sys.exit(main())
