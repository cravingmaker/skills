---
name: postgres-concurrency-control
description: Prevent lost updates, write skew and double booking in PostgreSQL. Use when two requests race or a database invariant fails under concurrent writers; choose an atomic update, constraint, lock or Serializable retry and prove it with two real connections.
---

# PostgreSQL concurrency control

Name the forbidden committed outcome, enforce it in PostgreSQL, and reproduce it with two independent connections before claiming a fix.

## Establish the invariant

When the failure has no established cause, use the `diagnosing-bugs` skill first; enter here once the evidence identifies concurrent database decisions.

Read the operation and every writer, including jobs, imports and administrative paths. Record the isolation level, transaction boundary, rows or predicate involved, and external effects. Write a tiny initial state and the final states the domain permits; use those states as the test oracle.

Distinguish a lost update on one row from write skew across rows and from duplicate admission of an absent row. An HTTP replay policy belongs to the `idempotent-requests` skill; publication and consumer recovery belong to the `async-messaging` skill when those jobs apply and the skills are installed. Use the `postgres-schema-design` skill when the fix changes the schema and the `postgres-migrations` skill when it needs a live rollout. Read each named skill before using it; their summaries here add no installation requirement.

Done when the initial state, concurrent operations and forbidden committed state are explicit.

## Choose the smallest sufficient enforcement

| Invariant | Start with | Check |
| --- | --- | --- |
| An arithmetic change or version precondition concerns one row | One conditional `UPDATE ... WHERE ... RETURNING ...` | Affected-row count distinguishes success from conflict; the expression uses the current stored value. |
| Identity or a reservation range must be unique | A unique or exclusion constraint | Every writer meets it, including concurrent inserts into an initially empty range. |
| A decision needs existing rows kept stable | Lock those rows in a consistent order inside one short transaction | Re-read under the lock; choose `FOR NO KEY UPDATE` or `FOR UPDATE` from the actual key changes and lock conflicts. |
| A cross-row or absent-row predicate must stay true | A suitable constraint, a shared guard row all writers lock, or Serializable | Locking an empty result locks no future row; Repeatable Read alone can admit write skew. |

Keep one checked-out client or transaction handle for the entire transaction. Return clients on success, rollback, timeout and cancellation; discard a connection whose transaction state is uncertain. Put lock and statement deadlines inside the caller's remaining budget, and keep network calls outside the transaction. Treat `SKIP LOCKED` as a queue selection choice; skipping a row cannot prove a general business invariant.

Read [references/anomalies-and-retries.md](references/anomalies-and-retries.md) when choosing a lock, testing a predicate or defining retry behavior. Check the deployed server and driver's official documentation using [references/sources.md](references/sources.md) before relying on a version-dependent isolation, lock or error behavior.

Done when the enforcement covers every writer and a conflict has a defined result.

## Prove the interleaving

Use a fresh, explicitly disposable database and synthetic fixtures. Declare its identity before connecting; verify the server identity and current database before creating anything. Never infer disposability from a URL's spelling or from an ambient `DATABASE_URL`. Destructive operations on existing data require explicit user confirmation.

Adapt [assets/two-connections.ts](assets/two-connections.ts) or [assets/two-connections.rs](assets/two-connections.rs) when building a Node or Rust concurrency test. Compare each starter with the project's locked driver, runtime and fixture conventions before copying it; compile and execute the adapted test in that project. The starters accept two already checked-out connections, verify different backend PIDs, and coordinate reads with a bounded barrier. They require the caller to own a disposable fixture and its cleanup; they create no database or table themselves.

Place a barrier before a competing write or after the reads that create the stale decision. A barrier after acquiring a conflicting row lock can deadlock the test itself. Use timeouts to fail missing progress, not sleeps to guess that another transaction has reached a step. Wait for both participants to settle, then inspect committed state through another connection. The broken implementation must reach the forbidden state or fail its invariant assertion; restore the repair and show the allowed state.

For write skew, use two active duty rows with the invariant that at least one stays active. Synchronize both count reads before each worker deactivates a different row. Repeatable Read exposes the invalid zero-active state; a Serializable repair must retry and re-read before deciding. For a row-lock repair, use a schedule that lets the first lock holder commit while the second waits; do not reuse a two-reader barrier inside the locked section.

Done when the test exercises two real sessions and the asserted durable state distinguishes the broken and repaired implementations.

## Retry the whole decision

On SQLSTATE `40001` or `40P01`, abandon the failed transaction and rerun all reads, decisions and writes in a new transaction. Retry a finite number of times within one deadline, with bounded backoff and jitter supplied by the application. Do not retry a random connection error or a lost commit acknowledgement as though the previous commit certainly failed. Treat uniqueness violations as domain conflicts unless a documented case justifies a different policy.

Read [assets/serializable-retry.ts](assets/serializable-retry.ts) when adapting a Node retry wrapper; the Rust starter includes the same whole-transaction loop. The retried callback performs database work only. Put an external effect after confirmed commit or persist an outbox intent in the transaction, with a separate recovery policy for a lost acknowledgement. Test a failure at commit, an exhausted retry budget, cancellation, a non-retryable error and an external-effect counter outside the retried callback.

Done when a retry demonstrably re-reads the state, exhausted attempts leave no partial local effect, and external-effect boundaries are explicit.

## Return the evidence

Report the invariant, anomaly, chosen enforcement, old and new durable states, transaction attempts and the exact executed test command. Label local PostgreSQL, provider transport and CI evidence separately. When runtime access is unavailable, return the test and the missing target or capability; static review alone does not prove a race fix.
