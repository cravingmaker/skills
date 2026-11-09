#!/usr/bin/env python3
"""Check an explicit peak connection budget. Python 3.12+, standard library.

Reads JSON only; no writes, prompts, network or database connections.
JSON results on stdout, diagnostics on stderr. Exits: 0 within all limits,
1 a limit exceeded, 2 usage/unreadable/malformed input. --help has no effects.
"""

import argparse
import json
import sys
from pathlib import Path


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("duplicate key")
        result[key] = value
    return result


def fields(value, required):
    if not isinstance(value, dict) or set(value) != set(required):
        raise ValueError("fields")


def count(value, minimum=0):
    if type(value) is not int or value < minimum:
        raise ValueError("count")
    return value


def group_total(groups):
    if not isinstance(groups, list):
        raise ValueError("groups")
    total = 0
    for group in groups:
        fields(group, ("instances", "pool_max"))
        total += count(group["instances"], 1) * count(group["pool_max"], 1)
    return total


def budget(data):
    fields(data, ("database_limit", "unavailable_connections", "other_connections",
                  "migration_connections", "operator_reserve", "direct_groups", "poolers"))
    limit = count(data["database_limit"], 1)
    unavailable = count(data["unavailable_connections"])
    other = count(data["other_connections"])
    migration = count(data["migration_connections"])
    reserve = count(data["operator_reserve"], 1)
    direct = group_total(data["direct_groups"])
    if not isinstance(data["poolers"], list) or not (direct or data["poolers"]):
        raise ValueError("empty topology")
    poolers, findings = [], []
    backend = 0
    for index, pooler in enumerate(data["poolers"]):
        fields(pooler, ("client_groups", "client_limit", "backend_slots"))
        clients = group_total(pooler["client_groups"])
        if clients == 0:
            raise ValueError("empty pooler")
        client_limit = count(pooler["client_limit"], 1)
        slots = count(pooler["backend_slots"], 1)
        backend += slots
        poolers.append({"index": index, "clients": clients, "client_limit": client_limit,
                        "client_headroom": client_limit - clients, "backend_slots": slots})
        if clients > client_limit:
            findings.append({"kind": "pooler_client_limit", "index": index})
    total = direct + backend + unavailable + other + migration + reserve
    if total > limit:
        findings.append({"kind": "database_limit"})
    return {"database_limit": limit, "database_total": total, "database_headroom": limit - total,
            "direct_sessions": direct, "pooled_backend_slots": backend,
            "unavailable_connections": unavailable, "other_connections": other,
            "migration_connections": migration, "operator_reserve": reserve,
            "poolers": poolers, "findings": findings}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("budget", type=Path, help="explicit budget JSON; see references/budget-format.md")
    args = parser.parse_args()
    if sys.version_info < (3, 12):
        print("error: use Python 3.12+ to run pool-budget.py", file=sys.stderr)
        return 2
    try:
        data = json.loads(args.budget.read_text(encoding="utf-8"), object_pairs_hook=unique_object)
        result = budget(data)
    except (OSError, UnicodeError, ValueError, TypeError, KeyError, RecursionError, OverflowError):
        print("error: supply valid UTF-8 budget JSON with exactly the fields in references/budget-format.md; use integer counts and a positive operator reserve", file=sys.stderr)
        return 2
    print(json.dumps(result, sort_keys=True, allow_nan=False))
    return int(bool(result["findings"]))


if __name__ == "__main__":
    sys.exit(main())
