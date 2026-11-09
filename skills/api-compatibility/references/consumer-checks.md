# Consumer checks

Read this when choosing compatibility tools and old-client fixtures or planning a deprecation.

## Keep the three contracts distinct

| Contract | Typical break | Proof |
| --- | --- | --- |
| Source | A generated SDK changes a required argument or return type. | Compile the consumer with the relevant generated SDK and dependency set. |
| Wire | An old decoder rejects a field type or new enum variant. | Decode candidate responses with the unchanged released decoder. |
| Semantic | A default, order, side effect, limit, or access rule changes. | Run the old journey and compare its observable result with the supported promise. |

A repository's new types are not a substitute for an old shipped decoder.
Capture fixture provenance: released artifact or source revision, generator settings, runtime, input bytes, and independent expected output.
Use synthetic records and tokens in fixtures.
If the old runtime or binary is unavailable, preserve its inputs and label that consumer untested.

## Choose the actual baseline

Resolve the branch merge base without rewriting history.
Generate both schemas with their own revision's locked tool chain where schemas are derived; using the new generator on both can hide drift.
Compare with the published/deployed contract too when it differs from the target branch.
Avoid mutable remote URLs as the sole baseline; retain the contract bytes and revision.

Use the existing schema-diff configuration, including its ignore rules.
Read an ignore before treating a clean run as proof.
Verify syntax and compatibility categories in [oasdiff's documentation](https://www.oasdiff.com/) or [Buf's breaking-change documentation](https://buf.build/docs/breaking/) for the installed tool.
Do not quietly suppress a new break to get CI passing.

## Build cases from changed assumptions

- Responses: absent versus null, unknown properties, exhaustive enums, arrays versus empty results, large exact numbers, time zones, and content negotiation.
- Requests: old defaults, previously accepted values, omitted fields, byte and batch limits, signatures over serialized bytes, and stricter validation.
- Journeys: ordering, pagination completion, error handling, retries after uncertain outcomes, caching, authorization, and operation latency/deadlines.
- Deployment: old caller/new server, new caller/old server where needed, and both versions during the actual rollout.

An enum addition is compatible only when supported consumers tolerate it.
Adding pagination can truncate a collection an old caller expected to be complete.
Changing authorization requires explicit impact treatment even if a schema tool cannot see it.

## Retire with evidence

Record the supported-client inventory, notice obligation, replacement readiness, aggregate usage by version, observation coverage, and removal owner.
Include offline or rarely connected consumers when defining the observation period.
Do not invent a universal number of days.
Document which resources the lifecycle fields cover, and link migration guidance using the API's established documentation convention.
Use a Link field with rel="deprecation" for migration guidance and rel="sunset" for an availability policy where useful.
For field or parameter deprecation, mark the authoritative schema and measure that field's usage through request data or client/SDK telemetry; resource headers alone do not identify the field.
Check cache behavior so old lifecycle signals do not outlive the intended transition.

Deprecation uses a Structured Field Date; Sunset uses an HTTP date.
The helper is deliberately a canonical sender-profile check, not an implementation of every permitted field parameter or legacy receiving form.
When both fields exist, test their chronology without comparing their strings lexicographically.

## Sources

The methods are paraphrased from [Google's compatibility policy](https://google.aip.dev/180), [HTTP Deprecation](https://www.rfc-editor.org/rfc/rfc9745.html), [Sunset](https://www.rfc-editor.org/rfc/rfc8594.html), and [Structured Fields](https://www.rfc-editor.org/rfc/rfc9651.html).
Support windows, installed tool behavior, and each consumer's release state must be checked at use time.
