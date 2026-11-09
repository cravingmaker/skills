#!/usr/bin/env python3
"""Compare complete actual-client access evidence with an independent policy.

Python 3.12+ standard library. No SQL execution, network access or writes.
Usage: check-privileges.py POLICY.json RESULTS.json
Output: JSON summary on stdout; field-path diagnostics on stderr.
Exit: 0 complete matching evidence, 1 findings, 2 usage/unreadable input.
The native adapter proves memberships and operations; this checks receipt closure.
"""

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path


def check(policy, results, policy_digest):
    errors = []

    def require(condition, fix):
        if not condition:
            errors.append(fix)

    def text(value):
        return isinstance(value, str) and bool(value.strip())

    def index(value, label):
        if not isinstance(value, list) or not value or any(not isinstance(x, dict) for x in value):
            errors.append(label + ": supply a nonempty array of checks")
            return {}
        indexed = {}
        for i, row in enumerate(value):
            ident = row.get("id")
            if not text(ident) or ident in indexed:
                errors.append(f"{label}[{i}]: supply distinct nonempty check ids")
            else:
                indexed[ident] = row
        return indexed

    if not isinstance(policy, dict) or not isinstance(results, dict):
        return ["supply policy and results JSON objects"]
    require(text(policy.get("target_id")) and policy.get("target_id") == results.get("target_id"),
            "bind results to the intended target")
    require(results.get("policy_sha256") == policy_digest, "rerun probes against these exact policy bytes")
    expected, actual = index(policy.get("checks"), "policy.checks"), index(results.get("checks"), "results.checks")
    require(set(expected) == set(actual), "supply every expected check exactly once, with no extra checks")
    for i, (ident, row) in enumerate(expected.items()):
        path = f"checks[{i}]"
        require(row.get("expected") in ("allow", "deny"), path + ": use allow or deny")
        require(row.get("kind") in ("sql", "connection"), path + ": use sql or connection")
        require(text(row.get("login")) and text(row.get("phase")), path + ": name login and lifecycle phase")
        probe_digest = row.get("probe_sha256")
        require(isinstance(probe_digest, str) and re.fullmatch(r"[0-9a-f]{64}", probe_digest) is not None,
                path + ": bind the exact native probe bytes")
        codes = row.get("codes")
        require(isinstance(codes, list) and bool(codes) and all(text(x) for x in codes),
                path + ": name the expected SQLSTATE or adapter failure codes")
        result = actual.get(ident, {})
        require(result.get("result") == row.get("expected") and isinstance(codes, list) and result.get("code") in codes,
                path + ": match the expected outcome and its cause; an arbitrary error is not a denial")
        for field in ("login", "probe_sha256", "phase", "kind"):
            require(text(row.get(field)) and row.get(field) == result.get(field), path + ": bind " + field)
        require(result.get("fresh_attempt") is True and result.get("adapter") == "actual-client",
                path + ": use a fresh actual-client attempt rather than an administrator's SET ROLE")
        if row.get("kind") == "sql":
            require(text(row.get("session_role")) and result.get("session_role") == row.get("session_role")
                    and result.get("authenticated_login") == row.get("login"), path + ": verify login and current role")
            forbidden = row.get("forbidden_roles")
            reachable = result.get("reachable_roles")
            require(isinstance(forbidden, list) and all(text(x) for x in forbidden)
                    and isinstance(reachable, list) and all(text(x) for x in reachable)
                    and not set(forbidden).intersection(reachable), path + ": remove forbidden inherited or SET ROLE paths")
            flags = result.get("role_flags")
            require(isinstance(flags, dict)
                    and set(flags) == {"superuser", "bypassrls", "createrole", "createdb"}
                    and all(v is False for v in flags.values()),
                    path + ": use a restricted identity without administrative or RLS-bypass attributes")
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
    parser.add_argument("policy", type=Path)
    parser.add_argument("results", type=Path)
    args = parser.parse_args()
    try:
        policy_bytes = args.policy.read_bytes()
        policy = json.loads(policy_bytes.decode("utf-8"), object_pairs_hook=unique_object)
        results = json.loads(args.results.read_text(encoding="utf-8"), object_pairs_hook=unique_object)
    except (OSError, UnicodeError, ValueError):
        print("error: supply readable UTF-8 policy and result JSON; contents withheld", file=sys.stderr)
        return 2
    errors = check(policy, results, hashlib.sha256(policy_bytes).hexdigest())
    for error in errors:
        print("error: " + error, file=sys.stderr)
    print(json.dumps({"ok": not errors, "findings": len(errors)}))
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
