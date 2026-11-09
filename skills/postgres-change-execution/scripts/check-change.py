#!/usr/bin/env python3
"""Compare a change plan with a fresh nonsecret observation and candidate bytes.

Python 3.12+ standard library. Read-only: never connects or executes SQL.
Usage: check-change.py PLAN.json OBSERVED.json CANDIDATE.sql
Output: JSON summary on stdout; value-free diagnostics on stderr.
Exit: 0 ready for native recheck, 1 rejected, 2 usage/unreadable input.
A pass supplies neither authorization nor protection against concurrent changes.
"""

import argparse
import hashlib
import json
import math
import re
import sys
from datetime import datetime, timezone
from pathlib import Path


def check(plan, observed, candidate):
    errors = []

    def require(condition, fix):
        if not condition:
            errors.append(fix)

    def digest(value):
        return isinstance(value, str) and re.fullmatch(r"[0-9a-f]{64}", value) is not None

    def text(value):
        return isinstance(value, str) and bool(value.strip())

    def same_json(left, right):
        try:
            return json.dumps(left, sort_keys=True, allow_nan=False) == json.dumps(right, sort_keys=True, allow_nan=False)
        except (TypeError, ValueError):
            return False

    if not isinstance(plan, dict) or not isinstance(observed, dict):
        return ["supply plan and observation JSON objects"]
    expected_target, actual_target = plan.get("target"), observed.get("target")
    require(isinstance(expected_target, dict)
            and set(expected_target) == {"deployment", "endpoint_id", "database", "server_identity", "principal"}
            and all(text(v) for v in expected_target.values())
            and expected_target == actual_target, "bind observation to the exact target and principal")
    actual_digest = hashlib.sha256(candidate).hexdigest()
    require(plan.get("candidate_sha256") == actual_digest == observed.get("candidate_sha256"),
            "rebuild and review the plan for these exact candidate bytes")
    try:
        when = datetime.fromisoformat(observed["observed_at"].replace("Z", "+00:00"))
        age = (datetime.now(timezone.utc) - when).total_seconds()
        max_age = plan["max_observation_age_seconds"]
        valid_age = (type(max_age) in (int, float) and math.isfinite(max_age)
                     and max_age > 0 and 0 <= age <= max_age)
    except (KeyError, TypeError, ValueError, AttributeError, OverflowError):
        valid_age = False
    require(valid_age, "collect a fresh timezone-aware observation inside the stated freshness budget")
    expected, actual = plan.get("preconditions"), observed.get("preconditions")
    require(isinstance(expected, dict) and bool(expected) and same_json(expected, actual),
            "recheck every named precondition; stale state requires a revised candidate")
    row_count, bound, expected_count = observed.get("row_count"), plan.get("max_rows"), plan.get("expected_rows")
    require(type(row_count) is int and type(bound) is int and type(expected_count) is int
            and 0 <= row_count == expected_count <= bound,
            "match the exact expected count within the approved maximum effect")
    key_digest = plan.get("selected_keys_sha256")
    require(digest(key_digest) and key_digest == observed.get("selected_keys_sha256"),
            "bind the selected key set and comparison values, not only a row count")
    for timeout in ("lock_timeout_ms", "statement_timeout_ms"):
        require(type(plan.get(timeout)) is int and plan[timeout] > 0, "set a positive " + timeout)
    require(text(plan.get("authority_ref")), "locate applicable authority for this target, candidate and effect")
    require(type(plan.get("destructive")) is bool, "classify whether this operation is destructive")
    if plan.get("destructive") is True:
        recovery = plan.get("recovery")
        require(isinstance(recovery, dict) and text(recovery.get("receipt_ref"))
                and recovery.get("target") == expected_target
                and recovery.get("usable") is True,
                "supply a verified usable recovery receipt bound to this target")
    effects = plan.get("effects")
    require(isinstance(effects, list) and bool(effects)
            and all(x in ("transactional", "nontransactional", "sequence", "trigger", "external") for x in effects),
            "inventory transactional, sequence, trigger and external effects")
    if isinstance(effects, list) and any(x != "transactional" for x in effects):
        rehearsal = plan.get("rehearsal")
        require(isinstance(rehearsal, dict) and rehearsal.get("disposable") is True
                and text(rehearsal.get("receipt_ref")),
                "rehearse nontransactional and indirect effects on an isolated disposable copy")
    require(text(plan.get("verification_ref")), "name independent post-change assertions")
    return errors


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("duplicate JSON member")
        result[key] = value
    return result


class Parser(argparse.ArgumentParser):
    def error(self, message):
        self.print_usage(sys.stderr)
        self.exit(2, "error: supply the documented local file arguments; see --help\n")


def main():
    parser = Parser(description=__doc__)
    parser.add_argument("plan", type=Path)
    parser.add_argument("observed", type=Path)
    parser.add_argument("candidate", type=Path)
    args = parser.parse_args()
    try:
        plan = json.loads(args.plan.read_text(encoding="utf-8"), object_pairs_hook=unique_object)
        observed = json.loads(args.observed.read_text(encoding="utf-8"), object_pairs_hook=unique_object)
        candidate = args.candidate.read_bytes()
    except (OSError, UnicodeError, ValueError):
        print("error: provide readable plan, observation and SQL files; contents withheld", file=sys.stderr)
        return 2
    errors = check(plan, observed, candidate)
    for error in errors:
        print("error: " + error, file=sys.stderr)
    print(json.dumps({"ok": not errors, "findings": len(errors),
                      "next": "native_recheck" if not errors else "stop"}))
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
