# Access matrix

Read this when creating policy and actual-client receipts or assessing effective privileges.

## Derive probes independently

Build policy from the intended job before observing current grants. The minimal starter illustrates existing read/write denial only; extend it before using it to claim a complete audit.

| Path | Positive case | Negative case |
| --- | --- | --- |
| Runtime | Intended table read/write and required sequence use. | Other tenant/schema/object, DDL, grant option, role escalation and owner/admin switching. |
| Future objects | Actual migration creator's new table, sequence and function remain usable as intended. | New objects give no unintended `PUBLIC`/reader/agent write or execute path. |
| RLS | Intended tenant rows through actual application/direct/pooled paths. | Other tenants through table, view, function, owner/BYPASSRLS paths and operations outside row policy coverage. |
| Agent | Bounded intended query through its real client. | Write/DDL, security-definer side effects, sequence mutation and reachable privileged roles. |
| Authentication | Fresh intended client with verified TLS and current credential. | Retired credential, disallowed network/family, plaintext and wrong CA/hostname. |

Object privileges accumulate through direct grants, inherited roles, `SET ROLE`, ownership and `PUBLIC`. A membership that does not inherit can still enable a privileged role switch; use installed-major membership options and test reachability separately. Review `SECURITY DEFINER` owners, qualified object references, a fixed `search_path` containing only trusted schemas with `pg_temp` last, and execute grants; read-only defaults can be changed and do not remove those paths. Do not expose function bodies or stored arguments containing sensitive material in public evidence.

Default ACLs belong to the role that actually creates objects; inherited membership does not substitute another creator's defaults. Existing objects need their own grants. A schema-scoped default revoke cannot undo a privilege granted globally by default; inspect both scopes, including default `PUBLIC` function execution. Inspect ownership and future objects after running through the actual migration creator, not a substitute test administrator.

RLS policy coverage is separate from database/schema/table access. Test table owner and administrative bypass, views/functions, `FORCE`, and non-row operations against installed-major documentation. A successful SELECT filtered to zero rows differs from a permission error; the native probe must assert exact allowed/forbidden rows and then emit its result.

## Receipt format

`policy` has a nonsecret `target_id` and nonempty `checks` array with distinct IDs. Each check names `login`, `phase`, `kind` (`sql` or `connection`), exact `probe_sha256`, `expected` (`allow` or `deny`) and permitted `codes`. For SQL also name `session_role` and `forbidden_roles`, including owner/migrator/provider admin paths inappropriate for the profile.

`results` repeats `target_id`, records `policy_sha256` for the exact policy bytes, and contains each expected check exactly once. Each result binds `id`, `login`, `phase`, `kind`, `probe_sha256`, `result`, `code`, `fresh_attempt: true` and `adapter: "actual-client"`. SQL results also record `authenticated_login`, `session_role`, `reachable_roles` and Boolean `role_flags` for `superuser`, `bypassrls`, `createrole` and `createdb`. These flags must all be false for this restricted-client checker; audit intended administrative principals separately with native tools. `reachable_roles` must reflect effective inheritance and switch paths, not only immediate membership rows. A connection-rejection adapter emits a stable classified code without copying raw client errors or credentials.

Bind receipts to protected native captures with timestamps, target/server/connection identity and the exact expected rows or failure signature. The helper checks closure and consistency; collection trust, complete policy coverage and current access remain independent review obligations.
