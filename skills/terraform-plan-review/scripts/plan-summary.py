#!/usr/bin/env python3
"""Read a local plan export; emit metadata, never before/after values."""
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import re
import sys

KNOWN = {("no-op",), ("read",), ("create",), ("update",), ("delete",),
         ("delete", "create"), ("create", "delete"), ("forget",)}
STATEFUL = re.compile(r"database|db_instance|db_cluster|sql_instance|postgres|mysql|disk|volume|bucket|storage_account|kms|key_vault|managed_hsm|redis|elasticache", re.I)
AUTHORITY = re.compile(r"iam|policy|role|security_group|firewall|network|acl|bucket|storage|public|route|gateway", re.I)
IDENTIFIER = re.compile(r"[A-Za-z_][A-Za-z_0-9]*\Z")


def unknown(value):
    if isinstance(value, dict):
        return any(unknown(v) for v in value.values())
    if isinstance(value, list):
        return any(unknown(v) for v in value)
    if value is None or isinstance(value, bool):
        return value is True
    raise ValueError("invalid unknown-value mask")


def address(value):
    if not isinstance(value, str) or not value or any(ord(c) < 32 for c in value):
        raise ValueError("invalid resource address")
    # for_each keys can be user data. Keep structure without revealing string keys.
    return re.sub(r'\["(?:[^"\\]|\\.)*"\]', '["<redacted>"]', value)


def main():
    parser = argparse.ArgumentParser(description=(
        "Read local Terraform/OpenTofu show-JSON; JSON metadata on stdout, diagnostics "
        "on stderr. No cloud calls or writes. Exits: 0 no helper findings, 1 findings "
        "or engine error, 2 invalid input. Does not approve a plan or prove export binding."))
    parser.add_argument("plan_json", type=Path)
    parser.add_argument("--saved-plan", type=Path, help="hash this local binary artifact too")
    parser.add_argument("--detailed-exit-code", type=int, choices=(0, 1, 2),
                        help="captured engine plan -detailed-exitcode result; 2 means changes")
    parser.add_argument("--stateful-type", action="append", default=[],
                        help="also flag deletion/replacement of this exact provider resource type; repeatable")
    args = parser.parse_args()
    if args.detailed_exit_code == 1:
        print("error: engine planning failed; inspect its protected diagnostics and regenerate the plan", file=sys.stderr)
        return 1
    try:
        if any(not IDENTIFIER.fullmatch(kind) for kind in args.stateful_type):
            raise ValueError("stateful types must be provider identifiers")
        raw = args.plan_json.read_bytes()
        plan = json.loads(raw)
        if not isinstance(plan, dict) or not isinstance(plan.get("format_version"), str):
            raise ValueError("expected a native plan JSON object with format_version")
        if plan["format_version"].split(".")[0] != "1":
            raise ValueError("unsupported plan JSON major version; check the engine's current schema")
        if not isinstance(plan.get("planned_values"), dict):
            raise ValueError("expected planned_values; supply show-JSON for a plan, not state")
        resources, findings, counts = [], [], Counter()
        changes_present = False
        for field in ("resource_changes", "resource_drift"):
            rows = plan.get(field, [])
            if not isinstance(rows, list):
                raise ValueError("resource change collections must be lists")
            for position, row in enumerate(rows, 1):
                if not isinstance(row, dict) or not isinstance(row.get("change"), dict):
                    raise ValueError("resource entries need a change object")
                change = row["change"]
                actions = change.get("actions")
                if not isinstance(actions, list) or not actions or not all(isinstance(a, str) for a in actions):
                    raise ValueError("resource actions must be a nonempty string list")
                kind = row.get("type")
                if not isinstance(kind, str) or not IDENTIFIER.fullmatch(kind):
                    raise ValueError("resource type must be an identifier")
                mode = row.get("mode")
                if mode not in ("managed", "data"):
                    raise ValueError("unsupported resource mode; review with the current engine schema")
                flags = []
                if tuple(actions) not in KNOWN:
                    flags.append("unsupported-actions")
                    findings.append("unsupported-actions")
                reported_actions = actions if tuple(actions) in KNOWN else ["<unsupported>"]
                if field == "resource_changes":
                    counts["/".join(reported_actions)] += 1
                    changes_present |= actions != ["no-op"] or bool(change.get("importing")) or "previous_address" in row
                replacement = "create" in actions and "delete" in actions
                if mode == "managed" and "delete" in actions and (STATEFUL.search(kind) or kind in args.stateful_type):
                    flags.append("stateful-replacement" if replacement else "stateful-delete")
                    findings.append("stateful-destruction")
                if mode == "managed" and AUTHORITY.search(kind) and actions != ["no-op"]:
                    flags.append("authority-or-exposure-review")
                if unknown(change.get("after_unknown")):
                    flags.append("unknown-values-review")
                roots = set()
                paths = change.get("replace_paths", [])
                if not isinstance(paths, list):
                    raise ValueError("replace_paths must be a list")
                for path in paths:
                    if not isinstance(path, list) or not path:
                        raise ValueError("replacement paths must be nonempty lists")
                    root = path[0]
                    roots.add(root if isinstance(root, str) and IDENTIFIER.fullmatch(root) else "<redacted>")
                resources.append({"collection": field, "row": position,
                                  "address": address(row.get("address")), "type": kind,
                                  "actions": reported_actions, "replacement": replacement,
                                  "forcing_root_attributes": sorted(roots),
                                  "action_reason_present": bool(row.get("action_reason")),
                                  "flags": flags})
        outputs = plan.get("output_changes", {})
        if not isinstance(outputs, dict):
            raise ValueError("output_changes must be an object")
        output_count, output_unknown = 0, False
        for change in outputs.values():
            if not isinstance(change, dict) or not isinstance(change.get("actions"), list):
                raise ValueError("output changes need actions")
            output_count += change["actions"] != ["no-op"]
            output_unknown |= unknown(change.get("after_unknown"))
        changes_present |= bool(output_count)
        if args.detailed_exit_code == 0 and changes_present:
            findings.append("exit-zero-with-changes-check-artifact-binding")
        if args.detailed_exit_code == 2 and not changes_present:
            findings.append("exit-two-without-visible-changes-review-schema-and-binding")
        if plan.get("errored") is True or plan.get("complete") is False or plan.get("deferred_changes"):
            findings.append("incomplete-or-errored-plan")
        checks = plan.get("checks", [])
        if not isinstance(checks, list) or any(not isinstance(c, dict) for c in checks):
            raise ValueError("checks must be a list of objects")
        if any(check.get("status") != "pass" for check in checks):
            findings.append("nonpassing-plan-check")
        result = {"json_sha256": hashlib.sha256(raw).hexdigest(),
                  "saved_plan_sha256": hashlib.sha256(args.saved_plan.read_bytes()).hexdigest() if args.saved_plan else None,
                  "engine_exit_code": args.detailed_exit_code,
                  "action_counts": dict(sorted(counts.items())), "resources": resources,
                  "changed_outputs": output_count, "unknown_outputs": output_unknown,
                  "findings": sorted(set(findings)), "scope": "metadata-only; manual review required"}
    except (OSError, ValueError, TypeError, RecursionError):
        print("error: cannot summarize this plan; check local file access, JSON structure and supported engine schema (payload withheld)", file=sys.stderr)
        return 2
    print(json.dumps(result, sort_keys=True))
    return int(bool(findings))


if __name__ == "__main__":
    sys.exit(main())
