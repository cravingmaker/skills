# Examples

These are unrun paired-evaluation scenarios; no real database transition is implied by authoring the package. The evaluation harness must provide an explicitly disposable target for every case that writes.

## Activation

- "Plan and rehearse our PostgreSQL minor patch with a restart budget." Expect: actual version/release-note/extension inventory, supported maintenance path and measured reconnect/application evidence; no unnecessary major-conversion procedure.
- "Prepare a PostgreSQL major transition and a rollback plan for the chosen transfer mode." Expect: target-version native preflight, full representative rehearsal and an exact recovery boundary that accounts for new writes.
- "Move our Neon workload to a supported newer engine major." Expect: verify the current provider method and destination identities; use the supported migration/transition path without host-storage commands.

## Near miss

- "Add an index and migrate a live table without changing PostgreSQL's engine version." Expect: the `postgres-migrations` skill owns schema evolution.
- "This query is slow after a deployment; inspect its execution plan." Expect: the `postgres-query-performance` skill owns a query regression unless evidence identifies an engine transition.
- "Grant a reporting role access to future tables." Expect: the `postgres-role-administration` skill owns access policy and effective grants.
- "Run deploy-checklist for an application release with no database engine change." Expect: the existing deployment-readiness process owns the request.
- "Use incident-response to coordinate a database outage." Expect: the existing incident process owns coordination; no opportunistic engine upgrade as mitigation.

- "Upgrade the database host operating system without changing the engine version." Expect: the host-maintenance owner handles this request.
- "Bump the PostgreSQL client driver dependency." Expect: ordinary dependency work; engine-transition planning stays out.
- "Run this REINDEX on production now without an engine change." Expect: the `postgres-change-execution` skill owns the scoped operational apply.

## Outcome

- "Review physical preflight and transfer recovery claims." Fixture: provide observed source/target binary manifests, two extension dependencies with one missing target library, and a selected transfer mode. Expect: the missing library blocks readiness even if native check mode succeeds; copy/link/destructive-mode boundaries are checked against target-version documentation and restore usability is separately evidenced.
- "Rehearse a logical transition completely." Fixture: an explicitly disposable real source/destination pair with a seeded table, sequence whose current value exceeds the maximum stored key, a large object with known bytes/owner, global roles/grants, and a job capable of writing. Expect: independently reconcile all applicable objects, reject a real old-writer commit after fencing, validate a new sequence allocation and retain nonempty real application/access tests; table-only replication cannot pass.
- "Check post-cutover rollback with new writes." Fixture: preserve an independently restored recovery artifact, acknowledge a distinct new row only on the upgraded target, then trigger the chosen recovery path. Expect: the row is reconciled or its loss is explicitly within the owner's approved budget; restarting the old database alone fails an accepted zero-loss claim.
- "Report plan-only or unavailable rehearsal honestly." Fixture: only a read-only inventory and a backup listing are supplied, with no isolated target or restore proof. Expect: return the reviewable matrix and commands with rehearsal/recovery blockers, make no database mutation, and make no completed-upgrade claim.
