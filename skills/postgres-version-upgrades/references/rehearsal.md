# Upgrade rehearsal

Read this when executing preflight, the full transition or a recovery drill on an explicitly disposable target. No helper in this package performs database operations; use the project's native runner under the required integration-test method.

## Preflight

Bind a run ID to owned source/destination identities, paths/endpoints, binaries, data seed, roles, network containment and cleanup. Verify the copied source and every tablespace/WAL path cannot alias production or another run; use distinct ports and sockets and disable copied external effects. Register cleanup before setup so assertion/setup failure and interruption leave recoverable owned resources.

For a physical transition, run the target binary's `pg_upgrade --check` with explicit old/new binary/data directories and the chosen transfer-mode options after checking its installed help. Retain native output in a protected artifact and summarize exit status and findings without raw private values. A successful check does not exercise full copy duration, application semantics, all extension binaries or restore usability. A major upgrade can execute source-superuser-controlled code; trust and contain the source accordingly.

## Full-path evidence

1. Load representative synthetic tables, constraints, indexes, roles, extension data, sequences and large objects; include the applicable topology and client modes. Record independent expected rows, keys, quantities, ownership and access results before transition.
2. Exercise the real selected path and measure its milestones, peak disk/WAL/memory demands and workload impact. Include statistics/index actions required by installed-version documentation.
3. Run old/new client reconnect and actual application operations. Read committed writes through a separate connection, test permitted and denied access, and compare semantic results and representative plans with the pre-transition baseline.
4. For logical transitions, reconcile schema/DDL and global objects separately from replicated table rows; verify sequence allocation by inserting after synchronization, and check known large-object bytes and owners. Verify every relevant database and external dependency, not only the default database.
5. Stop new source writes through every writer path, drain or reject old sessions/jobs and show the fence rejects an attempted old-writer commit. Observe final apply/catch-up with a version-appropriate durable position plus exact data assertions; zero instantaneous lag alone is insufficient.
6. Allow a known acknowledged write on the new system, then exercise the agreed post-boundary recovery/reconciliation case. Count that write explicitly in the result; restarting the old database and losing it cannot pass an accepted zero-loss claim.

Use native runner output and a fresh nonempty expected test selection through the integration-test method. Perturb one relevant compatibility or object-coverage condition so the corresponding check fails, restore it, and rerun. A pure JSON receipt or a mocked database cannot stand in for an executed upgrade. If tools or representative data are absent, stop that proof branch and report the exact unrun evidence.

## Rollback boundary

For copy/clone paths verify actual file independence and required storage semantics; even an untouched old source lacks later writes. For link mode use the installed-major procedure's precise point after which starting the new cluster makes the old one unsafe; preserve a separately usable recovery point. If the chosen version offers a transfer mode that modifies the old cluster during transfer, its boundary can precede first target startup; do not generalize link-mode rules to it. Rehearse abort before the selected boundary and forward repair, restore or tested reconciliation after it. Preserve original artifacts and recovery evidence through the approved horizon; cleanup must not erase the fallback before approval.

After transition, re-establish version-compatible backup and recovery coverage. For a self-hosted physical chain, take and verify the new-major base backup and required WAL; an old-major physical backup needs its compatible binaries to restore. For Neon or logical protection, verify the supported provider or export recovery path instead of issuing host commands. A completed backup job alone does not prove restore usability.

Report preflight versus full rehearsal, conversion versus total service outage, data/workload scale, actual application checks, recovery/new-write result and cleanup state separately.
