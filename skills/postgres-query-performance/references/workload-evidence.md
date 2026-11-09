# Workload evidence

Read this when collecting query statistics or considering index removal.

## Statistics record

Record the cluster, node, database, observation window and reset epoch using redacted stable identifiers. Record server start or compute replacement and any extension reset or statistics eviction in that window. Inspect extension availability, schema, privileges and column names on the target version before preparing read-only statistics SQL. Enabling or resetting an extension changes the environment and needs the applicable authority.

Rank query IDs by total execution time and calls, then inspect average, distribution and representative slow parameter classes. Retain application call counts and bytes, since a query-statistics average does not identify endpoint tails or application fan-out. Use the same observation scope when comparing a baseline and candidate; cumulative totals over different lifetimes are not comparable rates.

## Index decisions

Collect index definitions, validity, ownership of constraints, table size, write rate and relevant query plans. Include replicas, failover roles, batch jobs, periodic maintenance and rare high-value reads in the workload inventory. A visible zero scan count can follow a reset, insufficient privileges, a short window or a role change. Even a genuinely unused access path can implement uniqueness or another constraint.

Propose removal only with dependency checks, representative full-cycle observations, measured write/storage costs, a re-creation plan and explicit user confirmation for the destructive change. Use the `postgres-migrations` skill for an authorized online removal when installed. Distinguish dead-tuple estimates, reusable space, measured bloat and corruption; none is interchangeable with another. Operational rebuilds belong to a maintenance plan that budgets locks, temporary space, WAL and replica catch-up, with an interruption/recovery check.

## Safe source capture

Keep query text, literals, filters and plans in access-controlled artifacts. A normalizing extension can still reveal SQL constants, object names or query structure; never assume it removes private content. For public tests, use the synthetic plans in this skill's tests rather than customer captures.
