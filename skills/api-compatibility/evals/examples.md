# Examples

Run these cases with and without the final skill in restored identical fixtures when model evaluation is authorized.
This draft has no paired model runs.

## Activation

- "Is this new response enum value safe for our released iOS app?" Expect the actual old decoder to be exercised, even if the schema diff calls the edit additive.
- "Deprecate our legacy search endpoint without breaking old desktop clients." Expect a consumer inventory, coexistence plan, lifecycle field tests, and evidence-backed removal gates.
- "Can we tighten this request limit without an API version change?" Expect old-request fixtures and a semantic compatibility verdict tied to the existing promise.

## Near miss

- "Design the error and pagination contract for a brand-new orders endpoint." Expect the `api-design` skill.
- "Prevent another tenant from reading this export." Expect the `api-authorization` skill.
- "Persist a response so a timed-out charge request can be retried safely." Expect the `idempotent-requests` skill.
- "Set up consumer-driven contract tests for all services." Expect the broader test-suite job; this skill only supplies consumer and change evidence.

## Outcome

- "Check lifecycle response fields." Fixture: assets/lifecycle-headers.json, then change Sunset to a date before epoch zero. Expect the helper to pass the original, reject the inverted chronology, and reject an HTTP-date used as Deprecation.
- "Assess this apparently additive enum change." Fixture: an old decoder accepting only pending and complete, a candidate response with cancelled, and a clean schema diff. Expect the unchanged old decoder to fail, a breaking verdict for that supported consumer, and no weakening of the old fixture.
- "Decide whether we can remove the old endpoint." Fixture: a supported offline desktop client, zero measured calls in a short period, and no telemetry while offline. Expect the removal gate to stay open with the missing observation coverage named.
- "Review an unchanged schema with a new sort default." Fixture: a list request without sort, old behavior oldest-first, and candidate behavior newest-first. Expect a semantic break to be detected despite identical schema bytes.
