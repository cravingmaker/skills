# Examples

Run matched final-skill and no-skill cases when authorized. No paired model runs or application crate builds are recorded by these draft cases.

## Activation

- "Our Tokio service stalls because a standard mutex guard crosses an await." Expect: state ownership and guard lifetime change, with Clippy and a concurrent runtime case.
- "Bound spawn_blocking work even when the requesting task is cancelled." Expect: admission happens before spawning and the closure retains its permit for its real lifetime.
- "Fix Axum timeout responses and graceful shutdown." Expect: Tower layer ordering and public error mapping are tested through the actual server, followed by a busy-process termination case.

## Near miss

- "Forbid one Rust crate from depending on an infrastructure crate." Expect: the `architecture-fitness-functions` skill owns the dependency rule.
- "Upgrade the Rust compiler and Tokio dependencies." Expect: the `toolchain-upgrade` skill owns toolchain compatibility.
- "Repair a GPUI desktop focus and window-lifecycle bug." Expect: a native frontend job; server task/lifecycle rules do not replace desktop behavior.
- "Add timeout and retries to our billing API call." Expect: the `service-resilience` skill owns the dependency policy.
- "Build a Node TypeScript service for this API." Expect: the `typescript-node-services` skill owns that runtime.

## Outcome

- "Enforce lint inheritance for every workspace member." Fixture: the workspace manifests in `tests/rust-async-services/fixtures` and format-version-one Cargo metadata listing every member, including a path-only member missing its lint table. Expect: the checker reports that member, passes after its opt-in, and refuses missing or wrong-root metadata.

- "Prove supported features and middleware order." Fixture: a Tokio/Axum workspace with two mutually exclusive deployment features, auth/tracing/timeout layers, and a handler blocked at a notification. Expect: each supported combination builds and lints; unauthorized and timed-out calls return the intended status/problem body, headers, and trace context through the real stack.
- "Prove cancellation cannot release blocking capacity early." Fixture: one blocking permit, closure A waiting at a barrier, a cancelled awaiter, and queued closure B. Expect: B cannot start until A releases its permit; cleanup always releases the barrier and task failures remain supervised.
- "Prove a cancelled or terminating service preserves effects." Fixture: a real HTTP service, disposable database, barriers around a multi-step transaction, and an external-effect fake that can lose acknowledgements. Expect: observer connections establish commit/rollback, reconciliation handles uncertain writes, disconnect behavior matches the real stack, and SIGTERM drains or recovers accepted work within the recorded bound.
