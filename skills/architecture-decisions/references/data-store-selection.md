# Data-store selection

Read this when a datastore choice depends on recovery, concurrency, precision, or operating constraints.

Start with a logical input fixture and an independent expected result. Preserve required numeric precision, signs, ordering, nulls, identifiers, time zones, units, and source bytes. If a candidate cannot express the required semantics, disqualify it before comparing speed. For domain identities and relationships, use the `logical-data-modeling` skill when available.

For immutable Parquet manifests versus DuckLake, Iceberg, or Delta, use the analytical-table adapter linked from SKILL.md. A table format needs a demonstrated concurrent-writer, snapshot, or multi-engine requirement; compare plain files when they meet the workload.

Declare these cases before testing:

| Constraint | Disqualifying observation | Evidence |
| --- | --- | --- |
| Precision | Required source values change on write or readback | Exact values or bytes compared with the independent fixture |
| Concurrency | Two controlled writers commit a forbidden state | Barrier-driven schedule, final state, and transaction results |
| Recovery | Acknowledged effects disappear or replay duplicates them beyond the agreed scope | Crash point, durable checkpoint, restart, reconciliation |
| Recovery objectives | Restore exceeds the agreed time or loss window | Backup identity, restore log, logical comparison, elapsed time |
| Operations | Required privileges, topology, staffing, cost, or lifecycle support are unavailable | Verified vendor constraints and a dated operating model |

Use the same logical dataset and operations for every candidate. Record physical differences such as indexes or partitioning; equal semantics do not imply identical physical designs. Hold hardware budgets and concurrency comparable, separate cold and warm runs, and record errors and incomplete work alongside throughput. The `benchmark-checklist` skill owns measured-advantage claims when installed.

Use an explicit disposable target and a finite work budget. Capture exact tool and server versions, commands, input hashes, results, and deviations. Load and fault injection require an owned authorized target; do not infer authorization for a production restore. Destructive data operations need explicit user confirmation.

For PostgreSQL behavior, consult the tested release's [transaction isolation documentation](https://www.postgresql.org/docs/current/transaction-iso.html), [numeric types](https://www.postgresql.org/docs/current/datatype-numeric.html), and [backup and restore documentation](https://www.postgresql.org/docs/current/backup.html). For another datastore, verify the equivalent guarantees in its official release documentation. Do not equate a consistency label or a vendor benchmark with an end-to-end result.
