---
name: rust-async-services
description: Build or repair a Tokio/Axum service's state, tasks, cancellation, middleware, and shutdown. Use for async stalls, lost work, lock contention, blocking-pool growth, or connection leaks. Crate architecture checks and Rust toolchain upgrades are separate capabilities.
license: MIT
compatibility: Python 3.12 or later for the read-only lint-table checker; Cargo supplies workspace metadata.
---

# Rust async services

Make ownership, cancellation, and shutdown behavior explicit, then test the supported build and runtime paths.

## Select the actual build

Read the workspace, lockfile, toolchain file, supported features, MSRV policy, service entry, and deployment build. Verify relevant APIs and support against the installed Tokio, Axum, Tower, serde, and database client documentation. Do not substitute an unreleased API or remember a compiler setting from another toolchain.

Run `cargo fmt --check`, type/build checks, and Clippy over supported feature combinations and targets. Use cargo-hack when installed to enumerate the repository's supported combinations; mutually exclusive features make blind `--all-features` checks misleading. Choose the warnings-as-errors mechanism the installed toolchain supports. Compare [assets/workspace-lints.toml](assets/workspace-lints.toml) with workspace and member lint inheritance. Require request-dependent code to handle errors instead of using `unwrap` or `expect`. Keep justified test-only or library exceptions local and visible.

For a workspace, capture `cargo metadata --no-deps --locked --offline --format-version 1` in the evidence directory, then run `python3 <skill-dir>/scripts/check-workspace-lints.py --root . --metadata <evidence-dir>/cargo-metadata.json`. For a single crate, omit `--metadata`. This read-only checker detects missing member inheritance and missing or allowed required lints; Cargo supplies membership, including implicit path dependencies. It prints findings on stdout, diagnostics on stderr; exits are 0 pass, 1 findings, 2 invalid input. Active warnings still require the CI warnings gate.

Run the repository's cargo-deny policy for advisories, licenses, sources, and bans. Where sqlx is used, check query metadata with its supported prepare/check workflow and the project's disposable dependency harness. An offline metadata check is not evidence that a query works with the deployed schema. Read the `integration-test-harness` skill when installed for actual dependency tests.

For crate dependency or visibility rules, read the `architecture-fitness-functions` skill when installed. For compiler, crate, or tooling upgrades, read the `toolchain-upgrade` skill when installed.

## Choose state ownership

Share configuration, pools, and cheap dependency handles through explicit application state such as `Arc<AppState>`. Keep an already concurrent pool out of a global mutex. Use a synchronous mutex for a short in-memory critical section whose guard ends before `.await`. Use a task that owns an I/O resource and a bounded channel when operations need serialization. Use an async mutex only when holding exclusive ownership across suspension is required and its contention behavior is understood. Do not hold a standard lock guard across `.await`.

Bound channels, task admission, and blocking work. Acquire an admission permit before creating work, and retain it for the real operation's lifetime. For `spawn_blocking`, put the permit inside the blocking closure so cancellation of the awaiting task cannot release capacity while work still runs. Do not assume aborting its handle stops an already running closure. Limit blocking-pool work and keep its completion or abandonment policy observable.

Supervise spawned async work with `JoinSet` or the project's equivalent. Observe task failures and panics, release permits on every path, and stop or drain children according to the lifecycle. An in-process spawn does not make an external effect or background job durable. Read the `async-messaging` skill when installed for work that must survive process loss.

## Design cancellation and error boundaries

Read [references/cancel-safety.md](references/cancel-safety.md) when a `select!`, timeout, disconnect, or shutdown can drop a future. Identify what progress is lost, what remote effect may still complete, and who owns recovery. Test the actual server and middleware's disconnect behavior instead of assuming every handler drops at the same point. Use transactions, idempotency, or reconciliation for multi-step effects.

Decode untrusted HTTP, queue, configuration, and stored JSON with serde or the existing schema layer. Validate domain ranges and relationships after deserialization. Choose unknown-field and enum-evolution behavior by contract; preserve additions where forwarding or archival fidelity needs them. Parsing is separate from authorization.

Model expected domain failures with typed errors. Preserve internal causes and map public status, safe problem details, and correlation once through `IntoResponse` or the chosen boundary. Map extractor rejections too. Convert fallible Tower service errors into the promised response; a handler error type does not automatically cover middleware failures. Test layer order with an unauthorized request, a timeout, and a saturated service. Assert response headers, status/body, and trace context together. Read [references/service-tests.md](references/service-tests.md) when building those runtime cases.

## Drain the owned work

On termination, stop admission and claims, signal supervised tasks, drain accepted work within a deadline, then close pools. Define what happens when the deadline expires, including blocking closures that cannot be aborted. Read the `service-resilience` skill when installed for dependency deadlines and overload policy. Run a real process test that sends SIGTERM during work, observes postconditions from another connection, and checks bounded exit and restart recovery. Use owned disposable dependencies and synthetic inputs; destructive data operations need explicit user confirmation.

Done when supported feature builds and lints pass and runtime tests cover middleware order, dropped or cancelled work, bounded blocking work, and shutdown. Use Loom only when custom concurrent or lock-free code justifies its state-space test. Report exact feature/target commands, dependency versions, observed postconditions, and unavailable runtime proof.
