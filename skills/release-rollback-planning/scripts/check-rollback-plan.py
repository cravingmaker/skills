#!/usr/bin/env python3
"""Check a rollback plan record before a deploy.

Python 3.12+ standard library. Read-only: never runs a rollback command or
contacts a registry, cluster or database.

Usage: check-rollback-plan.py [--allow-unrehearsed] [--max-drill-age-days N]
                              [--today YYYY-MM-DD] PLAN.json

Checks: candidate and previous artifacts named by digest (repo@sha256:...),
not tag; a different artifact/config recovery state; configs named by commit SHA or digest; previous
artifact retained; GitOps plans say how auto-sync is handled; rollback
commands and a time budget; schema phase and whether the previous code runs
on it (incompatible schema requires strategy roll-forward); a non-empty list
of effects rollback cannot undo, each with its handling; rollback triggers
with signal and threshold, a decider and a decision deadline; a drill outside
production on these exact artifacts, with measured duration within budget
and a passing user-path check. Source/target/authority, abort/recovery, exact config,
plan-digest and local receipt binding are also required. A roll-forward drill
exercises the compatible candidate repair, not an incompatible old artifact.
A pass means the record is complete and self-consistent. It does not prove
the commands work on the real target or that the listed effects are all of
them.

Output: allowlisted JSON counts/enums and plan SHA-256 on stdout, diagnostics on stderr.
Never prints or executes commands, source values or effective configuration.
Local receipt existence and declarations do not prove rehearsal or authority.
Exit: 0 no findings, 1 findings, 2 usage or unreadable input.
"""

import argparse
import json
import hashlib
import math
from pathlib import Path
import re
import sys
from datetime import date, datetime, timezone

ARTIFACT = re.compile(r"^\S+@sha256:[0-9a-f]{64}$|^sha256:[0-9a-f]{64}$")
CONFIG = re.compile(r"^git:(?:[0-9a-f]{40}|[0-9a-f]{64})$|^sha256:[0-9a-f]{64}$")
PHASES = {"none", "expand", "migrate", "contract"}
PRODUCTION = {"production", "prod", "live"}


def text(value):
    return isinstance(value, str) and bool(value.strip()) and not re.search(r"<[^>\n]+>", value) and value.strip().lower() not in {"todo", "tbd", "unknown", "pending"}


def number(value):
    return type(value) in (int, float) and value > 0 and math.isfinite(value)


def unique(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError
        result[key] = value
    return result


def plan_digest(plan):
    return hashlib.sha256(json.dumps({k: v for k, v in plan.items() if k != "drill"},
                                    sort_keys=True, separators=(",", ":"), allow_nan=False).encode()).hexdigest()


def local_receipt(base, value):
    if not text(value):
        return False
    path = Path(value)
    candidate = base / path
    return not path.is_absolute() and not candidate.is_symlink() and candidate.resolve().is_relative_to(base.resolve()) and candidate.is_file()


def check(plan, args):
    findings = []

    def find(rule, detail):
        findings.append({"rule": rule, "detail": detail})

    def section(name):
        value = plan.get(name)
        if not isinstance(value, dict):
            find("missing", f"add the `{name}` object")
            return {}
        return value

    for field in ("service", "environment", "target", "owner", "authority"):
        if not text(plan.get(field)):
            find("missing", f"name the `{field}`")
    if not isinstance(plan.get("source_revision"), str) or not re.fullmatch(r"[0-9a-f]{40}|[0-9a-f]{64}", plan["source_revision"]):
        find("source_revision", "bind the source revision to a full commit resolved live")
    strategy = plan.get("strategy")
    if strategy not in ("rollback", "roll-forward"):
        find("missing", "set `strategy` to rollback or roll-forward")

    candidate, previous = section("candidate"), section("previous")
    for label, item in (("candidate", candidate), ("previous", previous)):
        if not (text(item.get("artifact")) and ARTIFACT.match(item["artifact"])):
            find("artifact_not_digest", f"name the {label} artifact by digest (repo@sha256:<64 hex>), resolved live; a tag can move")
        if not (text(item.get("config")) and CONFIG.match(item["config"])):
            find("config_not_pinned", f"name the {label} config by commit (git:<40 hex>) or digest, not a branch")
    if candidate.get("artifact") and candidate.get("artifact") == previous.get("artifact") and candidate.get("config") == previous.get("config"):
        find("same_state", "candidate and previous artifact/config are identical; identify the retained recovery state")
    if not text(previous.get("retained_until")):
        find("retention", "state until when the previous artifact and config are retained (registry and Git)")

    delivery = section("delivery")
    mechanism = delivery.get("mechanism")
    if mechanism not in ("push", "gitops"):
        find("missing", "set `delivery.mechanism` to push or gitops")
    elif mechanism == "gitops" and not (text(delivery.get("controller")) and text(delivery.get("auto_sync"))):
        find("gitops_auto_sync", "name the controller and how auto-sync is handled; a syncing controller reverts a manual rollback")

    rollback = section("rollback")
    commands = rollback.get("commands")
    if not (isinstance(commands, list) and commands and all(text(c) for c in commands)):
        find("rollback_commands", "list the exact rollback commands")
    elif any(re.search(r"<[A-Za-z][\w .-]*>", c) for c in commands):
        find("rollback_commands", "replace <placeholders> in rollback commands with real values or named $VARIABLES")
    for field in ("abort", "recovery"):
        if not text(rollback.get(field)):
            find("recovery_boundary", "name abort/escalation and independent user-path recovery criteria")
    if not number(rollback.get("max_seconds")):
        find("rollback_budget", "set `rollback.max_seconds`, the longest acceptable rollback")

    schema = section("schema")
    if schema.get("phase") not in PHASES:
        find("schema_state", "set `schema.phase` to none, expand, migrate or contract")
    compatible = schema.get("previous_code_compatible")
    if not isinstance(compatible, bool):
        find("schema_state", "state whether the previous code runs on the schema after this deploy (true/false)")
    elif compatible is False and strategy != "roll-forward":
        find("rollback_blocked_by_schema", "the previous code cannot run on the new schema; set strategy roll-forward and plan the fix path, or keep the schema compatible")

    effects = plan.get("irreversible_effects")
    if not (isinstance(effects, list) and effects):
        find("irreversible_effects", "list what rollback cannot undo (contracted schema, deleted or rewritten data, sent messages, external calls); never leave it empty")
    else:
        for index, effect in enumerate(effects):
            if not (isinstance(effect, dict) and text(effect.get("effect")) and text(effect.get("handling"))):
                find("irreversible_effects", f"effect {index + 1}: give `effect` and `handling`")

    decision = section("decision")
    triggers = decision.get("rollback_when")
    if not (isinstance(triggers, list) and triggers
            and all(isinstance(t, dict) and text(t.get("signal")) and text(t.get("threshold")) and text(t.get("source")) for t in triggers)):
        find("decision", "list rollback triggers, each with `signal` and `threshold`")
    if not text(decision.get("decider")):
        find("decision", "name who decides rollback versus roll-forward")
    if not number(decision.get("decide_within_minutes")):
        find("decision", "set `decide_within_minutes`")
    if strategy == "roll-forward" and not (isinstance(decision.get("roll_forward_when"), list) and decision["roll_forward_when"]):
        find("decision", "a roll-forward plan lists `roll_forward_when` conditions")

    if strategy == "roll-forward":
        commands = decision.get("roll_forward_commands")
        if not (isinstance(commands, list) and commands and all(text(x) for x in commands)):
            find("decision", "a roll-forward plan names the exact compatible repair commands and candidate artifact")
    drill = plan.get("drill")
    if drill is None:
        if not args.allow_unrehearsed:
            find("unrehearsed", "run a rollback drill outside production on these artifacts and record it; --allow-unrehearsed is for drafts")
    elif not isinstance(drill, dict):
        find("drill", "`drill` must be an object")
    else:
        if drill.get("target_kind") != "disposable" or not text(drill.get("target")) or drill.get("target") == plan.get("target"):
            find("drill_target", "name an explicitly disposable target distinct from the deployment target")
        if drill.get("plan_sha256") != plan_digest(plan):
            find("drill_stale", "the source, target, commands, config or decision changed; rehearse the current plan")
        if drill.get("action") != strategy:
            find("drill_action", "record which selected recovery strategy the drill exercised")
        expected = previous.get("artifact") if strategy == "rollback" else candidate.get("artifact")
        if drill.get("recovered_artifact") != expected:
            find("drill_recovery_artifact", "record the recovered artifact for the selected strategy")
        if not local_receipt(args.base, drill.get("receipt")):
            find("drill_receipt", "keep a relative regular local rehearsal receipt inside the plan directory")
        for field in ("candidate_config", "previous_config"):
            expected_config = candidate.get("config") if field == "candidate_config" else previous.get("config")
            if drill.get(field) != expected_config:
                find("drill_config", "rehearse with the exact retained candidate and previous configs")
        env = str(drill.get("environment", "")).strip().lower()
        if not env or env in PRODUCTION or env == str(plan.get("environment", "")).strip().lower():
            find("drill_environment", "drill in a non-production environment and name it")
        if drill.get("candidate_artifact") != candidate.get("artifact") or drill.get("previous_artifact") != previous.get("artifact"):
            find("drill_artifacts", "the drill must roll back from this candidate to this previous digest; drill again")
        seconds = drill.get("measured_seconds")
        if not number(seconds):
            find("drill_duration", "record the measured rollback duration in seconds")
        elif number(rollback.get("max_seconds")) and seconds > rollback["max_seconds"]:
            find("drill_too_slow", f"the drill took {seconds} s, over the {rollback['max_seconds']} s budget")
        probe = drill.get("user_path_check")
        if not (isinstance(probe, dict) and text(probe.get("command")) and probe.get("passed") is True):
            find("drill_user_path", "after the drill, a user-path check (a real request through the service) must pass")
        try:
            when = date.fromisoformat(str(drill.get("date")))
        except ValueError:
            find("drill_date", "record the drill date as YYYY-MM-DD")
        else:
            age = (args.today - when).days
            if age < 0:
                find("drill_date", "the drill date is in the future")
            elif args.max_drill_age_days is not None and age > args.max_drill_age_days:
                find("drill_stale", f"the drill is {age} days old; the limit is {args.max_drill_age_days}")
    summary = {"strategy": strategy if strategy in ("rollback", "roll-forward") else None,
               "schema_phase": schema.get("phase") if schema.get("phase") in PHASES else None,
               "irreversible_effects": len(effects) if isinstance(effects, list) else 0,
               "scope": "structure_only", "plan_sha256": plan_digest(plan)}
    return findings, summary


def main(argv):
    if "--help" in argv or "-h" in argv:
        print(__doc__.strip())
        return 0
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("--allow-unrehearsed", action="store_true")
    parser.add_argument("--max-drill-age-days", type=int)
    parser.add_argument("--today")
    parser.add_argument("plan")
    try:
        args = parser.parse_args(argv)
        args.today = date.fromisoformat(args.today) if args.today else datetime.now(timezone.utc).date()
    except (SystemExit, ValueError):
        print("usage: check-rollback-plan.py [--allow-unrehearsed] [--max-drill-age-days N] [--today YYYY-MM-DD] PLAN.json", file=sys.stderr)
        return 2
    if sys.version_info < (3, 12):
        print("error: use Python 3.12 or later", file=sys.stderr)
        return 2
    try:
        args.base = Path(args.plan).resolve().parent
        with open(args.plan, encoding="utf-8") as handle:
            plan = json.load(handle, object_pairs_hook=unique,
                             parse_constant=lambda _: (_ for _ in ()).throw(ValueError()))
    except (OSError, ValueError):
        print("error: pass readable unique-key UTF-8 JSON with finite values", file=sys.stderr)
        return 2
    if not isinstance(plan, dict):
        print("the plan must be a JSON object", file=sys.stderr)
        return 2
    try:
        findings, summary = check(plan, args)
    except (ValueError, TypeError, OverflowError, RecursionError, OSError):
        print("error: use the supplied plan schema with valid finite types and confined receipts", file=sys.stderr)
        return 2
    print(json.dumps({"findings": findings, "summary": summary}, indent=2))
    return 1 if findings else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
