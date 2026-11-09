# Delivery tests

Read this when turning an event contract into executable failure schedules. Build each case with the application's real transaction and transport adapters on disposable dependencies. The `integration-test-harness` skill, when installed, owns dependency setup and cleanup.

| Case | Controlled schedule | Independent result |
| --- | --- | --- |
| Atomic enqueue | Stop before the business transaction commits, then repeat after commit | A separate connection sees neither business change nor job before commit, and both after it |
| Relay lost acknowledgement | Destination accepts, relay crashes before its receipt commit | Restart republishes the same event ID; one consumer effect survives |
| Consumer rollback | Inbox insert succeeds, stop before effect transaction commits | Neither inbox nor effect survives; redelivery performs the effect |
| Consumer lost acknowledgement | Effect commits, process stops before transport acknowledgement | Redelivery finds the matching inbox fingerprint and leaves the effect count unchanged |
| Identity collision | Deliver one identity with a changed payload fingerprint | The consumer rejects or quarantines it; it cannot report an ordinary duplicate |
| Concurrent duplicates | Two consumers cross an admission barrier for the same scoped identity | The unique inbox constraint admits one effect, verified outside both transactions |
| Reordering | Deliver sequence two before sequence one for the same key | The documented gap policy holds; unrelated keys can progress |
| Lease expiry | Pause worker A, expire its lease, let B claim a newer generation, then resume A | A cannot renew or commit local state; B can complete |
| Final attempt crash | Crash after the last allowed claim and let its lease expire | The sweep records one dead letter; no new attempt is admitted |
| Poison message | Deliver an unsupported schema beside a valid unrelated event | The poison event reaches quarantine while the valid event completes |
| Replay horizon | Replay once within and once beyond retained inbox state | The stated guarantee matches both observations; replay beyond the horizon cannot claim deduplication |

For external writes, add a provider fixture that accepts the operation but drops its response. Assert provider-key reuse and reconciliation through an independent read. Local fencing and an inbox alone cannot prove external uniqueness.

Use a fake clock for scheduling logic; use actual committed transactions for claims about constraints or isolation. Keep the job deadline, cancellation margin, and lease duration in a shared configuration test. Have the test reject an execution deadline that reaches or exceeds the usable lease.

The repository fixture `tests/async-messaging/run.sh` checks the contract and, when `initdb` and `postgres` are installed, runs the actual starter fragments in a fresh single-user PostgreSQL cluster. This needs no network or pre-existing database. It checks sequential fencing and real commit/rollback; the application's multi-connection and transport schedules above remain required.

Sources: [AWS transactional outbox](https://docs.aws.amazon.com/prescriptive-guidance/latest/cloud-design-patterns/transactional-outbox.html), [PostgreSQL row locking](https://www.postgresql.org/docs/current/sql-select.html), and [RabbitMQ acknowledgements](https://www.rabbitmq.com/docs/confirms). Verify the selected transport's current acknowledgement, lease, retention, and retry behavior before implementing its adapter.
