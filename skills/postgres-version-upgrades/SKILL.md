---
name: postgres-version-upgrades
description: Plan and rehearse a PostgreSQL minor update or major-version transition when engine lifecycle changes. Deliver a version and extension compatibility matrix, timed cutover, recovery boundary and application evidence; use Neon's supported provider path for managed databases.
license: MIT
metadata:
  requires: "integration-test-harness"
---

# PostgreSQL version upgrades

Deliver a version-bound upgrade package with measured rehearsal and a usable recovery path.

Before rehearsal read the `integration-test-harness` skill; if it is unavailable, name the missing prerequisite and stop the rehearsal flow. Use it for real dependencies, independent assertions, fresh nonempty test selection and owned cleanup; an empty-cluster startup cannot prove application compatibility.

## Bind the installed system

Read [references/compatibility.md](references/compatibility.md) when inventorying the source, target or upgrade method. Compare [assets/upgrade-plan.md](assets/upgrade-plan.md) with the project's change plan before adapting it; it is a review outline, never a blind overwrite. Read [references/sources.md](references/sources.md) before stating supported versions, release-note actions, transfer options or provider features.

Record actual server version numbers on every source/replica, selected client and target binaries, extension versions/shared libraries, OS/architecture, locale/collation provider and versions, encoding, checksums, tablespaces, roles and topology. Use allowlisted observations with timestamps and stable nonsecret identities; never publish connection strings, raw settings, SQL bodies, dumps or provider secrets. Map every intervening major's release-note action and the selected minor's compatibility/security fixes to applicable objects, an action or a reason for exclusion. Resolve all versions, package/image digests and provider support from the installed system and primary documentation at use time.

Separate minor maintenance from a major data-format transition; choose the native or provider path supported for that exact pair. Choose among a version-matched `pg_upgrade` path, logical dump/reload or a supported logical transition using measured outage, storage, extension and topology constraints. A supplied recovery artifact must already have independent restore and application evidence with scope, recovery point and elapsed time; a backup listing alone is insufficient. If absent, prepare the package and report recovery as blocked before cutover; do not invent a new mandatory backup-skill dependency.

Done when each compatibility row has observed evidence and a disposition, the method is justified, and usable recovery coverage matches the proposed change.

## Rehearse the actual transition

Read [references/rehearsal.md](references/rehearsal.md) when running preflight, timed upgrade or recovery drills. Use an explicitly disposable source clone and destination with representative synthetic data and workload, matching versions, extensions, locale and client roles. Verify ownership and destination identity before writes; a database name containing test or an ambient connection URL is not proof of authority. Contain copied jobs, subscriptions, credentials and network egress so a clone cannot act on production services.

- For a minor update, run the supported package/provider maintenance path in the rehearsal environment; prove restart, extension behavior, replica health and actual application reconnect. `pg_upgrade` is not the minor-update method.
- For `pg_upgrade`, use the target version's executable, explicit old/new binary and data paths, ports and sockets; run its applicable `--check` first, then the full selected transfer mode. Check mode is compatibility evidence, not a timed rehearsal or restore.
- For dump/reload, account for every database and cluster-global dependency using version-supported clients; reconcile ownership, grants, extensions, sequences, large objects and external objects after the actual restore.
- For logical cutover, prove initial-copy completeness, ongoing apply, write fencing and final catch-up, then reconcile DDL/schema, sequence state and large objects explicitly. A streaming table count cannot establish complete database coverage.
- For Neon, verify the current supported version-transition path, project/branch/endpoint identities, region, extension support and connection changes in official provider documentation. Read [references/neon-upgrades.md](references/neon-upgrades.md) when taking this branch; never prescribe host package commands or `pg_upgrade` against managed storage.

Measure the full critical path: fencing/drain, final copy/apply, transition, statistics/index work, application reconnect, independent verification and resuming service. Record capacity peaks, query plans and error/latency observations for the same representative workload before and after; report the dataset/workload limits on the timing estimate. Treat version-specific statistics and collation/index actions as part of the outage or warm-up budget where they affect service; do not assume statistics are always transferred or always discarded.

Done when preflight and full rehearsal pass on the selected path, all applicable objects and real clients are checked, measured bounds fit the owner's budget, and failure/recovery scenarios have evidence.

## Make the cutover reviewable

Define the single writer, exact fence evidence, old/new connection inventory, final catch-up condition, abort thresholds and who can resume writes. State when the old cluster ceases to be reusable for the selected transfer mode; link mode and destructive transfer modes need mode-specific limits. Keeping separate data files does not reconcile writes accepted after cutover. Set a new-write recovery or reconciliation path before allowing those writes; reverse replication is not an assumed rollback. Rehearse abort before the boundary and the agreed forward repair or restore after it. Preserve the old artifacts until the approved recovery horizon is met.

For schema evolution use the `postgres-migrations` skill when installed; for operational SQL execution use the `postgres-change-execution` skill when installed; for query regressions use the `postgres-query-performance` skill when installed. Read each named skill's `SKILL.md` before relying on it; leave optional flows unavailable when the method is missing rather than restating its procedures here. When coordinating application/artifact rollback, use the `release-rollback-planning` skill when installed. Host package/service lifecycle remains with the system owner; database access policy remains with the existing database-role owner.

Production updates, data-directory changes, writer/traffic changes, deletion and credential rotation require explicit authorization for that exact scope; prior authorization persists. Prepare commands, compatibility evidence, rehearsal and recovery boundary before asking for any missing authorization. Immediately before mutation confirm account, project, region, cluster, source/destination and current writer, marking genuinely inapplicable fields for self-hosted local targets. Automatic writes require an explicit disposable target and must refuse otherwise; no supplied script connects to or mutates a database.

Done when the package names authorized steps and stop points, post-update server/client versions and extension state are observed, application/access/data/plan checks pass, and recovery handling covers new writes. For a plan-only task return the reviewable package and explicitly unrun execution evidence. Return compatibility dispositions, command/artifact hashes, preflight and selected rehearsal results, measured outage, writer/catch-up proof, post-update evidence and unresolved blockers.
