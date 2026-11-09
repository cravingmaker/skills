# Admission and recovery

Read this when defining request admission, replay, expiry, or external recovery.

## One-store operation

Authenticate, validate, and derive the trusted scope and fingerprint.
Inside one real transaction, attempt unique admission, perform the domain mutation, and store the replay result.
On a uniqueness conflict, follow the store's actual visibility rules: wait or retry the lookup as necessary, then compare fingerprints and replay or return the documented in-flight result.
Do not assume a conflicting uncommitted row is visible in the same statement or snapshot.
Handle aborted first transactions so a second caller can become the legitimate first executor.

Returning a committed response before its transaction actually commits would violate this protocol.
Losing the response after commit must leave a completed row that can replay the original result.
A rollback-per-test wrapper hides both of these boundaries.
Use independent committed connections for the proof.

## Multiple phases

For an external effect, a single database transaction cannot commit the remote outcome atomically.
Use durable phases such as admitted, provider_pending, and completed, with a recovery point for the local state each phase committed.
Persist a stable provider request identity before contacting the provider.
Derive that identity from the full local scope within the provider's account/operation namespace; forwarding the literal client key can collide across tenants sharing a provider account.
After a timeout or process death, retain uncertainty until that identity can be reconciled.
An HTTP timeout, disconnected caller, or cancellation signal is not proof that the remote effect failed.

If workers can take over, define who owns the current generation and how stale workers are fenced from local state transitions.
Verify whether the provider deduplicates concurrent uses of the same key.
Fencing only the database write does not undo an external call a stale worker already made.
Where arbitrary external effects cannot be made retry-safe, report that limitation and reconcile instead of claiming a guarantee.

## Replay and expiry

Choose whether replay preserves original status, representation bytes, selected safe headers, and error responses.
Do not persist cookies, bearer tokens, connection strings, or unnecessary personal data as replay metadata.
An asynchronous operation can replay a durable operation identifier; its mutable status resource has a separate read contract.
Reauthorize each request before replay and define how a changed permission or deleted resource affects that response.

Specify the normalization used by the fingerprint before hashing.
If the contract demands identical wire bytes, hash those bounded validated bytes; if it promises semantic equivalence, define a deterministic serialization of the relevant domain values.
Test precision, omitted/null fields, field order, and meaningful headers under that chosen policy.

Expiry is a lifecycle transition with preconditions, not an unconditional age-based deletion.
Do not prune provider_pending or uncertain work simply because the original response window ended.
Different principal/operation scopes may reuse the same literal key; retries after the window need business-level uniqueness or an explicit weaker guarantee.

## Provider and protocol checks

At use time, inspect the selected provider's version-specific idempotency documentation and sandbox behavior.
Do not import a provider's key lifetime, status codes, or stored-error behavior into the local API without choosing that policy.
For header syntax and default error mappings, check the [IETF Idempotency-Key document record](https://datatracker.ietf.org/doc/draft-ietf-httpapi-idempotency-key-header/) and the actual revision it identifies.
Its document status, revision, and expiry are volatile; this skill makes no claim that a remembered draft is current.

The recovery method paraphrases [Brandur's PostgreSQL idempotency discussion](https://brandur.org/idempotency-keys), [Stripe's idempotency reference](https://docs.stripe.com/api/idempotent_requests), and [AWS's retry-safe API discussion](https://aws.amazon.com/builders-library/making-retries-safe-with-idempotent-APIs/).
No text, schema, or code from those sources is copied.
