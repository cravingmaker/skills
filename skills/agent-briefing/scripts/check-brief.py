#!/usr/bin/env python3
"""Check required Markdown brief fields, not their truth or adequacy.

Requires Python 3.12 or later, standard library only. No writes or network.
Exit: 0 pass, 1 findings, 2 usage or unreadable input.
"""

import argparse
import re
import sys
from pathlib import Path, PurePosixPath

FIELDS = (
    "Task identity", "Goal", "Context", "Workspace", "Scope", "Constraints",
    "Permissions", "Write boundary", "Role skill", "Capability skills",
    "Communication", "Terminology", "Open decisions", "Dependencies",
    "Acceptance", "Evidence standard", "Return contract", "Raw report path",
    "Budget", "Stop conditions",
)
RETURN_FIELDS = (
    "Result first", "Evidence", "Artifacts and revisions", "Commands and results",
    "Unresolved claims", "Decisions needed", "Assumptions and surprises", "Usage",
)


def sections(text):
    result = {}
    duplicates = []
    current = None
    fence = None
    for line in text.splitlines():
        marker = re.match(r"^\s*(`{3,}|~{3,})", line)
        if marker:
            token = marker.group(1)
            if fence is None:
                fence = token
            elif token[0] == fence[0] and len(token) >= len(fence):
                fence = None
            continue
        heading = re.match(r"^## ([^#].*?)\s*#*\s*$", line) if fence is None else None
        if heading:
            current = heading.group(1).strip().casefold()
            if current in result:
                duplicates.append(current)
            else:
                result[current] = []
        elif current is not None:
            result[current].append(line)
    return {key: "\n".join(value).strip() for key, value in result.items()}, duplicates


def content(value):
    value = re.sub(r"<!--.*?-->", "", value, flags=re.S)
    return bool(re.sub(r"[\s\-:*`#]", "", value))


def labels(body):
    found = {}
    for line in body.splitlines():
        match = re.match(r"^\s*(?:- )?([^:\n]+):\s*(.*?)\s*$", line)
        if match:
            key, value = match.groups()
            found.setdefault(key.strip().casefold(), []).append(value)
    return found


def check_brief(text):
    body, duplicates = sections(text)
    errors = [f"{name}: duplicate heading; keep one authoritative section" for name in duplicates]
    for name in FIELDS:
        value = body.get(name.casefold(), "")
        if not content(value):
            errors.append(f"{name}: missing field; add a populated '## {name}' section")
        elif re.search(r"\{\{.*?\}\}|\b(?:TODO|TBD)\b", value, re.I | re.S):
            errors.append(f"{name}: replace template placeholders with task facts or an explicit none")
    returned = labels(body.get("return contract", ""))
    for name in RETURN_FIELDS:
        values = returned.get(name.casefold(), [])
        if len(values) != 1 or not content(values[0]):
            errors.append(f"Return contract / {name}: add one populated '{name}:' line")
    permissions = labels(body.get("permissions", ""))
    for name in ("Read", "Write", "External actions"):
        values = permissions.get(name.casefold(), [])
        if len(values) != 1 or not content(values[0]):
            errors.append(f"Permissions / {name}: add one explicit '{name}:' line")
    report = body.get("raw report path", "").strip().strip("`")
    if report and ("\n" in report or not PurePosixPath(report).is_absolute() or report.endswith("/") or ".." in PurePosixPath(report).parts):
        errors.append("Raw report path: give one absolute POSIX file path, without '..'")
    budget = labels(body.get("budget", ""))
    allowed = budget.get("delegation", [])
    if len(allowed) != 1 or allowed[0] not in ("yes", "no"):
        errors.append("Budget / Delegation: state exactly 'Delegation: yes' or 'Delegation: no'")
    elif allowed == ["yes"]:
        for name in ("Worker starts", "Retries", "Review rounds", "Concurrency ceiling"):
            values = budget.get(name.casefold(), [])
            if len(values) != 1 or not re.fullmatch(r"[0-9]+", values[0]):
                errors.append(f"Budget / {name}: allocate a finite integer from the coordinator's ledger")
            elif name in ("Worker starts", "Concurrency ceiling") and int(values[0]) < 1:
                errors.append(f"Budget / {name}: allocate at least one or set Delegation: no")
            elif name == "Concurrency ceiling" and int(values[0]) > 8:
                errors.append("Budget / Concurrency ceiling: use at most 8 and respect lower shared limits")
        ledger = budget.get("ledger", [])
        if len(ledger) != 1 or not ledger[0].startswith("/"):
            errors.append("Budget / Ledger: name the absolute path to the shared run ledger")
    stop = budget.get("stop after", [])
    if len(stop) != 1 or not content(stop[0]):
        errors.append("Budget / Stop after: state this worker's bounded stopping condition")
    return errors


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("brief", type=Path)
    args = parser.parse_args()
    if sys.version_info < (3, 12):
        print("error: check-brief.py needs Python 3.12 or later; use python3.12 or a newer versioned interpreter on PATH, or uv run --python 3.12 check-brief.py", file=sys.stderr)
        return 2
    try:
        source = args.brief.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as error:
        print(f"error: read an existing UTF-8 brief file: {error}", file=sys.stderr)
        return 2
    errors = check_brief(source)
    if errors:
        for error in errors:
            print(f"FAIL: {error}")
        return 1
    print("PASS: required brief fields; inspect authority, evidence, and usable paths before dispatch")
    return 0


if __name__ == "__main__":
    sys.exit(main())
