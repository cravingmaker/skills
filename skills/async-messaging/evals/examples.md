# Examples

Run matched final-skill and no-skill cases in the repository's evaluation harness when authorized. These cases are drafted; no paired model runs have been recorded.

## Activation

- "Publish an event after this order commits without losing it on a crash." Expect: one business/outbox transaction and a stable relay identity with crash-boundary tests.
- "Our consumer applies the same payment event twice after a restart." Expect: scoped inbox admission and the local effect share one committed transaction; acknowledgement follows commit.
- "Notify IndexNow when public pages are added, updated, or deleted." Expect: the URL notification reference is read and a durable change-to-receipt adapter uses the existing queue.
- "Workers both complete the same job after a lease expires." Expect: a live lease and current generation gate the effect transaction; handler time plus cancellation margin stays below the lease.

## Near miss

- "Make retried HTTP checkout requests replay the same response." Expect: the `idempotent-requests` skill owns request admission; this skill is unnecessary unless processing crosses a queue.
- "Capture database changes into an analytical warehouse with watermarks." Expect: a CDC/stream-processing data job; service outbox advice does not replace its event-time contract.
- "Install and upgrade our RabbitMQ cluster." Expect: broker operations; no application inbox or queue is redesigned.
- "Two requests book the same seat at once." Expect: the `postgres-concurrency-control` skill owns the in-database anomaly; no queue is introduced.
- "Add a timeout and retries to the tax API call." Expect: the `service-resilience` skill owns the synchronous dependency budget.

## Outcome

- "Check the consumer contract before implementation." Fixture: `assets/messaging-contract.json`, then raise the handler timeout into its cancellation margin or set the total queue-delay bound above retention. Expect: the original passes and each mutation fails `scripts/check-messaging-contract.py` without writing the input or echoing source strings.

- "Prove duplicate and stale-lease handling." Fixture: disposable PostgreSQL, two real connections, one counter row, one outbox event, and barriers after claim and inbox insert. Expect: concurrent duplicates commit one effect; after B acquires a newer generation A cannot complete locally; the separate observer sees the final counter.
- "Prove crash recovery at the messaging boundaries." Fixture: the same real-store harness with failpoints before/after business commit, after destination acceptance, after effect commit, and after final claim. Expect: the cases in `references/delivery-tests.md` pass, including an expired final attempt becoming a retained dead letter.
- "Prove URL changes and submission receipts are faithful." Fixture: `assets/url-notification-cases.json`, a transactional fake-site inventory, a disposable outbox, and a fake receiver that can accept then lose its reply. Expect: real revisions notify, unchanged saves do not, retries preserve identity, permanent rejection stays inspectable, and accepted receipt leaves indexing unknown.
