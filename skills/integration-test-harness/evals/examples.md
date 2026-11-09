# Examples

Paired model runs are pending; keep the catalog entry unevaluated.

## Activation

- "Our database integration suite mocks the repositories; prove commits and constraints." Expect: use real PostgreSQL with capability probes, committed writes and independent readback.
- "Test that this native store survives reopening and cleans up after cancellation." Expect: use the actual framework store, a separate reader and an interruption cleanup check.
- "Refactor this untested parser while preserving reviewed current behavior." Expect: use labeled characterization fixtures plus independent semantic cases for known rules.
- "Our Vitest suite passes when the network promise rejects later." Expect: repair awaiting and fixture cleanup, then prove a meaningful failure is observed.

## Near miss

- "Implement a pure arithmetic function test-first." Expect: use the `tdd` skill; no dependency harness is needed.
- "Package the project's repeatable launch and verify driver as a skill." Expect: use the `create-verification-skill` skill; the harness method can be consumed by that driver.
- "Wire existing tests into required CI checks." Expect: use the `project-guardrails` skill; the job is enforcement.
- "Prevent double booking under concurrent writers." Expect: use the `postgres-concurrency-control` skill for invariant and interleaving design; consume this harness method where needed.

## Outcome

- "Reject a false-green result." Fixture: fresh JUnit files containing zero cases, only a skipped expected case, a failed case or a declared count larger than actual cases; expected IDs are an independent nonempty JSON list. Expect: exit 1 for each incomplete or failed run, and no logs or credentials in output.
- "Verify a real commit." Fixture: one PostgreSQL table with a deferred uniqueness constraint, one writer and one independent reader. Expect: committed data survives client close; the invalid duplicate fails at commit, and rolling back a per-test wrapper cannot stand in for this proof.
- "Keep native and request adapters honest." Fixture: a disk-backed native store reopened after a write, plus an MSW-controlled client with an unexpected request and a rejected awaited promise. Expect: real-store persistence evidence, explicit mock scope, meaningful failures, nonempty selected results and cleanup after cancellation.
- "Reject a filtered-file pass." Fixture: the shipped `filtered-node.xml`, with an independent expected behavior ID `test::orders repository commits a reservation`. Expect: exit 1 even though the XML contains a passing file-level case.
- "Check the parser's selection contract." Fixture: `stock::atomic_increment` passes but `stock::write_skew` is missing, with both declared in expected IDs. Expect: exit 1; adding an actually passing unique second case yields exit 0, unchanged on repeat.
