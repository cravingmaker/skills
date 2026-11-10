#!/usr/bin/env python3
"""Reject effects outside a narrowly defined identity-preserving refactor."""
import argparse
import hashlib
import json
from pathlib import Path
import sys


def identity(value):
    return isinstance(value, str) and bool(value) and not any(ord(c) < 32 for c in value)


def expectations(document):
    if not isinstance(document, dict) or set(document) - {"moved", "imported"}:
        raise ValueError("expect only moved and imported identities")
    moved, imported = document.get("moved", {}), document.get("imported", [])
    if not isinstance(moved, dict) or not isinstance(imported, list):
        raise ValueError("invalid expectation collections")
    if any(not identity(old) or not identity(new) or old == new for old, new in moved.items()):
        raise ValueError("invalid move identities")
    if any(not identity(item) for item in imported) or len(set(imported)) != len(imported) or len(set(moved.values())) != len(moved):
        raise ValueError("duplicate or invalid expected identities")
    return moved, set(imported)


def has_unknown(value):
    if isinstance(value, dict):
        return any(has_unknown(v) for v in value.values())
    if isinstance(value, list):
        return any(has_unknown(v) for v in value)
    if value is None or isinstance(value, bool):
        return value is True
    raise ValueError("invalid unknown mask")


def main():
    parser = argparse.ArgumentParser(description=(
        "Check local show-JSON for a pure refactor/import: managed no-op and data reads "
        "only. No cloud calls or writes. JSON on stdout; diagnostics on stderr. "
        "Exits: 0 narrow check passed, 1 findings, 2 invalid input. "
        "Does not verify remote IDs, backups or authorization."))
    parser.add_argument("plan_json", type=Path)
    parser.add_argument("--expect", type=Path,
                        help="JSON with exact moved {old: new} and imported [address] sets; identifiers stay private")
    args = parser.parse_args()
    try:
        expected_raw = args.expect.read_bytes() if args.expect else None
        expected = expectations(json.loads(expected_raw)) if expected_raw is not None else None
        raw = args.plan_json.read_bytes()
        plan = json.loads(raw)
        if not isinstance(plan, dict) or not isinstance(plan.get("format_version"), str) or not isinstance(plan.get("planned_values"), dict):
            raise ValueError("not plan JSON")
        if plan["format_version"].split(".")[0] != "1":
            raise ValueError("unsupported major format")
        findings, moved, imported = [], {}, set()
        changes = plan.get("resource_changes", [])
        if not isinstance(changes, list):
            raise ValueError("invalid resources")
        for index, row in enumerate(changes, 1):
            if not isinstance(row, dict) or not isinstance(row.get("change"), dict):
                raise ValueError("invalid resource change")
            change, mode = row["change"], row.get("mode")
            actions = change.get("actions")
            if not isinstance(actions, list) or not actions or not all(isinstance(a, str) for a in actions) or mode not in ("managed", "data"):
                raise ValueError("invalid actions or mode")
            allowed = actions == ["no-op"] or (mode == "data" and actions == ["read"])
            if not allowed:
                findings.append({"row": index, "code": "resource-effect-outside-pure-refactor"})
            if has_unknown(change.get("after_unknown")):
                findings.append({"row": index, "code": "unknown-resource-values"})
            if "previous_address" in row or change.get("importing"):
                if not identity(row.get("address")):
                    raise ValueError("missing operation address")
            if "previous_address" in row:
                previous, current = row["previous_address"], row["address"]
                if not identity(previous) or previous == current or previous in moved or current in moved.values():
                    raise ValueError("invalid or duplicate move")
                moved[previous] = current
            if change.get("importing"):
                if not isinstance(change["importing"], dict) or row["address"] in imported:
                    raise ValueError("invalid or duplicate import")
                imported.add(row["address"])
        if expected is not None:
            want_moved, want_imported = expected
            if moved != want_moved:
                findings.append({"code": "move-set-does-not-match-expectation"})
            if imported != want_imported:
                findings.append({"code": "import-set-does-not-match-expectation"})
        outputs = plan.get("output_changes", {})
        if not isinstance(outputs, dict):
            raise ValueError("invalid outputs")
        for change in outputs.values():
            if not isinstance(change, dict) or not isinstance(change.get("actions"), list):
                raise ValueError("invalid output change")
            if change["actions"] != ["no-op"] or has_unknown(change.get("after_unknown")):
                findings.append({"code": "output-effect-outside-pure-refactor"})
        if plan.get("resource_drift"):
            findings.append({"code": "drift-needs-separate-review"})
        if plan.get("complete") is False or plan.get("errored") is True or plan.get("deferred_changes"):
            findings.append({"code": "incomplete-or-errored-plan"})
        checks = plan.get("checks", [])
        if not isinstance(checks, list) or any(not isinstance(c, dict) for c in checks):
            raise ValueError("invalid checks")
        if any(c.get("status") != "pass" for c in checks):
            findings.append({"code": "nonpassing-plan-check"})
        result = {"json_sha256": hashlib.sha256(raw).hexdigest(),
                  "expectation_sha256": hashlib.sha256(expected_raw).hexdigest() if expected_raw is not None else None,
                  "moved": len(moved), "imported": len(imported), "findings": findings,
                  "scope": "pure-refactor static check; remote identity and recovery unverified"}
    except (OSError, ValueError, TypeError, RecursionError):
        print("error: cannot check refactor; supply readable native plan JSON in a supported schema (payload withheld)", file=sys.stderr)
        return 2
    print(json.dumps(result, sort_keys=True))
    return int(bool(findings))


if __name__ == "__main__":
    sys.exit(main())
