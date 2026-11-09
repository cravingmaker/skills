# Examples

Run these cases with and without the final skill in restored identical fixtures when model evaluation is authorized.
This draft has no paired model runs.

## Activation

- "User B can read user A's invoice by changing the URL ID. Fix it and prove exports are protected too." Expect object and tenant predicates plus denial tests for both paths.
- "Add tenant isolation to our PostgreSQL-backed API and background export job." Expect actual application and job identities, RLS policy semantics, and direct/pooled paths in one matrix.
- "Review our bulk update for protected-field and admin-function bypasses; report only." Expect synthetic reproductions and evidence-backed findings without edits.

## Near miss

- "Choose an OAuth provider and design session rotation." Expect authentication design rather than this enforcement method.
- "Remove unused PostgreSQL login roles and repair default grants." Expect the `postgres-role-administration` skill to own operational privileges.
- "Design the new endpoint's pagination and error schema." Expect the `api-design` skill.
- "Create a disposable real PostgreSQL integration fixture." Expect the `integration-test-harness` skill to own the missing harness.

## Outcome

- "Expand the authorization cases." Fixture: assets/authz-matrix.csv. Expect fourteen concrete cases with explicit allow/deny values; an added duplicate cell or blank dimension fails, and expansion alone is not reported as tested access. Produce id,observed,identity results from real assertions; the checker must reject a leaked denial, deny-all behavior, missing or duplicate results, and an owner-role identity.
- "Prove the API is isolated even though its migration role owns the tables." Fixture: two synthetic tenants, an RLS-enabled table, an owner/migration role, a non-owner runtime role, and a job connection accidentally using the owner. Expect owner bypass to be reproduced and the job path to fail the intended denial until the runtime identity is corrected.
- "Reject stale matrix results." Fixture: retain successful results, change the operation or declared identity in the matrix, then recheck the old results. Expect unknown/missing-result findings; reordering unchanged rows still passes.
- "Check tenant context across pool reuse." Fixture: a single reusable connection runs tenant A, tenant B, then a request with no tenant context. Expect no A records in B's result, a fail-closed missing-context result, and allowed same-tenant controls.
- "Prove protected properties cannot be overwritten." Fixture: a member may update display_name but not tenant_id or is_admin, through both single and bulk handlers. Expect mixed-field policy assertions and unchanged protected state; removing the allowlist makes the test fail.
