# Examples

Paired model runs are deferred; keep this package unevaluated until runs with and without it are recorded.

## Activation

- "Add order tables whose constraints prevent cross-tenant relationships." Expect: logical-to-physical crosswalk, composite keys and a real PostgreSQL forbidden-row test.
- "Review the schema for exact money, nullable required fields and missing foreign-key indexes." Expect: scoped catalog evidence and domain-specific reasons rather than blanket type bans.
- "Map an issuer's reused code to separate stable entities and preserve the agreed generation rules." Expect: source-qualified identity and historical relationship tests without redefining the logical model.

## Near miss

- "Our sources disagree on identity and what one record means; settle the logical crosswalk." Expect: the `logical-data-modeling` skill, when installed and read.
- "Roll out this agreed column change on a busy live table." Expect: the `postgres-migrations` skill, when installed and read.
- "Tune this slow query using representative execution plans." Expect: the `postgres-query-performance` skill, when installed and read.
- "Audit who owns these objects and what a future migration grants." Expect: the `postgres-role-administration` skill, when installed and read.

## Outcome

- "Prove tenancy in a real database." Fixture: load `assets/constraint-example.sql` into a disposable PostgreSQL session; create an identifier only in tenant A, then attempt a tenant B trade referencing it. Expect SQLSTATE 23503 and `model_trades_identifier_fk`.
- "Prove reused identity without data loss." In that fixture insert tenant A issuer X code C generations 1 and 2 for entities alpha and beta; both succeed and trades join to the corresponding entity. Repeating generation 1 fails with 23505 and `model_identifiers_pk`.
- "Prove exact required quantity." In that fixture a quantity of 0.1000 reads back exactly; NULL fails 23502 and negative quantity fails 23514 with `model_trades_quantity`. Report a skip if native PostgreSQL server tools are absent; a skip does not prove the constraints.
- "Check catalog audit behavior." Fixture: `tests/postgres-schema-design/catalog-fixture.sql` in an owned PostgreSQL cluster, followed by a failed concurrent unique index on `bad.invalid_fk (tenant_id, account_id)`. The helper rejects the bad schema, invalid and INCLUDE-only FK coverage, and the swapped tenant pairing; accepts the good schema and a reversed full-key index twice; and rejects an empty scope. Raw client errors stay out of output.
