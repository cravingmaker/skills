# Anomalies and retries

Read this when selecting an enforcement mechanism or designing a race schedule.

## Separate the causes

**Lost update.** Both transactions read balance zero, calculate one in application code, then each stores one. An atomic increment stores two; a conditional version update makes one stale decision fail. Check the returned row count rather than treating a completed SQL call as a successful business change.

**Write skew.** Two rows are active and each transaction observes two before deactivating its own row. Disjoint writes can both commit under snapshot isolation. Use a constraint that represents the rule, a shared locked guard row used by all writers, or Serializable with retries.

**Absent-row race.** Two requests find no overlapping reservation and both insert. Locking the empty search result protects nothing. A unique violation (`23505`) or exclusion violation (`23P01`) is a domain conflict; for equality plus range exclusion, verify the required operator classes and extension availability, such as `btree_gist`. Test the constraint or predicate protection with both reads completed before either insert.

**Deadlock.** Transactions acquire the same resources in different orders. Use a canonical lock order and short transactions, then retry the entire transaction after a deadlock error within its finite budget. An increased lock timeout does not remove the cycle.

## Lock choices

Inspect the target server's lock-conflict table and actual key changes. Use the least restrictive row lock that protects the decision; foreign-key writers may need different compatibility from key-changing updates. A transaction-level advisory lock is released with the transaction, but protects an invariant only if every writer follows the protocol. A session-level advisory lock has different pooling and release requirements. Acquire any guard row before reading the predicate it protects.

For a queue claim, select eligible rows with `FOR UPDATE SKIP LOCKED` and record the claim in the same transaction. Test that concurrent workers receive distinct claims; this selection rule does not enforce a general cross-row invariant.

## Retry contract

Every writer affecting a Serializable predicate must use the same enforcement protocol; Serializable protects the set of transactions that actually run at that level. An attempt includes transaction start, every read and write, and commit. A result from the callback is provisional until commit succeeds. A rollback failure requires discarding the connection; expose a redacted error without leaking SQL, parameters or connection strings. Use driver SQLSTATE fields, not message substring matching.

Force one `40001` at commit in an adapter test and verify that the body executes again on a new transaction. Then inject `40P01`, an ordinary domain error, cancellation and exhaustion separately. Keep the fake limited to wrapper control flow; the race and the invariant still need real PostgreSQL evidence.

Use the `integration-test-harness` skill when fixture readiness, independent commit observations or interrupted cleanup need work.

## Cleanup and failures

Run all participant futures to completion or cancel them explicitly before releasing their connections. The fixture owner rolls back open transactions, releases clients and removes only the run's resources. Prove cleanup after an assertion failure and a terminated test process; retain resource identifiers for an authorized reaper after a hard kill.
