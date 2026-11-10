# PostgreSQL incident entry

Read this when an alert concerns database acquisition, locks, WAL/archive progress or provider health. Prepare observations against the deployed major version and privileges; a missing view, permission denial, NULL or stale collector is an unknown, not zero.

## Choose the next observation

Record provider/project/branch/endpoint, database, effective role, server identity, writer/reader role, observation window and reset/restart/suspend context. Keep query text, parameter values, credentials and row data private. Use bounded, reviewed, read-only observations; diagnostic access does not authorize expensive statements, ANALYZE execution or cancellation.

| Observation | Competing cause | Discriminating next step |
| --- | --- | --- |
| Application pool wait is high | Local pool saturation, database connection limit, lock-blocked transactions, provider outage | Compare acquisition/queue/active counts with a direct authorized database reachability observation and backend wait/blocking evidence. |
| Database sessions are waiting | Lock contention versus CPU/I/O or client waits | Inspect wait category and blocking relationships through `pg_stat_activity`, `pg_locks` and `pg_blocking_pids` as supported. Avoid exposing SQL text or assuming the oldest session is the blocker. |
| WAL/slot pressure rises | Slow or absent consumer, stalled archive, traffic spike or reset | Compare interval WAL generation, slot retention/consumer progress and `pg_stat_archiver` failure/progress with filesystem/provider capacity. Record observation epochs. |
| Archive failure is reported | Credentials/destination outage, permissions, archive command failure or missing collector | Verify the provider/archiver's native status and the last successful archive boundary. A missing metric cannot establish archive success. |
| Provider connection fails | Provider outage, suspended compute, wrong endpoint, TLS/authentication or local network | Compare provider status/endpoint identity with a safe direct connection and transport evidence. Bound retries; do not classify an authentication denial as capacity. |

Use the `postgres-connection-pooling` skill when installed and read first for pool topology, acquisition budgets and transport/session behavior. Use the `postgres-query-performance` skill when installed and read first for representative query or wait diagnosis. Use the `postgres-change-execution` skill when installed and read first for direct administrative mutation, including cancellation/termination, slot removal or emergency data changes. Hand recovery to the backup/recovery owner with the exact recovery point and coverage gap; do not invent an unavailable recovery skill.

## Prepare bounded mitigation

Describe each mitigation's exact target, preconditions, maximum effects, authority reference, deadline, abort and independent recovery check. Canceling work, terminating a session, dropping a slot and discarding data have different effects; none follows automatically from observing pressure. Preserve application consistency and needed WAL before any destructive action. Use the target-bound change method for execution and usable recovery evidence for destructive effects.

Canceling an idle transaction does not end it or release its transaction-held locks; the application owner must end that transaction or explicitly authorize a stronger action through the change method. An active replication slot can still lag and retain WAL. A healthy provider status page cannot exclude a local or unreported outage. Use interval progress and native connection evidence rather than those labels alone.

## Required rehearsal fixtures

- **Lock versus pool exhaustion.** Use a disposable database/application with a deliberately blocked transaction and a saturated application pool. Provide pool queue evidence plus native blocking/wait observations. The procedure must inspect the blocker before recommending a larger pool or a restart. A second fixture has high acquisition latency with no blocker and exhausted connections, so the same observations must take a different branch.
- **Unknown collector.** Deny the diagnostic role or remove a collector response. The procedure must escalate the observation gap; it cannot emit a healthy/zero conclusion or execute mitigation.
- **WAL/archive failure.** Pause a disposable consumer or archive destination, observe retention/progress and distinguish the stalled component. Restore it and verify progress plus an application transaction; do not delete a live slot or WAL directory.

Label synthetic saved observations as branch tests only. A sandbox operator run against the actual disposable service is still required before recording a successful rehearsal. Never run these fixtures against production.

## Primary references

At use time select the installed major's [monitoring views](https://www.postgresql.org/docs/current/monitoring-stats.html), [locks](https://www.postgresql.org/docs/current/explicit-locking.html), [statistics functions](https://www.postgresql.org/docs/current/functions-info.html) and [WAL archiving](https://www.postgresql.org/docs/current/continuous-archiving.html). For a managed target, verify supported observations and recovery against its provider's official docs, including [Neon connection pooling](https://neon.com/docs/connect/connection-pooling) and [compute lifecycle](https://neon.com/docs/manage/computes) where applicable. Provider capabilities and view schemas are checked live, never copied from a different major or plan.
