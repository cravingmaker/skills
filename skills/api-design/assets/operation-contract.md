# Operation contract

Compare this starter with the repository's format before using it.

- Authoritative source and generation command:
- Operation identifier, method, path, caller, and success condition:
- Resource identity and lifecycle:
- Request fields, types, absent/null behavior, and writable-field allowlist:
- Success status, headers, response schema, and example:
- Effective security declaration and authorization enforcement point:
- Conditional update or cache policy:
- Request, page, batch, response, and query-cost bounds:
- Pagination order, unique tie-breaker, cursor binding, expiry, and consistency:
- Retry policy and link to any admission/replay contract:
- Affected deployed consumers and compatibility review:

| Failure | Wire status | Stable problem type | Safe detail and extensions | Test |
| --- | --- | --- | --- | --- |
| Malformed input | | | | |
| Permission denied | | | | |
| Domain conflict or stale version | | | | |
| Dependency failure | | | | |

| Proof | Command or test | Observed result or unavailable reason |
| --- | --- | --- |
| Dialect and examples | | |
| Generated caller compile | | |
| Status, headers, and body | | |
| Preconditions and list boundaries | | |
