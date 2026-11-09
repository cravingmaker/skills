# PostgreSQL row security

Read this whenever authorization uses PostgreSQL RLS or claims database-enforced tenant isolation.
Use the installed server's documentation and test its actual behavior; this is an application-policy method, not a role-administration runbook.

## Check the policy semantics

- ENABLE ROW LEVEL SECURITY activates policies; an enabled table with no applicable policy has default-deny row access.
- USING governs which existing rows a command can see or target; WITH CHECK governs proposed inserted or updated rows. Inspect command-specific policies and the SELECT policies needed by reads and writes.
- Applicable permissive policies combine with OR; restrictive policies further constrain them with AND. Check role membership and every policy that can broaden access.
- Owners normally bypass row security; FORCE ROW LEVEL SECURITY subjects ordinary owner access to policies. Superuser and BYPASSRLS access still bypass it.
- SQL privileges remain necessary. Row security does not grant a privilege the role lacks.
- Whole-table operations such as TRUNCATE and REFERENCES are outside row-policy filtering. Referential-integrity checks also bypass it and can reveal information through failures.
- Setting row_security to off does not grant a bypass; it can raise an error when policy filtering would affect results.

Check those behaviors in [PostgreSQL's row-security documentation](https://www.postgresql.org/docs/current/ddl-rowsecurity.html) for the actual server major version.
Do not copy a generic policy into an existing schema without comparing ownership, role membership, and command behavior.

## Use the real identity

Inventory table owners, login roles, SET ROLE paths, role inheritance, superuser/BYPASSRLS attributes, FORCE state, and application grants.
Connect with the same login identity as the service, worker, or export path.
Capture safe test labels for session_user and current_user and verify that they correspond to the intended runtime role.
A passing test through the migration role can conceal the exact bypass the application must avoid.

Separate the request role from the migration/owner role.
For required changes to ownership, memberships, grants, or default ACLs, use the `postgres-role-administration` skill when installed.
Keep the policy and its tenant-path assertions in the authorization matrix.

## Exercise every data path

| Path or exception | Required observable case |
| --- | --- |
| SELECT, INSERT, UPDATE, DELETE | Same-tenant allow controls; cross-tenant and missing-context denials; UPDATE cannot move a row into an unauthorized tenant. |
| Owner and FORCE | Demonstrate the intended owner behavior with FORCE present/absent on a disposable fixture; privileged bypass is an explicit exception, never request authority. |
| Superuser or BYPASSRLS | Detect the bypass identity and prove request/job connections do not use it; FORCE cannot establish isolation for it. |
| Views | Identify whose privileges and policies apply; test owner behavior and security_invoker behavior where supported by the installed server. |
| Functions | Inspect SECURITY DEFINER ownership, execution grants, search_path, and tenant inputs; exercise the caller-visible path under its real role. |
| Jobs and exports | Verify the explicit authorized tenant scope of service principals, including bulk reads and alternate download routes. |
| Direct and pooled sessions | Run tenant A then tenant B and missing-context work on a reused connection; no tenant state may carry across transactions. |
| Non-row-policy operations | Verify least privileges and known constraint-error leakage; do not claim RLS protects TRUNCATE or every integrity check. |

For pooled access, establish tenant context and protected queries in the same transaction on the same checked-out connection.
Use transaction-local context with guaranteed cleanup where the driver and pool mode support it.
An arbitrary caller-controlled tenant setting is not an authorization boundary; validate how trusted identity becomes that setting.
Test absent, malformed, and stale context against a fail-closed policy.

For views, read the installed version of [CREATE VIEW](https://www.postgresql.org/docs/current/sql-createview.html); support and default security behavior must be verified.
For functions, inspect the version-matched [CREATE FUNCTION documentation](https://www.postgresql.org/docs/current/sql-createfunction.html).

## Run safely and report honestly

Create synthetic tenants and ordinary runtime-role connections in an explicitly disposable database.
Creating owners, changing policies, and exercising destructive exceptions belong only in that owned test fixture; destructive changes elsewhere need explicit user confirmation.
Keep credentials and connection strings out of output.
Label direct SQL, application, job/export, and pooled evidence separately.
If a role, pooler, or function path is unavailable, name the missing proof instead of declaring isolation from catalog inspection alone.
