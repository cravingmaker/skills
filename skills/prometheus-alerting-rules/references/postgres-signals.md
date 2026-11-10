# PostgreSQL signals

Read this when adding or repairing database collectors or rules; this is the postgres-monitoring and postgres-observability adapter. Use native PostgreSQL observations to define signal meaning, then the existing Prometheus rule and Alertmanager test path.

## Bind collection before alerting

Record server/extension/exporter versions, source view and column, unit, scope, collector role, freshness, reset marker and valid absence states for each metric. Verify views, column names and role requirements against the installed-major PostgreSQL documentation and the selected exporter's official documentation. Do not infer privilege or applicability from an empty query result. Use bounded aggregate queries; omit statement bodies, bind values, usernames and raw settings from shared evidence. Test collection with the intended least-privileged login and a fresh statistics snapshot, with the same pooling/session behavior as deployment. State whether a gauge is cluster-, database-, backend- or relation-scoped before aggregating it.

| Signal | Contract and discriminating check |
| --- | --- |
| Collection and connections | Distinguish exporter scrape success, SQL query permission, database reachability and expected target absence. Count connection states and remaining capacity using the applicable role/reserved-slot model; a successful exporter HTTP response alone proves none of those SQL permissions. |
| Locks and long transactions | Aggregate waiters, blocking duration and oldest transaction age; separately identify idle/prepared transactions when relevant. Keep blocker details in protected evidence and make no cancellation/termination automatic. |
| Statements and I/O | Name units, interval, extension enablement and reset epoch. Compute deltas only within the same epoch; cumulative totals from different windows cannot establish a regression. Record unavailable columns as unavailable. |
| Vacuum and freeze | Observe cleanup activity and transaction/multixact age against applicable configured horizons. Age and estimated dead tuples are separate signals; neither alone measures bloat or proves corruption. |
| WAL and checkpoints | Distinguish bytes, segments, elapsed time and rates; bind observed WAL generation, checkpoint pressure and free-space runway to one interval. A counter reset cannot become negative generation. |
| Archive and recoverability | Combine archive-failure increments with last-success age and expected WAL activity. No new WAL can legitimately leave an old success timestamp; a listed backup or quiet archive does not prove a usable restore chain. |
| Slots and replication | State primary/standby and physical/logical scope. Observe retained WAL bytes/runway, slot activity and actual catch-up. Preserve NULL lag or missing slot state rather than mapping it to zero lag. |
| Recovery coverage | Link to the latest independent recovery receipt and its scenario/age. A green backup job, exporter or alert does not establish recoverability. |

## Reset and absence semantics

Bind cumulative samples to postmaster/collector/statistics reset epochs where the source supplies them. Test independent instance resets before aggregation and explicitly model restart and Neon suspend/resume gaps. If the provider exposes only a subset of these observations, mark unsupported signals with a scoped alternative and owner; do not invent host or WAL-file access on Neon. Check current provider suspend/restart and metrics behavior in official Neon documentation before deciding what absence means. Determine whether the collector wakes or keeps compute active and record the cost effect; distinguish an expected suspension using independent provider state. Test primary/standby role changes so role-scoped alerts follow the new topology.

Preserve SQL NULL, metric absence, a reported zero and permission denial as separate states through the exporter adapter. A primary without an applicable replica may have undefined lag; a denied collector must produce a collection-failure signal, never a healthy zero. Use an independently maintained expected-target inventory to detect complete target disappearance; a metric derived solely from the disappearing target cannot discover every missing target.

## Fixture and delivery evidence

Native rule fixtures use synthetic aggregate metrics with an explicit adapter contract, not an assumed production exporter schema. Cover collector denial and complete absence, zero versus absent health gauges, archive failure then recovery, freeze age, retained WAL, missing versus NULL replication state, fresh epochs and suspend gaps. Verify expression outputs as well as pending/firing/resolved alerts, and ensure telemetry failure routes to an owner even when database symptom rules have no input.

Separately replay controlled cases through the actual collector on an explicitly disposable database using the intended role. Prove allowed collection and denied collection, verify units and NULL omission, and compare reset/absence output with the rule fixture contract. If no such target is available, label the collector replay unrun; native synthetic tests establish expression semantics only. For an actual incident, hand the bounded evidence to the existing runbook/incident owner; for collection changes or notifications follow the task's mutation authorization.
