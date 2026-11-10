#!/usr/bin/env python3
"""Check an alert-linked runbook's structure and diagnostic branch graph offline.

Python 3.12+ stdlib. Usage: check-runbook.py RUNBOOK.json
Stdout: JSON counts and finding codes, never commands or source values.
Stderr: input/fix diagnostics. Exit: 0 structural pass, 1 findings, 2 bad input.
--help exits 0 without inspection or writes. No commands or network calls run.
Receipt paths are relative regular files inside the runbook's directory; their
digest, target, date and step coverage are checked, not their truth.
This is not rehearsal or authorization.
"""
import argparse
from datetime import date
import json
import hashlib
from pathlib import Path
import re
import sys
from urllib.parse import urlsplit

TERMINALS = {"recovered", "abort", "escalate"}
TOP = {"title", "alert", "runbook_url", "owner", "escalation", "target", "preconditions",
       "abort", "recovery", "last_rehearsed", "rehearsal_receipt", "steps"}
STEP = {"id", "kind", "command", "expected", "on_expected", "otherwise", "timeout_seconds", "authority"}


def unique(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError
        result[key] = value
    return result


def text(value):
    return (isinstance(value, str) and bool(value.strip()) and not re.search(r"<[^>\n]+>", value)
            and value.strip().lower() not in {"todo", "tbd", "pending", "not run", "unknown"})


def receipt(base, value):
    if not text(value):
        return False
    path = Path(value)
    candidate = base / path
    return (not path.is_absolute() and not candidate.is_symlink()
            and candidate.resolve().is_relative_to(base.resolve()) and candidate.is_file())


def check_receipt(base, value, content, ids):
    if not receipt(base, value["rehearsal_receipt"]):
        return ["missing_local_rehearsal_receipt"]
    try:
        record = json.loads((base / value["rehearsal_receipt"]).read_text(), object_pairs_hook=unique,
                            parse_constant=lambda _: (_ for _ in ()).throw(ValueError()))
    except (OSError, ValueError):
        return ["invalid_rehearsal_receipt"]
    if not isinstance(record, dict):
        return ["invalid_rehearsal_receipt"]
    findings = []
    if record.get("procedure_sha256") != hashlib.sha256(content.encode()).hexdigest():
        findings.append("receipt_stale")
    if record.get("rehearsed_on") != value["last_rehearsed"]:
        findings.append("receipt_date_mismatch")
    if record.get("target") != value["target"] or not text(record.get("operator")):
        findings.append("receipt_target_or_operator_missing")
    observed, omitted = record.get("steps"), record.get("not_rehearsed")
    if not isinstance(observed, list) or not isinstance(omitted, list):
        return findings + ["invalid_receipt_steps"]
    covered = []
    for row in observed:
        if not isinstance(row, dict) or not isinstance(row.get("id"), str):
            findings.append("invalid_receipt_steps")
            continue
        covered.append(row["id"])
        if not text(row.get("observed")) or row.get("matched") is not True:
            findings.append("rehearsal_mismatch")
    if omitted:
        findings.append("unrehearsed_steps")
    if set(covered) != set(ids) or len(covered) != len(set(covered)):
        findings.append("receipt_step_coverage")
    return findings


def evaluate(value, base, content):
    if not isinstance(value, dict) or set(value) != TOP or not isinstance(value["steps"], list):
        raise ValueError
    findings = []
    for field in ("title", "alert", "owner", "escalation", "target", "recovery"):
        if not text(value[field]):
            findings.append(f"missing_text:{field}")
    for field in ("preconditions", "abort"):
        if not isinstance(value[field], list) or not value[field] or not all(text(x) for x in value[field]):
            findings.append(f"missing_list:{field}")
    try:
        url = urlsplit(value["runbook_url"])
        if url.scheme != "https" or not url.hostname or url.username or url.password:
            findings.append("invalid_runbook_url")
    except (ValueError, TypeError, AttributeError):
        findings.append("invalid_runbook_url")
    try:
        if not isinstance(value["last_rehearsed"], str) or date.fromisoformat(value["last_rehearsed"]) > date.today():
            raise ValueError
    except ValueError:
        findings.append("missing_successful_rehearsal_date")
    steps, edges = value["steps"], {}
    if not steps:
        findings.append("no_steps")
    for index, step in enumerate(steps):
        if not isinstance(step, dict) or not STEP <= set(step) or set(step) - STEP - {"undo"}:
            raise ValueError
        ident = step["id"]
        if not isinstance(ident, str) or not ident.isidentifier() or ident in TERMINALS or ident in edges:
            raise ValueError
        edges[ident] = []
        for field in ("command", "expected", "authority"):
            if not text(step[field]):
                findings.append(f"incomplete_step:{index}:{field}")
        if step["kind"] not in {"diagnostic", "mitigation", "verification"}:
            findings.append(f"invalid_step_kind:{index}")
        if type(step["timeout_seconds"]) is not int or step["timeout_seconds"] <= 0:
            findings.append(f"unbounded_step:{index}")
        if step["kind"] == "mitigation" and step["authority"] in {"read-only", "none", "planning only"}:
            findings.append(f"missing_mitigation_authority:{index}")
        if step["kind"] == "mitigation" and not text(step.get("undo")):
            findings.append(f"missing_mitigation_undo:{index}")
        for field in ("on_expected", "otherwise"):
            target = step[field]
            if not isinstance(target, str):
                raise ValueError
            edges[ident].append(target)
            if target == "recovered" and step["kind"] != "verification":
                findings.append(f"recovery_without_verification:{index}")
    if steps and steps[0]["kind"] != "diagnostic":
        findings.append("entry_is_not_diagnostic")
    if any(target not in edges and target not in TERMINALS for targets in edges.values() for target in targets):
        findings.append("dangling_branch")
    seen, active = set(), set()

    def walk(node):
        if node in TERMINALS or node not in edges:
            return
        if node in active:
            if "cycle_without_bound" not in findings:
                findings.append("cycle_without_bound")
            return
        if node in seen:
            return
        active.add(node)
        for target in edges[node]:
            walk(target)
        active.remove(node)
        seen.add(node)

    if steps:
        walk(steps[0]["id"])
    if set(edges) - seen:
        findings.append("unreachable_step")
    if not any("recovered" in targets for targets in edges.values()):
        findings.append("missing_recovery_path")
    findings.extend(check_receipt(base, value, content, edges))
    return {"steps": len(steps), "findings": findings, "scope": "structure_only",
            "procedure_sha256": hashlib.sha256(content.encode()).hexdigest()}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("runbook", type=Path)
    args = parser.parse_args()
    if sys.version_info < (3, 12):
        print("error: use Python 3.12 or later", file=sys.stderr)
        return 2
    try:
        content = args.runbook.read_bytes().decode("utf-8")
        value = json.loads(content, object_pairs_hook=unique,
                           parse_constant=lambda _: (_ for _ in ()).throw(ValueError()))
        result = evaluate(value, args.runbook.resolve().parent, content)
    except (OSError, ValueError, TypeError, RecursionError):
        print("error: supply valid unique-key JSON matching the runbook asset, with finite values and unique step IDs", file=sys.stderr)
        return 2
    print(json.dumps(result, sort_keys=True))
    if result["findings"]:
        print("error: complete the named fields, repair branch targets and record an actual successful rehearsal", file=sys.stderr)
    return 1 if result["findings"] else 0


if __name__ == "__main__":
    sys.exit(main())
