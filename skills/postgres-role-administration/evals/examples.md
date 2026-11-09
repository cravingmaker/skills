# Examples

Paired model runs are deferred; keep this package unevaluated until the adoption harness records runs with and without it.

## Activation

- "Audit our application and migration roles, including grants on future tables and sequences." Expect: effective-access sources, real-creator future objects and actual-login allowed/denied probes.
- "Give the database agent a bounded reader identity and prove it cannot write or escalate." Expect: the shared matrix with agent function/sequence/owner/admin paths and actual client credentials.
- "Rotate the PostgreSQL credential and enforce verified TLS for our clients." Expect: the authentication transition branch with fresh client/network/family tests, retired credential refusal and an applicable recovery path.

## Near miss

- "Design the tenant RLS policy for this API and test its tenant matrix." Expect: the `api-authorization` skill, when installed and read; this package owns role/default-ACL/bypass checks rather than policy semantics.
- "Execute this already reviewed emergency revoke on production." Expect: the `postgres-change-execution` skill, when installed and read, with the role matrix as input.
- "Choose composite keys and physical constraints for a new schema." Expect: the `postgres-schema-design` skill, when installed and read.

## Outcome

- "Reject incomplete access receipts." Fixture: extend `assets/policy-example.json` with allowed/denied future-object probes; build actual-client-shaped results with the exact policy digest. Missing, duplicate or extra result IDs and an unchanged digest after a policy edit fail `scripts/check-privileges.py`.
- "Reject false denial and privilege escalation." On that fixture, replace 42501 with syntax-error 42601, supply an administrator SET ROLE adapter, expose a forbidden reachable owner/managed-admin role, or set an administrative/RLS-bypass flag. Each is rejected; matching restricted-client receipts pass twice without writes.
- "Prove native access beyond receipt closure." Fixture: an isolated PostgreSQL database with owner, actual migration creator, runtime and agent logins; create future table/sequence/function objects through the real creator and run positive/negative probes using fresh restricted credentials. Include RLS bypass and fresh old/new credential/TLS failures. No static receipt checker alone can mark this outcome passed.
- "Run the native access fixture." With compatible PostgreSQL server tools, `tests/postgres-role-administration/run.sh` creates its own cluster. Actual reader credentials allow scoped SELECT, deny INSERT/DDL/owner switching/sequence mutation/privileged function calls with 42501, and preserve future table/sequence/function defaults under the real migrator login and owner switch. Native reachability detects a temporary forbidden owner membership, then the revoke restores the original result.
