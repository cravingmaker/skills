# Examples

Run these cases with and without the final skill in restored identical fixtures when model evaluation is authorized.
This draft has no paired model runs.

## Activation

- "Add an HTTP endpoint for cancelling an order and define its errors before writing the handler." Expect an operation contract tied to the authoritative schema, domain transition, method, status, and problem types.
- "Design cursor pagination and sortable filters for our orders endpoint." Expect a total order, cursor binding, bounded page size, filter allowlists, and page-boundary fixtures.
- "Document and enforce ETag and If-Match on profile updates." Expect an atomic version check and a wire test proving failed preconditions leave state unchanged.

## Near miss

- "Will this changed response break our deployed mobile client?" Expect the `api-compatibility` skill to own deployed-client evidence.
- "Make charge retries safe after a timeout." Expect the `idempotent-requests` skill to own durable admission, replay, and recovery.
- "A user can fetch another tenant's order by ID." Expect the `api-authorization` skill to own enforcement and denial tests.
- "Design the GraphQL schema for our product catalog." Expect the chosen-protocol schema design job without an HTTP operation redesign.
- "Design these protobuf service definitions." Expect the chosen-protocol service design job without an HTTP operation redesign.
- "Publish prose reference pages for these unchanged endpoints." Expect documentation work without an API redesign.

## Outcome

- "Check these error examples." Fixture: a JSON array with a POST error having http_status 409, content_type application/problem+json, and body.status 400. Expect the helper to exit 1 and report status-mismatch without echoing the body; correcting body.status to 409 passes.
- "Check a valid bodyless error and an omitted optional problem status." Fixture: the two cases in assets/problem-responses.json, then remove status from the POST body. Expect both inputs to pass; --require-status rejects the second input, and a non-null HEAD body is rejected.
- "Prove the orders list contract." Fixture: six synthetic orders, four sharing a timestamp, a page size of two, and a created_at/id sort. Expect exact static-set traversal without duplicates or omissions, plus a cross-tenant cursor rejection and documented behavior under concurrent inserts.
- "Fix an API that returns 200 with an error object." Fixture: a missing-order handler returns 200 and an error property. Expect a documented failure mapping and a wire assertion for status, media type, and problem type; changing only the JSON shape cannot pass.
- "Reject exposed internal diagnostics." Fixture: a POST error example with status 500 and detail containing SQLSTATE plus a synthetic secret marker. Expect internal-diagnostic, exit 1, and no marker in output; replacing detail with safe guidance passes.
- "Validate the new operation's schema." Fixture: an existing OpenAPI source and its locked generator, with a changed operation containing the dialect feature used by the real caller. Expect schema/example validation, generated caller compilation, and separate wire evidence; a helper-only pass cannot satisfy the outcome.
