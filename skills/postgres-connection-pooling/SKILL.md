---
name: postgres-connection-pooling
description: Choose PostgreSQL connection paths and budget pools across peak app instances, workers, migrations and an operator reserve. Use for too many connections, acquisition waits, serverless database access or direct versus transaction-pooled endpoints; verify the actual transport and session needs.
---

# PostgreSQL connection pooling

Budget every connection path and test the features the deployed transport must support. A pool limit bounds connections; measured acquisition wait and database work determine whether that limit serves the workload.

## Map the paths

Read runtime, deployment and driver configuration without printing URLs or credentials. Inventory peak overlapping instances during rollout, processes per instance, workers, per-process pools, migration jobs and other clients sharing the database. Record each path's transport, endpoint type, application role, transaction needs and lifecycle owner. Keep migration credentials separate from application credentials.

Distinguish application pool wait from pooler queueing, database lock waits, execution time, connection setup and provider cold starts. Use the `postgres-query-performance` skill when database execution dominates, and the `postgres-concurrency-control` skill when correctness depends on transaction ownership or locking. Provisioning a Neon project or branch is a separate job; this skill selects and verifies connections to an already authorized target.

Done when every pool and its peak multiplicity has an owner and the suspected wait has a measured location.

## Choose the connection contract

| Need | Candidate path | Required evidence |
| --- | --- | --- |
| A fixed query or non-interactive batch on a supported Neon runtime | HTTP driver | The installed driver supports the batch's transaction and isolation needs; partial failure rolls back the batch. |
| A later statement depends on an earlier result | A persistent client, including a supported WebSocket client | One checked-out connection owns the whole interactive transaction. |
| Session state across transactions | A compatible direct or session-pooled path | The state survives the required lifecycle and is reset before another borrower uses the connection. |
| Ordinary short transactions through PgBouncer | A transaction-pooled endpoint | Every required feature works without depending on affinity across commits. |
| Migrations, dump or session-dependent administrative tools | A direct endpoint | The tool and role are compatible; its peak connections appear in the budget. |

Verify supported transports, runtime lifetimes, pooler mode, provider limits and driver behavior at use time using [references/sources.md](references/sources.md). Keep numeric provider limits out of standing defaults. HTTP can support transactional batches; a fixed batch is different from interactive read-then-decide code. WebSocket transport alone does not turn a transaction-pooled endpoint into a persistent backend session.

Read [references/transport-compatibility.md](references/transport-compatibility.md) when auditing session features or prepared statements. Treat URL suffixes as an inventory hint and confirm the endpoint configuration. Inspect actual reachable code paths and driver configuration. Use [scripts/find-session-features.py](scripts/find-session-features.py) on declared pooled paths to locate candidate session features:

```sh
python3 scripts/find-session-features.py src/pooled
```

The read-only Python helper prints `path:line: feature: fix` on stdout and diagnostics on stderr; exits are 0 no candidates, 1 candidates, 2 usage or unreadable/empty scope. It skips dependency/build directories and echoes no source lines. `--help` has no effects. Confirm every finding; suppress a reviewed exception with `pooler-ok: <reason>` on its line. Passing the text scan proves no transport compatibility; retain the actual endpoint tests.

Done when each path has a justified feature contract and a test against the actual endpoint type.

## Compute the peak budget

Adapt [assets/budget.json](assets/budget.json) to the deployment before running [scripts/pool-budget.py](scripts/pool-budget.py). The fixture numbers are arithmetic examples, never sizing recommendations. Read [references/budget-format.md](references/budget-format.md) when filling the input or interpreting its independent limits.

```sh
python3 scripts/pool-budget.py budget.json
```

The helper uses Python 3.12+ and the standard library, reads one explicit JSON file and makes no network or database calls. It emits JSON counts on stdout and diagnostics on stderr; exits are 0 within budget, 1 a limit exceeded, 2 malformed input or usage. `--help` exits 0 without inspecting a target or writing anything.

Direct sessions equal the sum of peak processes times pool maximum for every direct group. For a pooler, separately count client connections and the aggregate backend allocation across its users, databases and replicas. Count backend allocations against the server budget; counting all pooled client connections as PostgreSQL sessions gives the wrong topology. Account for other services, server-reserved slots, simultaneous migrations and an additional operator reserve without counting the same reserve twice. Include rollout overlap and worker fan-out in the input; an omitted deployment group cannot be discovered by arithmetic.

Done when both server and pooler client budgets pass against observed limits and every input has a deployment or provider source.

## Exercise the path and lifecycle

Use synthetic fixtures on an explicitly disposable target, with its identity checked before any write. Use the `integration-test-harness` skill when setting up that fixture or its result evidence. Destructive operations on existing data require explicit user confirmation.

Test commit, rollback after a failing statement, independent committed readback and the session features the application actually uses. For transaction pooling, create competing transactions that occupy backend slots and force reassignment; a one-client success can hide accidental session affinity. For prepared statements, exercise the driver's real protocol behavior after reassignments and reconnections. Use a direct connection for a listener or persistent advisory lock when the deployed pooler cannot preserve it.

Measure acquisition time, waiters, active and idle clients, pooler wait, database work and error rate under the stated authorized workload. Prove clients return after exceptions, timeouts and cancellation, and prove shutdown drains work before closing the pool. On edge runtimes, verify whether a connection may outlive a request rather than caching it by assumption. A larger pool needs new measurements; it can increase expensive database contention while shortening an application queue.

Done when the deployed transport passes its feature tests and the stated workload fits the connection and wait budgets.

## Return the evidence

Report the topology, redacted endpoint identifiers, sourced peak counts, computed headroom, tested features and measured wait location. Separate local PostgreSQL tests from provider tests and CI results. If an endpoint or runtime is unavailable, name the untested compatibility case; a passing arithmetic check proves only the supplied budget.
