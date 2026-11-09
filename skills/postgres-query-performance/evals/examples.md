# Examples

Paired model runs are pending; keep the catalog entry unevaluated.

## Activation

- "This endpoint issues hundreds of SQL calls and is slow." Expect: rank request call count and total query contribution before changing an index.
- "Should we add a composite index to this PostgreSQL query?" Expect: compare representative predicates, ordering, plans and write costs.
- "The index scan counter is zero; can we remove the index?" Expect: check reset epoch, workload cycle, replicas and constraint dependencies before a destructive proposal.

## Near miss

- "Waiters spend their time acquiring pool clients." Expect: use the `postgres-connection-pooling` skill for topology and acquisition evidence.
- "Two transactions can reserve the same time slot." Expect: use the `postgres-concurrency-control` skill for invariants and interleavings.
- "Roll this index change out on a busy table." Expect: use the `postgres-migrations` skill when available for rehearsal and locks.
- "Build a general fixture framework for tests." Expect: use the `integration-test-harness` skill when real-interface behavior needs proof.

## Outcome

- "Summarize this nested plan." Fixture: a root with 5 shared reads and one child with 5 reads, child estimate 1, actual rows 20 and loops 3. Expect: root reads remain 5, the child's estimate factor is 20 and its approximate total row work is 60; no fabricated summed read total appears.
- "Handle unexecuted and spilling nodes." Fixture: a child with loops zero, a disk Sort and a Hash with batches 4 and temp writes. Expect: no estimate ratio for the unexecuted node, distinct spill flags and no division error.
- "Keep plan data private." Fixture: JSON with a secret-shaped marker in a Filter, Relation Name and Query Text; malformed JSON also includes that marker. Expect: neither stdout nor stderr contains it, and malformed input exits 2.
- "Interpret a limited plan." Fixture: the shipped `captured-loops.json`, with a nested Limit reading one row per outer row from a scan estimated at 15. Expect: a possible early stop, not a definitive estimate error; planned/launched worker shortfalls are separate flags.
- "Bound a before/after claim." Fixture: identical workload metadata but an estimated-only baseline and an analyzed candidate. Expect: the script reports missing execution evidence and no measured delta; the agent leaves the improvement unproven.
