# Budget input

Read this when filling `budget.json` or reviewing the helper's counts. All counts are nonnegative integers; booleans and fractional counts are invalid. Group instance and pool counts, client limits, backend allocations and the database limit must be positive. The operator reserve must be positive even when migrations or other clients are zero.

| Field | Meaning |
| --- | --- |
| `database_limit` | Observed server session limit before the allocations listed below. |
| `unavailable_connections` | Server-reserved or otherwise unavailable slots, excluding the separately listed operator reserve. |
| `other_connections` | Peak consumers outside the modeled groups, excluding migration and operator allocations. |
| `migration_connections` | Maximum simultaneous migration or direct administrative tool sessions. |
| `operator_reserve` | Additional usable sessions kept for the operator. |
| `direct_groups` | One `{instances, pool_max}` object per peak process group connecting directly. Include worker processes and rollout overlap. |
| `poolers` | One object per distinct pooler allocation sharing this server. Use `client_groups`, `client_limit` and `backend_slots`. |

Each pooler's `client_groups` uses the same `{instances, pool_max}` format. Its `client_limit` must describe the same pooler scope as those groups. Its `backend_slots` is the aggregate possible server allocation, including every database/user pool, replica and applicable reserve pool; it is not one per-user default copied as a global cap. Split budgets by server when endpoints route to different servers. Resolve overlapping allocations explicitly instead of summing the same server pool twice.

The server total is direct sessions plus pooler backend allocations plus unavailable, other, migration and operator slots. Each pooler's client total is checked separately against its own limit. The helper emits both totals and signed headroom, with limit findings as stable identifiers. It prints no input labels, URLs or arbitrary input values.

Reject unknown keys to catch misspelled or silently omitted accounting fields. An empty topology is invalid; for an HTTP-managed path without a visible pool, obtain the provider's actual allocation or record the budget as unknown rather than inventing a zero.

The example input yields 33 server slots: 12 direct, 10 pooled backend, 3 unavailable, 2 other, 2 migration and 4 operator slots. Its pooler has 40 client connections against a limit of 100. The script's offline tests include an over-limit case caused by overlapping workers, a pooler-client-only overflow, exact-boundary acceptance and malformed counts.
