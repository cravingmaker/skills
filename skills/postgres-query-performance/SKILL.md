---
name: postgres-query-performance
description: Diagnose slow PostgreSQL queries from workload statistics and representative plans. Use for a slow endpoint, N+1 calls or an index proposal; compare EXPLAIN JSON, row estimates, loops, spill and buffers, with safe execution scope and evidence before removing an index.
---

# PostgreSQL query performance

Find the expensive query or query pattern, preserve its correctness, and compare representative evidence before changing it.

## Rank the workload

Bind the symptom to an endpoint or job, a query shape, safe parameter classes and the observation window. Rank by total execution contribution and call count using the deployed `pg_stat_statements` schema when available; inspect per-call latency and tail cases separately. Check application traces for N+1 requests and overfetching; one fast query repeated per row can dominate a request. Separate execution from pool acquisition, lock waits, network transfer and response serialization. Use the `postgres-connection-pooling` skill when acquisition or connection setup dominates.

Record database and node identity, statistics reset epoch, observation start/end, restarts or compute replacements, role visibility, and workload coverage. Retain those facts for index-usage observations too; a zero counter after a reset or on one reader is weak evidence about a cluster's workload. Read [references/workload-evidence.md](references/workload-evidence.md) when collecting statistics or judging an unused-index claim.

Compare [assets/workload-observations.sql](assets/workload-observations.sql) with the deployed PostgreSQL and extension schema when preparing read-only workload or index-usage queries; supply the extension schema explicitly and keep the output private.

Done when the ranked query accounts for a measured part of the symptom and the observation's limits are explicit.

## Capture a safe, representative plan

Inspect the installed server, extension and client versions, then use their official documentation in [references/sources.md](references/sources.md). Start with estimated `EXPLAIN (FORMAT JSON)` when execution authority or cost is uncertain. `EXPLAIN ANALYZE` executes the statement, including functions called by a `SELECT`. Read access to a database does not authorize an expensive or mutating diagnostic.

Run measured plans only within the authorized execution budget. Prefer synthetic, explicitly disposable data with representative cardinality, skew, tenant sizes, nulls and parameter selectivity. Use a read-only transaction and suitable statement/lock limits for an approved pure read, after checking its functions and external effects. For writes, use a disposable target and an intentional rollback; rollback does not undo sequences or external effects. Destructive operations on existing data require explicit user confirmation.

Capture `EXPLAIN (ANALYZE, BUFFERS, FORMAT JSON)` only when those conditions hold. Keep SQL text, parameter values and relation identifiers private; exported plans and statistics can contain them. Retain raw plans in an approved private artifact and publish only a scrubbed summary.

Run [scripts/explain-summary.py](scripts/explain-summary.py) on saved JSON; it does not connect to a database or execute SQL.

```sh
python3 scripts/explain-summary.py before.json
python3 scripts/explain-summary.py before.json --compare after.json
```

The helper needs Python 3.12+ and the standard library. It emits numeric and structural JSON on stdout, diagnostics on stderr, and exits 0 without triage flags, 1 with flags, or 2 for malformed input or usage. `--help` exits 0 without reading a plan or writing anything. Its estimate-factor, large-scan and high-loop thresholds are configurable triage defaults, not database limits or automatic tuning decisions. An estimated-only plan is reported as missing execution evidence, never as a measured improvement.

Read [references/reading-plans.md](references/reading-plans.md) when interpreting per-loop rows, worker detail, buffer counters or before/after output. Done when the plan represents the actual parameter classes and its execution authority and dataset are recorded.

## Test one cause

| Evidence | Candidate cause | Discriminating check |
| --- | --- | --- |
| Large estimate error | Stale or insufficient statistics, correlated predicates, parameter skew | Compare row counts and statistics; test relevant parameter classes and generic versus custom plans. |
| Many loops or many calls | Nested work or N+1 requests | Count request SQL calls and inner-node work; batch or reshape the query and preserve its result semantics. |
| Sort or hash spill | Work exceeds available memory for that operation | Inspect temp I/O, disk sort or hash batches, concurrent nodes and workers before proposing a scoped setting. |
| Many pages scanned for few relevant rows | Missing usable access path or unsuitable predicate | Compare candidate indexes and sargable query shapes on the same data and workload. |
| Long time with little row work | Lock, storage, scheduling or provider delay | Match wait evidence and elapsed time; do not infer the cause from plan costs alone. |

Choose composite B-tree order from predicates and ordering, then test selectivity and ordering requirements. Evaluate partial predicates, expression matching, covering columns and heap visibility before promising index-only scans. Use GIN for matching search operators and BRIN when physical range correlation makes it useful. Verify skip-scan support on the deployed major version; an omitted leading predicate is a measurement question, not an automatic rejection or guarantee. A sequential scan can be the best plan for a small table or a large result fraction.

Read [references/index-choice.md](references/index-choice.md) when comparing index shapes, existing indexes or foreign-key access paths.

Use the `postgres-schema-design` skill when index changes expose missing constraints, and the `postgres-migrations` skill for an online index rollout when those skills are installed. Use the `benchmark-checklist` skill for a reported speedup that needs comparable repeated measurements. Read each named skill before relying on it. Keep operational index reconstruction with the maintenance owner and its lock, space, WAL and recovery plan. An estimated bloat percentage or unused sample does not authorize a rebuild or removal.

Done when one changed cause explains an observed difference and the result set, ordering, null behavior and concurrent write behavior remain correct.

## Compare and return

Compare baseline and candidate on the same workload, data distribution, parameter classes, engine, settings and cache conditions. Record changed statistics or indexes explicitly; repeat enough measurements to expose noise, and report the full unsuccessful cases as well as the favorable one. Plan timing alone does not establish endpoint latency or capacity; measure those claims through the actual endpoint and authorized workload.

Report raw private plan locators, scrubbed summaries, calls, elapsed distributions, loops, reads, spill, write/storage costs, correctness checks and remaining limits. Keep local, CI and deployed measurements separate. If execution was unavailable, provide the estimated plan and next discriminating check; leave the performance claim unproven.
