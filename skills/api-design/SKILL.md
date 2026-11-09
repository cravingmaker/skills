---
name: api-design
description: "Design an HTTP operation contract before its handler: resources, methods, errors, pagination, filters, limits, and conditional updates. Use when adding or reshaping an endpoint or OpenAPI operation. Deployed-client compatibility, access enforcement, and retry deduplication are separate jobs."
---

# API design

Deliver one operation contract whose examples, generated consumer, and wire behavior agree.

## Establish the contract

1. Find the authoritative OpenAPI document or the schemas that generate it, the installed validator and generator, and a caller of the operation. Keep one editable source; regenerate derived files.
2. Name the caller's operation, the resource identity and lifecycle, and the success condition. Name resources for the caller's domain rather than storage tables; use a domain action when replacement or field editing would misrepresent it. A queued operation needs a durable status resource and a distinction between acceptance and completion.
3. Choose the smallest protocol the callers and intermediaries support. Keep an established protocol unless the task calls for changing it. For a new choice, compare HTTP/JSON, GraphQL, and gRPC against client access, caching, streaming, and operational cost.
4. Verify the chosen OpenAPI dialect against the official specification and the installed validator, framework, and generator. Exercise a feature the operation actually uses through that tool chain; accepting a document alone proves little about generated clients.

Start from [assets/operation-contract.md](assets/operation-contract.md) when the repository has no operation review format; compare it with existing conventions before copying.
Read [references/contract-tools.md](references/contract-tools.md) when choosing a protocol, OpenAPI dialect, or contract check.

Done when the source, callers, supported dialect, and operation's success condition are explicit.

## Define observable behavior

- Choose methods by their intended effects. Separate safe methods, idempotent effects, and request deduplication. A successful retry can return a different status while preserving the intended effect.
- Define request and response schemas at the boundary, including absent versus null values, numeric precision, timestamps, unknown fields, and field allowlists. Parse untrusted values before constructing domain values.
- Map each domain failure to an HTTP status and stable problem type. Use the API's chosen problem-details format for application errors, document exceptions, and keep secrets, SQL, stack traces, and personal records out of public details.
- Describe success, validation, conflict, forbidden access, and dependency failure examples as status, headers, and body together. Respect responses that cannot carry content, including HEAD responses and bodyless success statuses.
- For a mutable representation, decide whether callers need a strong ETag and If-Match. Enforce the version comparison and mutation atomically; test that a failed precondition leaves state unchanged.
- Bound request bytes, list and batch sizes, filter complexity, and response work using the service's actual requirements. Document enforced defaults and maxima in the contract.
- For lists, choose ordering and pagination before clients depend on a complete collection. Allowlist filter fields, operators, and sort keys; parameterize values.
- Set cache rules, validators, and variation for authenticated and tenant-specific representations. A cursor or cache key does not replace authorization.

Read [references/http-semantics.md](references/http-semantics.md) when choosing methods, status mappings, problem fields, caching, or preconditions.
Read [references/pagination-filtering.md](references/pagination-filtering.md) when the operation returns a collection.

Done when each observable branch has a documented example and every limit or concurrency promise has an enforcement point.

## Check the contract

1. Run the repository's OpenAPI dialect validator and style rules. Check unique operation identifiers, effective security declarations including intentional public access, request and response examples, list bounds, and error mappings. Validate examples against their schemas.
2. Regenerate the client or types and compile a real caller using the changed operation. Check the generated artifact for unsupported or dropped dialect features.
3. Run wire tests through the real serialization and error handling boundary. Assert the wire status, media type, problem type, relevant headers, and body together; include a failing precondition and a list boundary where applicable.
4. For a small supplemental check on sanitized error captures, run:

   ```sh
   python3 <api-design skill>/scripts/check-problem-responses.py error-examples.json
   ```

   The read-only helper needs Python 3.12+ and emits JSON findings; exits are 0 pass, 1 findings, and 2 usage or unreadable input. It checks a problem+json policy on origin error responses, permits an omitted problem status, requires HEAD to have no content, and rejects common stack-trace/SQL signatures in title or detail. Signature checks do not prove complete redaction; retain the synthetic-marker wire tests. Use `--require-status` only if the API contract requires that optional member.

   [assets/problem-responses.json](assets/problem-responses.json) shows the input shape with synthetic values. The helper neither validates an OpenAPI dialect nor runs a server; captured examples need provenance from the actual test.

Done when the validator, compiled caller, and wire assertions pass, or the exact unavailable proof is reported.

## Adjacent work

When independently deployed consumers exist, read the `api-compatibility` skill if installed before claiming the change is compatible.
When enforcing object, property, function, or tenant access, read the `api-authorization` skill if installed.
When an unsafe operation must tolerate retries, read the `idempotent-requests` skill if installed.
GraphQL schema design, protobuf service design, and API reference publishing are separate jobs; hand over the agreed operation model and examples.

## Done

Return the authoritative contract path, method and resource choices, error mapping, pagination and limit behavior, and precondition policy.
Include exact validation commands and results for the dialect, examples, generated caller, and wire tests.
Label missing runtime or consumer evidence explicitly; a clean schema does not establish those claims.
