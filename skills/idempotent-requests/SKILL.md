---
name: idempotent-requests
description: "Make a retried unsafe request produce one scoped durable effect: key admission, fingerprint, in-flight behavior, replay, expiry, and provider reconciliation. Use for double charges, safe retries, lost responses, or Idempotency-Key. Queue-consumer deduplication is a separate job."
---

# Idempotent requests

Deliver an admission and recovery protocol whose guarantees survive concurrent requests, process crashes, and uncertain external outcomes.

## Define the retry contract

1. Identify the operation's irreversible effects, authoritative store, transaction boundaries, external providers, and caller retry behavior. State the invariant that must hold, including any business uniqueness rule that persists beyond key retention.
2. Define the key scope from trusted tenant/principal identity plus semantic operation plus key. Treat aliases of the same operation deliberately. A key is neither a credential nor a globally readable result-cache address.
3. Give callers one key per intent, reused across retries and persisted across restarts while the outcome is unresolved. A new key represents a new intent or an explicitly chosen terminal-failure retry under the API's policy; a timeout alone never justifies it.
4. Define the request fingerprint, validation and execution boundary, in-flight behavior, replay result, retention, expired-key behavior, and recovery ownership.
5. Choose fingerprint input from the validated operation data and relevant request semantics. Specify normalization, absent/null handling, precision, and versioning; use a maintained serializer or hash library rather than inventing JSON canonicalization.
6. Read the API's existing policy and the provider's actual contract. Verify the current Idempotency-Key document and its status at the IETF before choosing header syntax and error mappings. Keep provider and local policies distinct.

Use [assets/request-contract.md](assets/request-contract.md) when the repository lacks this contract.
Read [references/admission-recovery.md](references/admission-recovery.md) when choosing transaction boundaries, replay behavior, expiry, or provider reconciliation.

Done when each possible retry has an explicit admission, wait/conflict, replay, rejection, or reconciliation outcome.

## Make admission durable

- Use a unique store constraint over the whole scope. Admit by an atomic insert or equivalent conditional operation, not a read-then-insert check or a process-local lock.
- When all effects are in one database, commit the domain mutation and stored completion/result in the same transaction. A crash before commit must leave neither effect nor successful replay record.
- On duplicate admission, compare the stored fingerprint before returning any result. A changed request with the same scoped key must not mutate state or replace the original record.
- Authenticate and authorize every attempt before exposing a replay. Handle revoked permissions and sensitive fields under the operation's access policy.
- Define what happens while the first attempt is in flight: a bounded wait, a documented conflict response, or a status resource. Do not wait beyond the caller's deadline or pretend a timed-out waiter cancelled the durable effect.
- Store the agreed replay status, safe headers, and body or durable result reference. Reuse the original domain identity; do not execute the handler again to reconstruct its side effect.
- Decide which validation failures or execution failures become durable results. Caching every error, including transient server errors, is a policy choice that varies by API and provider.

Compare [assets/idempotency.sql](assets/idempotency.sql) with the actual schema before adapting it.
It is an original PostgreSQL table starter, not an executor, migration, cleanup job, or complete external-effect protocol.
It makes the tenant, principal, and operation part of the key and keeps nonfinal state distinct from stored completion.
Check syntax, constraints, and concurrency against the installed server on an explicitly disposable target before using it.

Done when the real store serializes admission and ties the domain effect to the relevant durable recovery state.

## Recover external effects and expired keys

Persist the provider intent and stable provider key before the call.
After an uncertain acknowledgement, reconcile against that same provider identity; do not create a fresh key and repeat the effect.
Where the provider supports idempotency, verify its account and operation scope, fingerprint rules, failure behavior, retention, and lookup capabilities live.
If it offers neither deduplication nor reliable lookup, state the remaining duplicate risk and choose a manual or business-level reconciliation path.

For multiple durable phases, commit each recovery transition with its local state.
Use exclusive recovery ownership and fencing or another proven protocol for competing workers; a lease timeout alone cannot stop an old worker from causing an external effect.
Do not retry arbitrary external calls inside a database transaction retry.

Set retention from the actual caller/provider retry horizon and data-retention requirements.
Keep pending or uncertain provider work out of blind expiry cleanup.
Define whether an expired key is rejected or reusable and how business uniqueness survives that choice.
Destructive cleanup on existing data needs explicit user confirmation.

Done when every crash boundary has an accountable recovery path and expiry cannot silently re-admit an unresolved effect.

## Prove the protocol

Read [references/failure-schedules.md](references/failure-schedules.md) before claiming retry safety.
Use real PostgreSQL for PostgreSQL admission/transaction claims and at least two independent connections with barriers, not sleeps.
Control crash points and time through explicit hooks or a test clock.
Use an owned fake provider with a durable effect ledger and lost-acknowledgement control; never send real charges or notifications for these tests.

Prove simultaneous duplicates, changed payload, cross-tenant/principal/operation reuse, crashes before and after commit, in-flight recovery, expiry, and provider success with lost acknowledgement.
Assert durable row/effect counts and original result identity independently of the implementation's own response.
Keep keys, credentials, request payloads, and personal data out of test output.
When a real dependency harness is missing, read the `integration-test-harness` skill if installed.

Done when each applicable failure schedule passes and disabling admission or separating effect/result commits makes the corresponding test fail.

## Adjacent work and completion

For queue-consumer deduplication or an outbox, read the `async-messaging` skill if installed.
For HTTP method and error semantics, read the `api-design` skill if installed.

Return the scope and retention of the guarantee, contract/schema paths, admission/replay/recovery decisions, and the exact real-store test results.
State unavailable provider or crash-path proof.
Use a bounded claim such as one committed domain effect per scoped key during the documented retention window; an unqualified exactly-once claim is unsupported.
