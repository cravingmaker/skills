# Denial matrix

Read this when implementing authorization or reviewing a suspected access leak.

## Establish the oracle

Use business policy to decide who may act, on which tenant and object, on which fields, and through which entry points.
Keep expected results independent of the current handler's behavior.
When policy is unclear, isolate that decision and continue mapping reachable paths.
Do not infer broad cross-tenant administration rights from the word admin.

| Dimension | Cases to distinguish |
| --- | --- |
| Role | Anonymous, ordinary user, read-only user, service principal, privileged role. |
| Tenant | Authorized tenant, another tenant, absent context, invalid context, stale pooled context. |
| Operation | Read, create, update, delete, approve, export, and bulk equivalents. |
| Object | Own, another user's in the same tenant, cross-tenant, absent, and nested relationship. |
| Property | Allowed input/output, sensitive output, protected writable field, and a mixed payload. |
| Entry point | HTTP, resolver, bulk, export/download, job, admin, cache, database view/function where present. |

Use only applicable combinations and record why a path is inapplicable.
The CSV generator expands explicitly stated expectations; it cannot infer missing combinations or decide policy.
Every affected entry point and each applicable denial dimension need a case, even if several handlers share a helper.

## Assert the effect

For a read denial, check rows, count/aggregate values, protected fields, download links, and problem details.
For a write denial, compare durable state before and after and assert no external side effect was scheduled.
For a bulk request mixing allowed and forbidden objects, verify the documented all-or-nothing or per-item behavior.
For mixed allowed and protected fields, prove the protected field remains unchanged.
For an allowed control, check that a legitimate caller can still perform the operation and obtain the expected representation.

Use real authentication fixtures and the application's actual database role.
An authorization unit test is useful, but it cannot prove that an export or job calls the policy.
Trace each generated case to a runner assertion and retain case-level results with its observed runtime identity.
Run the result checker on that evidence; a generated expected outcome copied into the results file is not an observation.
On PostgreSQL, include the RLS branch's actual identities and direct/pooled paths in this same matrix.

## Make a failed rule observable

On an isolated fixture, remove the tenant predicate, grant a protected writable field, or bypass the policy call.
The corresponding test must fail because the forbidden row, field, or effect becomes observable.
Restore the implementation and rerun the allowed control and denial.
Do not make this counterexample by changing production permissions.

## Review mode

For a requested report-only review, keep the implementation unchanged.
Report the actor, entry point, requested object or field, expected policy, actual result, code location, and minimal synthetic reproduction.
Distinguish a reproduced leak from a suspicious path whose runtime proof is unavailable.
Hand authentication design and wider attack-model questions to their owners with the exact boundary evidence.

## Sources

The method paraphrases object, property, and function authorization concerns from the [OWASP API Security project](https://owasp.org/API-Security/) and the [OWASP authorization guidance](https://cheatsheetseries.owasp.org/cheatsheets/Authorization_Cheat_Sheet.html).
Check the project's current guidance at use time; no OWASP text or code is copied here.
