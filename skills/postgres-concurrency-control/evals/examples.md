# Examples

Paired model runs are pending; keep the catalog entry unevaluated.

## Activation

- "Two requests both spend the last unit of stock." Expect: state the stock invariant and reproduce the stale decision with two real sessions before choosing an atomic conditional change.
- "Both doctors go off duty even though one must stay on call." Expect: demonstrate cross-row write skew and test a repair that re-evaluates the predicate.
- "Our Serializable transaction sometimes raises 40001 at commit." Expect: retry the entire transaction within one finite budget and keep external effects outside its callback.

## Near miss

- "Replay the saved HTTP response when a payment key is reused." Expect: use the `idempotent-requests` skill when available; the job is request admission and replay.
- "The consumer publishes twice after a crash." Expect: use the `async-messaging` skill when available for publication and acknowledgement boundaries.
- "Design primary and foreign keys for the new tables." Expect: use the `postgres-schema-design` skill when available; the job is schema shape.
- "This query is slow with one client." Expect: use the `postgres-query-performance` skill for measured query evidence.

- "Checkout fails intermittently and we have no idea why." Expect: use the `diagnosing-bugs` skill before choosing a race mechanism.

## Outcome

- "Prove the counter repair." Fixture: one table with integer value zero, two clients, both reads released by a barrier, then two stale absolute updates. Expect: the broken case commits one; the atomic increment case commits two, read independently after both finish.
- "Prove duty coverage." Fixture: two active rows, two synchronized count reads and disjoint deactivations. Expect: the broken Repeatable Read case reaches zero; Serializable retries re-read and preserve one active row.
- "Check retry safety." Fixture: a driver adapter fails the first commit with SQLSTATE 40001, then commits; a second adapter always fails and a third raises a connection error without SQLSTATE. Expect: complete body replay only in the eligible cases, finite exhaustion, all clients released, and one external effect after confirmed success.
