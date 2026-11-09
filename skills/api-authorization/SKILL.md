---
name: api-authorization
description: "Enforce object, property, function, and tenant authorization, then prove allowed and denied paths with a matrix. Use for cross-user leaks or access changes in endpoints, bulk actions, exports, jobs, and admin paths. Includes PostgreSQL RLS behavior; identity-provider design is separate."
---

# API authorization

Deliver enforced access rules and a denial matrix that exercises every affected data path under its actual runtime identity.

## Specify the access decision

1. Read the authentication boundary, authorization policy, data-access code, and affected entry points. Work from trusted authenticated identity; request bodies, tenant headers, cursors, and object IDs cannot grant authority.
2. Enumerate role, tenant relationship, operation, object relationship, readable/writable property, and entry point. Include unauthenticated callers, missing tenant context, unrelated users in the same tenant, and cross-tenant objects where applicable.
3. Write explicit allow and deny expectations from the product's policy. Include a successful authorized control so an implementation that rejects everything cannot pass.
4. Trace alternate access through bulk and nested operations, export/download paths, resolvers, jobs, service principals, caches, and internal/admin routes. Record legitimate privileged exceptions and their authorization boundary.

Read [references/denial-matrix.md](references/denial-matrix.md) when defining cases, or when reviewing an existing implementation without permission to edit it.
Use [assets/authz-matrix.csv](assets/authz-matrix.csv) as a shape example with synthetic labels; replace its policy with the application's policy.

Done when each affected path has an explicit policy, including allowed controls and denied object, field, and function access.

## Enforce at the protected operation

- Apply tenant and owner predicates in the query or protected command, including writes. Bind the tenant from trusted identity, and check affected-row results.
- Put tenant identity into keys and relationship constraints where cross-tenant references would violate the domain. A route prefix or a globally unique ID does not establish ownership.
- Allowlist writable fields before constructing updates and readable fields before serializing responses. Reject or omit protected fields according to the documented contract; test mixed allowed/protected input.
- Authorize nested objects, batch members, count and aggregate results, exports, and admin actions as deliberately as a single-object handler. Define batch atomicity and partial-failure behavior.
- Bind caches, cursor interpretation, and replay results to the applicable identity and authorization scope. Recheck permission when it can have changed.
- Use PostgreSQL RLS as another enforcement layer when the design chooses it. Read [references/postgres-rls.md](references/postgres-rls.md) before making an RLS claim; enabling a table flag alone proves no runtime isolation. Compare [assets/rls-policy.sql](assets/rls-policy.sql) with the existing schema only when a transaction-local tenant policy is appropriate.

For an existing-system review, report reachable violations with code paths and reproducible synthetic cases; make changes only within the user's requested scope.

Done when the same access policy protects the primary path and every affected alternate path.

## Prove the matrix

Expand explicit cases with the read-only helper:

```sh
python3 <api-authorization skill>/scripts/authz-matrix-cases.py authz-matrix.csv
```

It needs Python 3.12+ and emits JSON test inputs on stdout.
CSV columns are `role,tenant,operation,object,property,entrypoint,identity,expect`; pipe-separated values in the first six columns expand to individual cases.
Declare one runtime identity per row; IDs bind the cell, identity, and expected outcome.
Expectations are `allow` or `deny`; blanks, wildcards, repeated cells, and missing allow/deny controls fail.
Exits are 0 expanded, 1 matrix findings, and 2 usage or unreadable input.
The configurable `--max-cases` bound limits local expansion work.
Use synthetic fixture labels rather than secrets or production records.

The helper creates inputs; it does not execute requests or infer that the matrix covers the service.
Record `id,observed,identity` CSV rows from the real entry-point assertions and actual runtime identity, then check coverage and outcomes:

```sh
python3 <api-authorization skill>/scripts/authz-matrix-cases.py authz-matrix.csv --results authz-results.csv
```

The checker rejects failed denials, over-denied controls, missing/unknown/duplicate results, and wrong or unrecorded identities.
It checks the recorded evidence; retain runner output that establishes the observations.
Changed cells or identities require new results; row reordering preserves IDs.
Compare the expanded cases with the entry-point inventory, then drive them through the real application and, for RLS claims, real PostgreSQL using actual login roles and connection paths.
For each denial, assert the status or policy outcome, absence of forbidden fields and records, unchanged protected state, and absence of external effects.
For allowed controls, assert the intended effect and readable fields.
Check existence leaks through counts, errors, and constraint failures as well as returned rows.

Use bounded tests against owned, authorized targets.
Keep credentials and personal data out of fixtures, logs, matrix output, and reports.
Destructive database tests require an explicitly disposable target; destructive operations on other data need explicit user confirmation.

Done when every matrix cell has an observed assertion result, the result checker passes, and a missing tenant predicate or writable-field restriction makes a relevant test fail.

## Adjacent work and completion

Identity, token, session, and OAuth design belong to the authentication owner; a system threat model is a separate security job.
When the fix needs PostgreSQL ownership, role membership, grants, or default privileges, read the `postgres-role-administration` skill if installed.
When a real dependency harness is missing, read the `integration-test-harness` skill if installed.

Return the policy and entry-point inventory, matrix path, enforcement locations, exact test commands, runtime roles/connection paths, and observed allow/deny results.
Keep privileged exceptions and unavailable runtime evidence visible.
A generated matrix, mocked repository, or migration-owner session cannot establish tenant isolation.
