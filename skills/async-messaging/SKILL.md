---
name: async-messaging
description: Make event publication and background jobs survive duplicates and crashes. Use for an outbox, a consumer that processes twice, queue leases, poison messages, or durable URL change notifications. Covers service delivery semantics; broker operations and analytical streams belong elsewhere.
license: MIT
compatibility: Python 3.12 or later for the read-only contract checker.
---

# Async messaging

Deliver a durable publication and processing contract, with tests at each commit and acknowledgement boundary. Start with a PostgreSQL queue when the business write and enqueue can share a transaction. Choose a broker when measured throughput, fan-out, retention, or independent consumers require one.

## Define the boundaries

Write the event identity, tenant scope, schema version, ordering key, authoritative writer, and local effect. Separate acceptance, publication, processing, and acknowledgement; name the durable record at each point. State the deduplication and replay retention windows. An at-least-once transport can repeat messages after a successful effect. Claim an effect happens once only within the stated identity, transaction, and retention boundary.

For request-key admission and response replay, read the `idempotent-requests` skill when installed. Analytical CDC and event-time stream processing are separate data jobs; broker deployment is an operations job. Read [references/delivery-tests.md](references/delivery-tests.md) when defining recovery schedules and their independent oracles.

Compare [assets/messaging-contract.json](assets/messaging-contract.json) with each consumer or job and run `python3 <skill-dir>/scripts/check-messaging-contract.py contract.json`. The read-only helper checks timeout plus cancellation margin against the lease, finite retries with full jitter, and the retry envelope plus total queue-delay bound against retention. It prints findings by consumer index on stdout; diagnostics use stderr. Exits: 0 pass, 1 findings, 2 invalid input. A passing contract checks configuration, not delivery behavior.

A new broker or datastore is a hard-to-reverse choice. Use the `architecture-decisions` skill when installed to compare the options, keep any ADR proposed, and obtain user sign-off before adopting it.

## Make the transaction carry the guarantee

1. Commit the business change and queued job or outbox row together.
2. Publish a stable event ID and payload version; record a relay receipt only after the destination acknowledges.
3. In each consumer, insert its inbox key and apply the local effect on the same transaction handle.
4. Acknowledge after that transaction commits; on a duplicate, verify the stored fingerprint agrees before treating the effect as complete.

A duplicate that finds an inbox conflict must skip the effect. A reused identity with a different payload is a contract violation. Keep external effects outside the local guarantee: use the provider's deduplication key and reconcile an uncertain acknowledgement. Detached work in an application process is not a durable queue.

Compare [assets/outbox-inbox.sql](assets/outbox-inbox.sql) with the application's schema and transaction code. It contains separate SQL fragments, not a migration to apply unchanged. Adapt keys, payload retention, and supported PostgreSQL syntax to the repository. Read the `integration-test-harness` skill when installed to exercise actual commits, concurrent connections, and restart boundaries.

## Bound work and preserve ownership

Claim a bounded batch through `FOR UPDATE SKIP LOCKED`; commit the claim before slow network work. An expiring lease allows recovery but does not stop a paused worker. Increment a fencing generation on every claim and require the current generation and live lease for local completion or renewal. Check external destinations for their own fencing or idempotency support. Without that support, a stale worker can still produce an external effect; document the reconciliation path.

Set an execution deadline shorter than the lease or visibility timeout, including cancellation and commit margin. Bound prefetch, active workers, payload size, attempts, elapsed retry time, and queued age. Count attempts at durable claim time so a crash consumes an attempt. Define how an expired final attempt becomes a retained dead letter instead of remaining stuck. Read the `service-resilience` skill when installed for dependency deadlines and retry budgets.

Ordering is per named key. `SKIP LOCKED` does not preserve aggregate order: enforce sequence checks, serialize a key, or use commutative effects. On a missing predecessor, retain a bounded wait or reconciliation state; never silently discard the gap. Quarantine unsupported schemas and permanent failures without blocking unrelated keys.

## Recover deliberately

Retain dead-letter reason, stable event identity, attempt history, and a safe payload reference. Alert on exhausted work and oldest pending age. Replay needs an authorized scope, compatible decoder, deduplication window, and a recorded operator action. Destructive retention or mass replay against live data needs explicit user confirmation. Use synthetic or minimized payloads for fixtures and omit credentials from receipts and reports.

For URL add, update, or delete notifications, read [references/url-change-notifications.md](references/url-change-notifications.md). That adapter uses this outbox and retry contract; an HTTP receipt never proves indexing. Use [assets/url-notification-cases.json](assets/url-notification-cases.json) when building that adapter's fixtures.

## Prove delivery behavior

Run duplicate, reordered, stale-lease, poison-message, and crash-boundary cases against the actual store and selected transport. Use barriers or injected failpoints rather than sleeps to choose the failure order. Observe the business state through a separate connection and compare durable event, inbox, receipt, and effect identities. Run the named URL adapter cases when that reference applies. Keep SQL inspection and in-memory simulations separate from evidence about real database atomicity.

Done when each durable boundary has a recovery test, duplicate delivery preserves the effect invariant, a stale generation cannot commit locally, and exhaustion produces an inspectable terminal state. Report the tested transport/store versions, exact test commands, deduplication window, external uncertainty, and any unrun recovery cases.
