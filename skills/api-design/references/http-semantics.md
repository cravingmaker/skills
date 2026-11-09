# HTTP semantics

Read this when selecting a method, status, problem shape, cache rule, or update precondition.

## Method and response rules

Use HTTP's meanings rather than giving a familiar verb a new effect.
Safe methods request read-only behavior; PUT and DELETE have idempotent intended effects, while POST and PATCH need operation-specific reasoning about retries.
Idempotence does not promise identical response bytes or statuses.
Keep mutations out of GET, including tracking actions that change user-visible business state.

| Condition | Candidate response and required decision |
| --- | --- |
| Malformed request | 400; identify a safe, actionable correction. |
| Missing or invalid authentication | 401; emit the applicable authentication challenge. |
| Authenticated caller lacks permission | 403, or the established 404 concealment policy; avoid object-existence leaks. |
| Resource absent | 404; preserve the distinction from a missing route where callers need it. |
| Request conflicts with current resource state | 409; describe how the caller can resolve it. |
| A supplied precondition fails | 412; prove that the mutation did not occur. |
| Unsupported request media type | 415; document accepted formats. |
| Syntactically valid content violates domain input rules | 422 where the API uses this distinction. |
| A required update precondition is missing | Choose and document the API's required-precondition response, commonly 428. |
| Principal exceeds a request limit | 429; define the retry instruction and the scope of the limit. |
| Temporary service unavailability | 503 when appropriate; align any retry advice with the operation's retry contract. |

This table is a design starting point; retain deliberate existing mappings and explain any change.
Redirects are protocol behavior, not application errors that automatically need a problem body.
HEAD responses carry no content, and neither do statuses whose HTTP semantics prohibit it.

## Problems

Use stable problem type identifiers for machine decisions and stable titles except for localization.
Problem details do not require every standard member; an omitted type has the standard default, and status is optional.
When the origin emits status in the body, it must match the HTTP status it sends.
Choose which members this API requires and validate that stronger local policy separately.
Use extension fields for machine-readable validation locations rather than asking callers to parse detail strings.
Retain unknown-member tolerance in consumers.

Test that a schema error, domain conflict, and unexpected exception all reach the intended status and serialization path.
Test redaction with synthetic secret-shaped and personal-data-shaped values; compare the external error and internal diagnostic policy separately.

## Preconditions and caching

If-Match uses strong comparison; weak validators do not prevent lost updates through that precondition.
Back the comparison with an atomic conditional update or equivalent concurrency control, and assert that one of two stale concurrent writers loses.
Decide whether a missing If-Match is allowed or rejected.
An ETag's representation variant and any content encoding must agree with the validator strategy.

Choose Cache-Control and Vary from the representation's authorization and content-negotiation behavior.
Verify a 304 path without a response body and an authorized cache miss after relevant state changes.
Do not infer that all authenticated responses are safe for a shared cache.

## Sources

These are paraphrased design rules; no source text or code is incorporated.
Check [HTTP semantics](https://www.rfc-editor.org/rfc/rfc9110.html), [HTTP caching](https://www.rfc-editor.org/rfc/rfc9111.html), [problem details](https://www.rfc-editor.org/rfc/rfc9457.html), and [additional statuses](https://www.rfc-editor.org/rfc/rfc6585.html) for the precise protocol requirements.
