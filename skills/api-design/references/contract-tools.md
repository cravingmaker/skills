# Contract tools and protocol choice

Read this when selecting a protocol or checking an OpenAPI dialect and its tools.

## Choose from the caller's needs

| Candidate | Evidence to collect before choosing |
| --- | --- |
| HTTP with JSON | Browser and partner access, cache behavior, resource lifecycle, existing client and gateway support. |
| GraphQL | Several callers need flexible graph reads, and the team can enforce field authorization, query-cost bounds, and batching. |
| gRPC or a compatible RPC transport | Generated client needs, streaming and deadline behavior, browser access, and proxy/load-balancer support. |

A protocol decision does not implement its schema or solve its authorization and failure behavior.
For a hard-to-reverse protocol choice, obtain the user's sign-off; any draft decision record remains proposed.
For an unfamiliar HTTP method, verify the method's current IETF status and actual support in every required client, router, proxy, and schema tool.
Use a supported ordinary HTTP operation when those checks fail; do not depend on an unreleased framework feature.

## Prove dialect support

1. Inspect the repository's lockfile, framework generator, validation command, and generated client version.
2. Read the chosen dialect at the [OpenAPI specification index](https://spec.openapis.org/oas/) and the installed tools' official support documentation.
3. Use a minimal operation containing the actual nullable, composition, example, security, or streaming feature at issue.
4. Run validation, generation, and compilation through that fixture. Compare the generated types and request serialization with the intended contract.

Use the existing Spectral or Redocly configuration where present; inspect its installed version and rule syntax before extending it.
Compare candidate rules with the repository's conventions before applying them.
Generic rules requiring problem bodies on every non-success response would mishandle redirects and HEAD.
An Idempotency-Key rule also needs an operation-level retry policy; unsafe methods do not all need a new header.

## Checks to retain

- The chosen dialect is accepted without unsupported-feature warnings or silent feature loss.
- Operation identifiers are unique, security inheritance is deliberate, and request/response examples validate.
- List defaults, maximum page sizes, and error schemas match the implementation.
- Generated callers compile and use the intended requiredness, numeric representation, and null behavior.
- The wire test drives the actual error handler, serializer, precondition check, and pagination query.

Versions and supported dialects change.
Verify tool behavior from [Spectral's documentation](https://docs.stoplight.io/docs/spectral/), [Redocly CLI documentation](https://redocly.com/docs/cli/), and the generator's own release notes at use time.
Do not install or upgrade a tool merely to apply this skill without task scope for that change.
