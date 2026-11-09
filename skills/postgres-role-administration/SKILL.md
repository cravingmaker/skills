---
name: postgres-role-administration
description: Provision or audit effective PostgreSQL roles, ownership, grants and future-object access. Use for runtime or agent database identities, privilege audits, login/TLS transitions or credential rotation; deliver a tested access matrix and the smallest scoped transition or located finding.
license: MIT
---

# PostgreSQL role administration

Prove what each actual login can do, including inherited roles, owner paths and newly created objects. Deliver a policy-to-observation matrix and either a minimal transition or a finding located at the responsible grant, owner, function or membership.

## Establish policy and effective access

1. Read the supplied access policy, actual application/job/migration logins, intended databases/schemas, object creators and credential/network paths. Separate owner, migrator, runtime, reader and agent jobs.
2. Inspect installed-major role-membership behavior, grant options, inheritance and `SET ROLE` reachability. Trace reachable owner/admin roles rather than checking direct grants only.
3. Inventory database/schema/object privileges, `PUBLIC`, predefined roles, functions, sequences, ownership, default ACLs and RLS bypass paths. Read [references/privilege-audit.sql](references/privilege-audit.sql) when collecting the bounded read-only inventory. Use its native inheritance/switch reachability and effective privilege queries as evidence; raw membership edges are candidates rather than a complete access result.
4. State allowed and denied operations per real login, including future objects created by the actual migration creator. Schema access and table access are different permissions; sequence and function paths need their own cases.
5. Propose the smallest grant/revoke/ownership/membership change that satisfies policy. Add narrowly bounded role limits and timeouts where useful; role-level/session read-only defaults alone do not enforce read-only access.

Done when the matrix covers every intended entry path and each effective permission has an attributable source. Read [references/access-matrix.md](references/access-matrix.md) when creating policy/probe receipts or reviewing default ACL and RLS edge cases. For RLS policy semantics, use the `api-authorization` skill when installed, reading its `SKILL.md` first; retain this package's role, ownership and bypass checks.

## Conditional profiles

- For an agent or MCP database identity, read [references/agent-access.md](references/agent-access.md) when provisioning or auditing that client. It uses the same effective-access matrix and checker.
- For password/HBA/TLS migration, rotation or revocation, read [references/authentication-transitions.md](references/authentication-transitions.md) when changing login or transport. It adds fresh-client and intended-network evidence to the same matrix.
- For Neon, verify current provider roles, managed-admin memberships, role creation paths, connection routing and driver transport in [Neon's documentation](https://neon.com/docs/manage/roles). Inspect actual reachable managed-admin roles rather than assuming a provider-created identity is restricted.

These branches add cases to one policy rather than creating a second privilege framework. Handle credentials through the existing secret store or protected client configuration; no password, verifier, token or full connection string belongs in reports, fixtures or command arguments. Certificate issuance, firewall persistence and agent tool/egress policy retain their separate owners.

## Prove through actual clients

Rehearse changes and future-object creation only on an explicitly disposable, contained target. Production role changes are direct operational changes; use the `postgres-change-execution` skill when installed and read first, preserving existing applicable authority.

1. Run probes through fresh restricted login credentials and the real driver/network path. Capture authenticated login and current role. Administrator `SET ROLE` is supplementary and cannot prove a restricted identity can connect or cannot escalate.
2. Test allowed reads/writes and denied writes, DDL, grant/role escalation, owner switching, administrative paths and side-effecting function calls. Assert the intended SQLSTATE/failure cause; a syntax or network error is not an access denial.
3. Use the real migration creator to create a new table, sequence and function in isolation. Re-run allowed and denied cases against them, inspecting their owner and effective/default ACLs.
4. Test RLS as the actual runtime identity across tenants, direct/pooled application paths, views/functions and owner/BYPASSRLS exceptions. Treat `FORCE ROW LEVEL SECURITY` and non-row-policy operations according to installed-major behavior.
5. For rotation/revocation, prove a fresh allowed connection using the replacement and refusal using the retired credential, keeping recovery access inside policy. Treat already-open sessions separately.

Read [assets/policy-example.json](assets/policy-example.json) when a project lacks an existing receipt format; compare it with the actual policy instead of installing it blindly. Use the read-only helper to reject incomplete or mismatched restricted-client receipts:

```sh
python3 scripts/check-privileges.py policy.json results.json
```

The Python 3.12+ helper binds exact policy/probe digests, target, login, current role and lifecycle phase. It checks expected allow/deny causes and rejects forbidden reachable roles or administrative/RLS-bypass flags on restricted SQL clients. It neither collects database evidence nor audits an intended administrator; use native catalog/driver checks for those jobs. It prints JSON to stdout and field-path diagnostics to stderr; exit 0 means receipt closure, 1 findings, and 2 usage/unreadable input.

Done when every required positive and negative probe passes through the intended client, future objects meet policy, and raw evidence supports the matrix. The package tests run native catalog, actual restricted-login and real-creator future-object fixtures on their own disposable cluster when PostgreSQL tools are available. These fixtures do not prove the user's client, credential rotation or TLS paths. A complete JSON receipt does not prove trustworthy collection; inspect the independent native captures. If client/network/provider access is unavailable, return located static findings and exact missing runtime proof.

## Deliver

Return the policy, effective-access sources, smallest candidate transition or located finding, native allow/deny/future-object/rotation evidence, checker output and unrun paths. For a physical-key or ownership design question, use the `postgres-schema-design` skill when installed and read first; avoid changing schema semantics inside a grant fix.

## Sources

At use time consult the installed-major [role membership](https://www.postgresql.org/docs/current/role-membership.html), [privileges](https://www.postgresql.org/docs/current/ddl-priv.html), [default privileges](https://www.postgresql.org/docs/current/sql-alterdefaultprivileges.html), [function security](https://www.postgresql.org/docs/current/perm-functions.html) and [row security](https://www.postgresql.org/docs/current/ddl-rowsecurity.html) references. For authentication and TLS support, use the primary sources linked by that conditional reference; this skill fixes no server/provider version or limit.
