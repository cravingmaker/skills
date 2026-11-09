---
name: api-compatibility
description: "Check whether an API change breaks deployed consumers and plan its versioning or deprecation. Use for \"is this breaking\", \"retire this endpoint\", or keeping old mobile and desktop clients working. Combine schema diffs, real old-client fixtures, semantic changes, and measured migration."
---

# API compatibility

Decide compatibility against consumers that may still run, then prove the transition and its removal gate.

## Bind the comparison

1. Identify the authoritative contract, target branch, exact base and candidate revisions, and the published contract that deployed clients actually use. A merge-base diff catches changes in this branch; also compare with the deployed contract when it differs.
2. Inventory independently deployed consumers: owner, release or schema version, decoder, supported lifetime, update control, and operation usage. Include old mobile and desktop clients, offline clients, jobs, partners, and generated SDKs.
3. Read the existing compatibility and support policy. Use it to choose representative oldest-supported clients and the allowed coexistence window. Missing ownership or usage data is an open removal gate, not zero usage.

Use [assets/compatibility-report.md](assets/compatibility-report.md) when there is no local format.
Read [references/consumer-checks.md](references/consumer-checks.md) when selecting diff tools, old-client fixtures, or semantic cases.

Done when the comparison revisions, consumer set, compatibility promise, and unknown consumers are explicit.

## Test schema and behavior

1. Run the repository's breaking-schema check against the exact base and candidate, such as `oasdiff breaking` for OpenAPI or `buf breaking` for protobuf. Inspect the installed tool's current official documentation and configuration before choosing its flags and compatibility mode.
2. Feed candidate wire responses into the actual decoder or generated client from each selected deployed version. Exercise unknown fields, absent and null fields, enum additions, numeric precision, dates, and changed error responses where relevant.
3. Exercise old requests against the candidate server for changed request rules and old responses against candidate consumers where deployment order requires that direction.
4. Maintain a semantic-change inventory even when the diff is clean: defaults, validation, limits, pagination, ordering, status and problem types, cache rules, authorization, retry effects, and latency or cancellation promises.
5. Match each changed assumption to a fixture with an independent expected result. Keep the old decoder unchanged; weakening it to accept the candidate does not prove deployed-client compatibility.

An optional field or enum value can still break strict or exhaustive old clients.
A tighter authorization rule may be a necessary security fix; report the break and migration impact without delaying an authorized containment action.

Done when the schema result and old-client behavior are both known, and every semantic change has a verdict or a named unresolved check.

## Plan coexistence and retirement

- Prefer a compatible extension when it preserves the promised behavior. An intentional break needs the established new-version or replacement path, consumer owners, rollout order, fallback, and an approved removal gate.
- Publish deprecation scope and replacement instructions, with a Link field using rel="deprecation" when response metadata points to migration guidance. Deprecation announces lifecycle state; it does not change endpoint behavior by itself.
- Use Deprecation with a Structured Field Date and Sunset with an HTTP date when the API adopts those fields. Sunset cannot precede Deprecation when both are supplied. Test the fields on actual responses and relevant gateway/cache paths.
- The supplemental helper checks this canonical emission profile:

  ```sh
  python3 <api-compatibility skill>/scripts/check-lifecycle-headers.py lifecycle-headers.json
  ```

  Provide JSON containing only the extracted lifecycle fields; [assets/lifecycle-headers.json](assets/lifecycle-headers.json) is a synthetic fixture. Python 3.12+ is required. The read-only helper emits JSON findings; exits are 0 pass, 1 findings, and 2 usage or unreadable input.

  This profile uses a bare Deprecation date without parameters and a GMT IMF-fixdate Sunset. It is not a general Structured Fields parser. If the API intentionally emits parameters or another accepted receiving form, use its maintained protocol parser and test that contract rather than declaring it invalid from this profile check.

- Measure deprecated-operation usage by supported client/version with safe aggregate data. Set the observation period from the support promise, offline behavior, telemetry coverage, and any contractual notice.
- Remove only after the established support obligation, measured migration, and responsible owner's authorization permit it. Retain a rollback or forward-repair plan for missed consumers.

Done when the replacement remains usable during coexistence and every removal gate has evidence or stays open.

## Adjacent work and evidence

For shaping the endpoint itself, read the `api-design` skill if installed.
For building a broader consumer-driven contract suite, hand the consumer inventory, provider states, and failing examples to the test owner.

Return the base and candidate revisions, affected consumers, schema-diff output, old-client test commands, semantic verdicts, and rollout/removal gates.
Keep source, wire, and semantic compatibility distinct.
Report unrun consumers and incomplete telemetry; neither a clean diff nor a calendar deadline establishes safe retirement.
