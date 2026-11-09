# Examples

Run matched final-skill and no-skill cases when authorized. Helper fixtures are deterministic checks; they do not constitute paired behavioral evaluation.

## Activation

- "Add this outbound dependency without letting slow responses exhaust our service." Expect: one remaining deadline, actual client cancellation, and finite concurrency and response-size limits.
- "Our retries at the proxy, service, and SDK cause a traffic storm." Expect: attempts are multiplied, retry ownership is reduced to one layer, and fault tests observe downstream attempts.
- "SIGTERM loses accepted jobs and leaves sockets open." Expect: admission stops, accepted work drains within a deadline, and restart postconditions verify recovery.

## Near miss

- "Choose availability SLOs and paging thresholds." Expect: an operations policy job; this skill does not invent an error budget.
- "Configure Kubernetes autoscaling and probes." Expect: platform configuration owns that work; application liveness semantics can be supplied without taking over the deployment.
- "Fix an ESM import failure in emitted Node code." Expect: the `typescript-node-services` skill owns the artifact/runtime issue.
- "A Tokio blocking closure outlives its request permit." Expect: the `rust-async-services` skill owns the lifetime fix, with this method only if dependency budgets also change.
- "Make POST /payments safe for client retries." Expect: the `idempotent-requests` skill owns admission and replay.
- "Retry failed background jobs." Expect: the `async-messaging` skill owns durable redelivery.
- "Our PostgreSQL pool runs out of connections." Expect: the `postgres-connection-pooling` skill owns the connection budget.
- "Add tracing to the tax API call." Expect: the `opentelemetry-instrumentation` skill owns emitted telemetry.

## Outcome

- "Check our nested attempt and deadline policy." Fixture: `assets/retry-policy.json`; then change caller attempts to three and dependency attempts to four. Expect: the unchanged policy passes, the mutation reports twelve leaf attempts and multiple retry owners, and repeated checks produce identical JSON without input writes.
- "Allocate sequential dependency budgets." Fixture: a policy with `hops` instead of `layers`, two calls at 100 ms with 10 ms backoff and three calls at 250 ms with 50 ms backoff, plus 100 ms overhead and five total leaf attempts. Expect: 1160 ms passes, 1159 ms fails, and a negative overhead is invalid.
- "Find calls whose bounds need review." Fixture: the bounded and unbounded TS/Rust files under `tests/service-resilience/fixtures/`. Expect: the helper finds the five unsafe candidates, accepts the visibly bounded files, and reports `complete_analysis: false`; comments cannot supply a missing signal.
- "Prove retry and drain behavior." Fixture: a fake-clock client with injectable randomness and token budget, plus a real child service with a barrier-controlled fake dependency. Expect: Retry-After date/delta cases, cancellation, overload and recovery obey bounds; SIGTERM rejects new work and preserves accepted-work postconditions before bounded exit.
