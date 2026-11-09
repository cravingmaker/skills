---
name: postgres-schema-design
description: Design PostgreSQL tables and constraints that enforce supplied identity, relationship, type and tenancy rules. Use when adding or reshaping a target schema; deliver the logical-to-physical crosswalk and real database counterexamples. Live rollout belongs to postgres-migrations.
license: MIT
---

# PostgreSQL schema design

Make the database enforce the domain rules for every writer. Start with the supplied logical identity, cardinality, grain and lifecycle; preserve them in an explicit crosswalk to columns and constraints.

## Design from invariants

1. Read the schema, migration tool, ORM mappings, actual writers and representative queries. Read the target server major and provider support before choosing syntax.
2. List each rule and its positive and invalid-row examples. Where identity or relationships are disputed, use the `logical-data-modeling` skill when installed, reading it first; carry unresolved meanings into the design.
3. Choose stable primary keys separately from mutable public/source identifiers. Compare identity columns and UUID generation against locality, offline creation and exposed-identifier needs. Check built-in UUID generation support live rather than assuming it.
4. Use `timestamptz` for instants, `date` for business dates and an explicit zone policy for local schedules. Use exact numeric values or integer minor units with a declared scale and currency for money.
5. Make absence explicit: prefer `NOT NULL` when a value is required, and define when NULL means unknown or inapplicable. A `CHECK` alone can leave NULL accepted.
6. Express uniqueness, valid values and relationships with constraints. A `CHECK` is not a general cross-row concurrency mechanism; choose a suitable unique/exclusion constraint or a transaction protocol.
7. Put tenant identity in the relevant unique and foreign keys. Name delete/update behavior. Consider referencing-side indexes for joins, parent changes and deletes; prove any intentional omission against the workload.
8. Use JSONB where flexibility earns it, with a document version, validation/size policy and indexed access paths. Keep relationships and stable invariants enforceable. Choose enums, lookup tables or text plus checks from the change policy rather than habit.

Done when each rule maps to a type, key, constraint or separately owned transaction rule, and the original logical grain and identity remain unchanged. Read [references/design-cases.md](references/design-cases.md) when source identifiers can be reused, time ranges matter, or an apparent relationship could cross tenants. For supported temporal-key syntax and extensions, verify the installed major's [CREATE TABLE reference](https://www.postgresql.org/docs/current/sql-createtable.html) and provider extension support at use time.

## Inspect catalogs, then test invalid data

Read [references/catalog-audit.sql](references/catalog-audit.sql) when inspecting an existing target schema. Run `python3 scripts/audit-schema.py --schema <name>` through authorized libpq service/environment configuration; [the helper](scripts/audit-schema.py) requires Python 3.12+ stdlib and compatible `psql`, emits JSON metadata, and exits 0 for no leads, 1 for leads or empty scope, and 2 for usage/setup/query failure. It withholds raw client errors. Its read-only queries are review leads: a local schedule may need a zone-free timestamp, and a nullable column may be deliberate. Compare results with the crosswalk, comments and workload before treating a row as a defect. Use authorized read-only access; keep connection details and row data out of output.

Run constraint tests on an explicitly disposable PostgreSQL target, using the project's test setup. Read [assets/constraint-example.sql](assets/constraint-example.sql) when building a minimal identity and tenancy fixture; compare it with the project rather than installing it blindly. The example creates objects and is intended only for a disposable database. The package's `tests/postgres-schema-design/run.sh` creates its own temporary cluster or reports a clean skip when native server tools are absent.

- Insert valid boundary rows and read them through the actual client/ORM, checking numeric scale and instant round trips.
- Attempt duplicate keys, missing required fields, invalid values, orphan links and cross-tenant links; assert the expected SQLSTATE and constraint identity.
- Reuse a source code in a later generation and prove both entities and their historical relationships remain distinct.
- Inspect actual constraint, index validity and ownership catalogs; declaration text alone cannot prove installation.

Done when deliberately invalid rows fail for the intended constraint, valid boundary rows succeed, and consumer joins preserve exact keys and quantities. Use the `integration-test-harness` skill, when installed, if a real-client harness needs to be built; read it first. Unrun PostgreSQL tests remain an explicit verification gap.

## Deliver and route

Return DDL, the invariant-to-constraint crosswalk, catalog findings with reasons, actual test output and remaining semantic decisions. For live deployment sequencing, use the `postgres-migrations` skill when installed, reading it first. For measured access-path choices, use the `postgres-query-performance` skill when installed, reading it first. For object ownership and future grants, use the `postgres-role-administration` skill when installed, reading it first. RLS policy semantics go through the `api-authorization` skill when installed and read; composite tenant keys still protect structural relationships.

## Sources

Read the installed-major versions of the [constraint documentation](https://www.postgresql.org/docs/current/ddl-constraints.html), [numeric types](https://www.postgresql.org/docs/current/datatype-numeric.html), [date/time types](https://www.postgresql.org/docs/current/datatype-datetime.html) and [JSON types](https://www.postgresql.org/docs/current/datatype-json.html) when selecting their behavior. No server version, extension availability or provider limit is fixed by this skill.
