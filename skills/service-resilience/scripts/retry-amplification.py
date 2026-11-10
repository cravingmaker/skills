#!/usr/bin/env python3
"""Check nested sequential retry attempts and deadline allocations.

Python 3.12+ standard library; read-only, offline, no prompts.
Usage: retry-amplification.py POLICY.json
stdout: JSON counts, allocation rows and finding codes (no source values).
stderr: usage/input diagnostics. Exit: 0 pass, 1 policy findings, 2 bad input.
Attempts include the first call. Layers are outermost to innermost.
Use "hops" instead of "layers" for sequential dependency operations: their
worst-case times add and their leaf attempt counts add. Nested layers multiply.
max_backoff_ms bounds each gap between attempts, including Retry-After if
honored. The bound includes (attempts - 1) such gaps, not one total delay.
This is a bound, not measured execution time.
"""

import argparse
import json
import math
import sys
from pathlib import Path


def unique(pairs):
    value = {}
    for key, item in pairs:
        if key in value:
            raise ValueError("duplicate JSON key")
        value[key] = item
    return value


def reject_constant(_):
    raise ValueError("non-finite JSON number")


def check_shape(policy):
    common = {"deadline_ms", "overhead_ms", "max_leaf_attempts"}
    if not isinstance(policy, dict) or set(policy) not in (common | {"layers"}, common | {"hops"}):
        raise ValueError("use deadline_ms, overhead_ms, max_leaf_attempts and either layers or hops")
    for field in ("deadline_ms", "max_leaf_attempts"):
        if type(policy[field]) is not int or policy[field] < 1:
            raise ValueError("use positive integer budgets")
    if type(policy["overhead_ms"]) is not int or policy["overhead_ms"] < 0:
        raise ValueError("use nonnegative integer overhead_ms")
    layers = policy.get("layers", policy.get("hops"))
    if not isinstance(layers, list) or not layers:
        raise ValueError("supply at least one outer-to-inner layer")
    names = set()
    for layer in layers:
        if not isinstance(layer, dict) or set(layer) != {
            "name", "attempts", "timeout_ms", "max_backoff_ms"
        }:
            raise ValueError("each layer needs name, attempts, timeout_ms, max_backoff_ms")
        name = layer["name"]
        if not isinstance(name, str) or not name.strip() or name in names:
            raise ValueError("supply distinct nonempty layer names")
        names.add(name)
        for field in ("attempts", "timeout_ms", "max_backoff_ms"):
            minimum = 0 if field == "max_backoff_ms" else 1
            if type(layer[field]) is not int or layer[field] < minimum:
                raise ValueError("use integer attempt, timeout and backoff bounds")


def evaluate(policy):
    check_shape(policy)
    nested = "layers" in policy
    layers = policy["layers"] if nested else policy["hops"]
    attempts = (math.prod if nested else sum)(layer["attempts"] for layer in layers)
    rows = [
        {
            "layer_index": index,
            "attempts": layer["attempts"],
            "timeout_ms": layer["timeout_ms"],
            "max_backoff_ms": layer["max_backoff_ms"],
            "worst_total_ms": (
                layer["attempts"] * layer["timeout_ms"]
                + (layer["attempts"] - 1) * layer["max_backoff_ms"]
            ),
        }
        for index, layer in enumerate(layers)
    ]
    findings = []
    if nested and sum(layer["attempts"] > 1 for layer in layers) > 1:
        findings.append("multiple_retry_owners")
    if attempts > policy["max_leaf_attempts"]:
        findings.append("leaf_attempt_budget_exceeded")
    for index in range(1, len(rows)) if nested else ():
        if rows[index]["worst_total_ms"] > rows[index - 1]["timeout_ms"]:
            findings.append(f"child_exceeds_parent_timeout:{index}")
    total = (rows[0]["worst_total_ms"] if nested else sum(row["worst_total_ms"] for row in rows)) + policy["overhead_ms"]
    if total > policy["deadline_ms"]:
        findings.append("end_to_end_deadline_exceeded")
    return {
        "leaf_attempts_upper_bound": attempts,
        "outer_bound_with_overhead_ms": total,
        "allocations": rows,
        "findings": findings,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("policy", type=Path)
    args = parser.parse_args()
    if sys.version_info < (3, 12):
        print("error: use Python 3.12 or later", file=sys.stderr)
        return 2
    try:
        policy = json.loads(args.policy.read_text(encoding="utf-8"),
                            object_pairs_hook=unique, parse_constant=reject_constant)
        result = evaluate(policy)
    except (OSError, UnicodeError, ValueError, RecursionError):
        print("error: read valid policy JSON with the fields shown in --help and the asset", file=sys.stderr)
        return 2
    print(json.dumps(result, sort_keys=True))
    return 1 if result["findings"] else 0


if __name__ == "__main__":
    sys.exit(main())
