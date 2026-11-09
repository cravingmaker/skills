#!/usr/bin/env python3
"""Summarize one saved PostgreSQL EXPLAIN JSON document, optionally beside another.

Python 3.12+, standard library; reads local JSON, never executes SQL or writes.
Numeric/structural JSON on stdout; diagnostics on stderr. Exits: 0 no triage
flags, 1 triage flags (not a regression verdict), 2 malformed input/usage.
--help has no effects. Output omits query, relation, index and filter text.
"""

import argparse
import json
import math
import sys
from pathlib import Path

BUFFERS = ("Shared Hit Blocks", "Shared Read Blocks", "Shared Dirtied Blocks",
           "Shared Written Blocks", "Local Hit Blocks", "Local Read Blocks",
           "Temp Read Blocks", "Temp Written Blocks")
NODE_TYPES = set("Seq Scan|Parallel Seq Scan|Index Scan|Index Only Scan|Bitmap Heap Scan|Bitmap Index Scan|BitmapAnd|BitmapOr|Tid Scan|Tid Range Scan|Subquery Scan|Function Scan|Values Scan|CTE Scan|Named Tuplestore Scan|WorkTable Scan|Foreign Scan|Custom Scan|Nested Loop|Merge Join|Hash Join|Hash|Aggregate|Group|Sort|Incremental Sort|Unique|SetOp|LockRows|Limit|Materialize|Memoize|Append|Merge Append|Recursive Union|Gather|Gather Merge|Result|ProjectSet|ModifyTable|WindowAgg".split("|"))


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("duplicate key")
        result[key] = value
    return result


def number(node, key):
    value = node.get(key)
    if value is None and key not in node:
        return None
    if type(value) not in (int, float) or not math.isfinite(value) or value < 0:
        raise ValueError("invalid metric")
    return value


def metrics(node):
    return {key: number(node, key) for key in BUFFERS if key in node}


def summarize(path, args):
    document = json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=unique_object)
    if not isinstance(document, list) or len(document) != 1 or not isinstance(document[0], dict):
        raise ValueError("expected one EXPLAIN statement")
    statement = document[0]
    root = statement.get("Plan")
    if not isinstance(root, dict):
        raise ValueError("missing Plan")
    nodes, findings = [], []

    def walk(node, address, under_limit=False):
        if not isinstance(node, dict) or not isinstance(node.get("Node Type"), str):
            raise ValueError("invalid node")
        kind = node["Node Type"] if node["Node Type"] in NODE_TYPES else "Other"
        estimated, actual, loops = (number(node, key) for key in ("Plan Rows", "Actual Rows", "Actual Loops"))
        if (actual is None) != (loops is None):
            raise ValueError("incomplete execution metrics")
        flags, factor = [], None
        if loops is None:
            flags.append("missing_execution")
        elif loops == 0:
            flags.append("not_executed")
        elif estimated is not None:
            if estimated == 0 and actual > 0:
                flags.append("zero_estimate")
            elif actual == 0 and estimated > 0:
                flags.append("possibly_stopped_early" if under_limit else "zero_actual")
            elif actual > 0 and estimated > 0:
                factor = max(actual / estimated, estimated / actual)
                if not math.isfinite(factor):
                    raise ValueError("metric overflow")
                if factor >= args.estimate_factor:
                    flags.append("possibly_stopped_early" if under_limit and actual < estimated else "estimate_error")
        removed_filter = number(node, "Rows Removed by Filter")
        removed_recheck = number(node, "Rows Removed by Index Recheck")
        total_rows = actual * loops if actual is not None else None
        if total_rows is not None and not math.isfinite(total_rows):
            raise ValueError("metric overflow")
        examined_rows = (actual + (removed_filter or 0) + (removed_recheck or 0)) * loops if actual is not None else None
        if examined_rows is not None and not math.isfinite(examined_rows):
            raise ValueError("metric overflow")
        observed_rows = examined_rows if examined_rows is not None else estimated
        if kind in ("Seq Scan", "Parallel Seq Scan") and observed_rows is not None and observed_rows >= args.large_scan_rows:
            flags.append("large_sequential_scan")
        if loops is not None and loops >= args.high_loops:
            flags.append("many_loops")
        if node.get("Sort Space Type") == "Disk":
            flags.append("disk_sort")
        buffers = metrics(node)
        if buffers.get("Temp Read Blocks", 0) or buffers.get("Temp Written Blocks", 0):
            flags.append("temp_io")
        if buffers.get("Shared Read Blocks", 0):
            flags.append("shared_reads")
        batches = number(node, "Hash Batches")
        if batches is not None and batches > 1:
            flags.append("hash_batches")
        planned = number(node, "Workers Planned")
        launched = number(node, "Workers Launched")
        if planned is not None and launched is not None and launched < planned:
            flags.append("fewer_workers")
        workers = node.get("Workers", [])
        if not isinstance(workers, list) or any(not isinstance(worker, dict) for worker in workers):
            raise ValueError("invalid workers")
        worker_metrics = []
        for worker in workers:
            worker_buffers = metrics(worker)
            worker_flags = []
            if worker.get("Sort Space Type") == "Disk":
                worker_flags.append("disk_sort")
            if worker_buffers.get("Temp Read Blocks", 0) or worker_buffers.get("Temp Written Blocks", 0):
                worker_flags.append("temp_io")
            worker_batches = number(worker, "Hash Batches")
            if worker_batches is not None and worker_batches > 1:
                worker_flags.append("hash_batches")
            worker_metrics.append({"number": number(worker, "Worker Number"),
                                   "actual_rows_per_loop": number(worker, "Actual Rows"),
                                   "loops": number(worker, "Actual Loops"), "buffers": worker_buffers,
                                   "sort_space_kb": number(worker, "Sort Space Used"),
                                   "hash_batches": worker_batches, "flags": worker_flags})
        if any(worker["flags"] for worker in worker_metrics):
            flags.append("worker_spill")
        output = {"path": address, "node_type": kind, "estimated_rows": estimated,
                  "actual_rows_per_loop": actual, "loops": loops, "approx_total_rows": total_rows,
                  "rows_removed_by_filter_per_loop": removed_filter,
                  "rows_removed_by_recheck_per_loop": removed_recheck,
                  "approx_examined_rows": examined_rows,
                  "estimate_factor": factor, "buffers": buffers, "hash_batches": batches,
                  "sort_space_kb": number(node, "Sort Space Used"), "workers": worker_metrics,
                  "workers_planned": planned, "workers_launched": launched,
                  "flags": flags}
        nodes.append(output)
        findings.extend({"path": address, "kind": flag} for flag in flags)
        children = node.get("Plans", [])
        if not isinstance(children, list):
            raise ValueError("invalid Plans")
        for index, child in enumerate(children):
            walk(child, address + [index], under_limit or kind == "Limit")

    walk(root, [])
    execution = number(statement, "Execution Time")
    if execution is None:
        findings.append({"path": [], "kind": "missing_execution_time"})
    return {"planning_ms": number(statement, "Planning Time"), "execution_ms": execution,
            "root_buffers_inclusive": metrics(root), "nodes": nodes, "findings": findings}


def positive(value):
    try:
        parsed = float(value)
        if math.isfinite(parsed) and parsed > 0:
            return parsed
    except ValueError:
        pass
    raise argparse.ArgumentTypeError("use a finite positive threshold")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("plan", type=Path, help="one saved EXPLAIN JSON array")
    parser.add_argument("--compare", type=Path, help="candidate saved plan; side-by-side metrics only")
    parser.add_argument("--estimate-factor", type=positive, default=10, help="triage factor, default 10")
    parser.add_argument("--large-scan-rows", type=positive, default=100000, help="triage scan rows, default 100000")
    parser.add_argument("--high-loops", type=positive, default=1000, help="triage loops, default 1000")
    args = parser.parse_args()
    if sys.version_info < (3, 12):
        print("error: use Python 3.12+ to run explain-summary.py", file=sys.stderr)
        return 2
    try:
        baseline = summarize(args.plan, args)
        if args.compare:
            candidate = summarize(args.compare, args)
            before, after = baseline["execution_ms"], candidate["execution_ms"]
            result = {"baseline": baseline, "candidate": candidate,
                      "execution_ms_delta": after - before if before is not None and after is not None else None}
            flagged = bool(baseline["findings"] or candidate["findings"])
        else:
            result, flagged = baseline, bool(baseline["findings"])
        encoded = json.dumps(result, sort_keys=True, allow_nan=False)
    except (OSError, UnicodeError, ValueError, TypeError, KeyError, RecursionError, OverflowError):
        print("error: supply one valid UTF-8 EXPLAIN JSON array with a Plan tree and finite nonnegative metrics; keep raw plans private", file=sys.stderr)
        return 2
    print(encoded)
    return int(flagged)


if __name__ == "__main__":
    sys.exit(main())
