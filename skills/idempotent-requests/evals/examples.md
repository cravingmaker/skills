# Examples

Run these cases with and without the final skill in restored identical fixtures when model evaluation is authorized.
This draft has no paired model runs.

## Activation

- "Clients time out after creating a charge and retry it. Make that safe." Expect scoped atomic admission, replay, provider reconciliation, and failure-schedule evidence.
- "Implement Idempotency-Key for this unsafe operation." Expect fingerprint, in-flight and mismatch behavior, retention, and durable result semantics before handler changes.
- "Our server commits the order and dies before returning. Recover the original result on retry." Expect the local effect and replay result to share a commit and a post-commit lost-response test.

## Near miss

- "Deduplicate deliveries in this queue consumer." Expect the `async-messaging` skill.
- "Choose between PUT and PATCH for profile replacement." Expect the `api-design` skill.
- "Prove users cannot replay another tenant's stored response." Expect the `api-authorization` skill to own the access-policy proof.
- "Prevent two different reservation requests from booking the last seat." Expect the `postgres-concurrency-control` skill for the business invariant across distinct request keys.

## Outcome

- "Prove simultaneous retries create one order." Fixture: a disposable PostgreSQL database, two independent application connections, a barrier at unique admission, and an independently queried orders ledger. Expect one committed order and the documented second-request outcome; removing unique admission makes the test fail.
- "Recover after a lost response." Fixture: kill the owned worker at a hook after the local effect/result commit and before response delivery, then restart and retry. Expect the original resource identity and one durable effect; a separately committed effect/result variant is detected as broken.
- "Handle provider success with an unknown local outcome." Fixture: an owned durable fake-provider ledger commits a charge, drops the acknowledgement, and exposes lookup by the stable provider identity. Expect reconciliation to find one charge, with no newly generated provider key; unavailable lookup preserves uncertainty.
- "Resume a payment after the mobile client restarts." Fixture: an unresolved intent and key in a file-backed client store, plus a provider effect whose acknowledgement was lost. Expect the restarted caller to reuse the stored key and the independent ledger to retain one effect.
- "Define key expiry and scope." Fixture: two tenants, two same-tenant principals, two operations, a controllable clock, and one expired provider_pending record. Expect separate authorized scopes, the chosen expiry response, no pruning of unresolved work, and an explicit bound on the safety claim.
