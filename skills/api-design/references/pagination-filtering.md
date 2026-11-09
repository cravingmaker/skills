# Pagination and filtering

Read this when an operation returns a collection or accepts filters and sort keys.

## Make the ordering total

Choose keyset pagination for a growing ordered collection when its access pattern supports it.
Offset pagination remains useful for small bounded lists and explicit random page access; measure deep-page cost before promising it.
Append a unique tie-breaker to a nonunique sort key and define null ordering, collation, and direction.
Choose an index from the actual predicates and order; a cursor does not make a query efficient by itself.

For a descending created_at/id order, the next-page comparison must carry both values and apply the corresponding lexicographic boundary.
Use fixtures with several equal timestamps and page boundaries inside that tie.
Assert that a static collection is exhausted without duplicates or omissions.
Then test inserts, deletes, and mutable sort keys between pages against the documented consistency policy.
A cursor alone cannot promise a snapshot; a snapshot or high-water mark needs its own implementation and lifetime.

## Bind and bound the cursor

Bind cursor interpretation to the tenant, filters, sort order, and contract version that produced it.
Use an opaque token with a documented expiry and invalid-token response.
Base64 provides encoding; use a maintained signing mechanism or server-side state when integrity or confidentiality is required.
Authorize every page independently.
Define page-size defaults and maxima, final-page behavior, and whether a requested total is exact, estimated, or absent.

## Parse filters and sorting

Allowlist identifiers, operations, and sort keys before building the query.
Parameterize values rather than interpolating them into SQL.
Define absent and null behavior, time boundaries and zones, string comparison, repeated fields, and invalid combinations.
Bound filter nesting or count when the grammar permits expensive expressions.
A short API can use typed query parameters; a richer grammar needs a parser and query-cost constraints.

## Fixtures

Cover an empty list, one row, an exact page boundary, a partial final page, equal sort keys, and the maximum allowed size.
Reject an excessive page size, invalid or expired cursor, changed filter/order, and a cursor from another tenant.
Include an injection-shaped sort key and confirm it never becomes an identifier in generated SQL.
Observe query count and representative plans separately from response correctness.

## Sources

These rules paraphrase [Google's pagination guidance](https://google.aip.dev/158) and [filtering guidance](https://google.aip.dev/160).
Those documents describe Google's design policies; adopt the relevant choices rather than treating them as universal HTTP requirements.
