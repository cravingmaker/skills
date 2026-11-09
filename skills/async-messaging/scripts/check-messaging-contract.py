#!/usr/bin/env python3
"""Check a messaging contract (JSON) for the delivery mistakes that lose or repeat work.

Usage: check-messaging-contract.py CONTRACT.json

Requires Python 3.12 or later, standard library only. Reads one file; no writes or network.
Output: one "FAIL consumers[index]: <problem>" line per finding on stdout, or "OK <n> consumers".
Exit: 0 pass, 1 findings, 2 usage or unreadable input.
"""

import json
import math
import sys

REQUIRED_TEXT = (
    "name", "effect", "source", "delivery", "ordering", "dead_letter",
    "dead_letter_owner", "replay_authorized_by", "external_effects",
)
DELIVERY = {"at-least-once"}
JITTER = {"full"}


def text(value):
    return isinstance(value, str) and value.strip() != ""


def number(value):
    try:
        return type(value) in (int, float) and math.isfinite(value) and value > 0
    except OverflowError:
        return False


def unique(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("duplicate JSON key")
        result[key] = value
    return result


def reject_constant(_):
    raise ValueError("nonfinite JSON number")


def retry_window(entry):
    """Retry envelope plus a declared total queue/recovery-delay bound, in seconds."""
    attempts, lease = entry["max_attempts"], entry["lease_seconds"]
    base, cap = entry["backoff"]["base_seconds"], entry["backoff"]["cap_seconds"]
    # First retry has cap base. Double only until cap, then sum the plateau.
    count, delay, delays = 0, base, 0
    while count < attempts - 1 and delay < cap:
        delays += delay
        delay = min(cap, delay * 2)
        count += 1
    try:
        return attempts * lease + delays + (attempts - 1 - count) * cap + entry["queue_delay_bound_seconds"]
    except OverflowError:
        return math.inf


def check(entry):
    problems = []
    for key in REQUIRED_TEXT:
        if not text(entry.get(key)):
            problems.append(f"{key} is missing or empty; state it explicitly")
    delivery = entry.get("delivery")
    if text(delivery) and delivery not in DELIVERY:
        problems.append(
            "delivery is outside this contract; use at-least-once plus dedupe_key"
        )
    if not text(entry.get("dedupe_key")):
        problems.append("dedupe_key is missing; at-least-once delivery repeats messages")
    ordering = entry.get("ordering")
    if text(ordering) and ordering != "none":
        if ordering != "global" and not ordering.startswith("per-key:"):
            problems.append("ordering must be none, per-key:<key>, or global")
        elif ordering == "per-key:":
            problems.append("ordering per-key needs the key name after 'per-key:'")
        if not text(entry.get("ordering_reason")):
            problems.append("ordering_reason is missing; name the invariant that needs ordering")

    numeric_ok = True
    for key in ("lease_seconds", "handler_timeout_seconds", "retention_seconds"):
        if not number(entry.get(key)):
            problems.append(f"{key} must be a positive number of seconds")
            numeric_ok = False
    for key in ("cancellation_margin_seconds", "queue_delay_bound_seconds"):
        value = entry.get(key)
        if not number(value) and not (type(value) in (int, float) and value == 0):
            problems.append(f"{key} must be a finite nonnegative number of seconds")
            numeric_ok = False
    attempts = entry.get("max_attempts")
    if not isinstance(attempts, int) or isinstance(attempts, bool) or attempts < 1:
        problems.append("max_attempts must be a finite integer of at least 1; unbounded retries hide poison messages")
        numeric_ok = False
    backoff = entry.get("backoff")
    if not isinstance(backoff, dict):
        problems.append("backoff is missing; give base_seconds, cap_seconds, and jitter")
        numeric_ok = False
    else:
        if not number(backoff.get("base_seconds")) or not number(backoff.get("cap_seconds")):
            problems.append("backoff base_seconds and cap_seconds must be positive numbers")
            numeric_ok = False
        elif backoff["cap_seconds"] < backoff["base_seconds"]:
            problems.append("backoff cap_seconds is below base_seconds")
        if backoff.get("jitter") not in JITTER:
            problems.append("backoff jitter must be full; unjittered retries arrive together")

    if numeric_ok:
        if entry["handler_timeout_seconds"] >= entry["lease_seconds"]:
            problems.append(
                f"handler_timeout_seconds {entry['handler_timeout_seconds']} is not below "
                f"lease_seconds {entry['lease_seconds']}; a second worker can claim a job still running"
            )
        elif entry["handler_timeout_seconds"] + entry["cancellation_margin_seconds"] >= entry["lease_seconds"]:
            problems.append("handler timeout plus cancellation margin must stay below lease_seconds")
        window = retry_window(entry)
        if window >= entry["retention_seconds"]:
            problems.append(
                "worst-case retry window reaches retention_seconds; messages can expire before they dead-letter"
            )

    schema = entry.get("schema")
    if not isinstance(schema, dict) or not text(schema.get("type")):
        problems.append("schema.type is missing; every event names its type")
    elif not isinstance(schema.get("version"), int) or isinstance(schema.get("version"), bool) or schema["version"] < 1:
        problems.append("schema.version must be a positive integer")
    return problems


def main(argv):
    if len(argv) == 2 and argv[1] in ("-h", "--help"):
        print(__doc__.strip())
        return 0
    if len(argv) != 2:
        print("usage: check-messaging-contract.py CONTRACT.json", file=sys.stderr)
        return 2
    try:
        with open(argv[1], encoding="utf-8") as handle:
            data = json.load(handle, object_pairs_hook=unique, parse_constant=reject_constant)
    except (OSError, UnicodeError, ValueError, RecursionError):
        print("cannot read contract; pass readable UTF-8 JSON with unique keys and finite numbers", file=sys.stderr)
        return 2
    consumers = data.get("consumers") if isinstance(data, dict) else None
    if not isinstance(consumers, list) or not consumers:
        print("contract has no 'consumers' list; start from assets/messaging-contract.json", file=sys.stderr)
        return 2
    findings = 0
    for index, entry in enumerate(consumers):
        if not isinstance(entry, dict):
            print(f"FAIL consumers[{index}]: entry must be an object")
            findings += 1
            continue
        label = f"consumers[{index}]"
        for problem in check(entry):
            print(f"FAIL {label}: {problem}")
            findings += 1
    if findings:
        return 1
    print(f"OK {len(consumers)} consumers")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
