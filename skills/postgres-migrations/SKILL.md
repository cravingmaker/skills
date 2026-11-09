---
name: postgres-migrations
description: Plan and rehearse a PostgreSQL schema change on tables with traffic using expand, compatible deploy, resumable backfill, validation and contract. Use for a live-table migration; prove lock bounds and mixed-version compatibility on an explicitly disposable target.
license: MIT
---

# PostgreSQL migrations

Ship the transition as separate compatible phases and prove it under representative data and traffic. The target schema is an input; use the `postgres-schema-design` skill, when installed, to settle schema invariants first, reading its `SKILL.md` before use.

## Bind the transition

1. Inspect the project's native migration runner, transaction wrapping, ledger and lint configuration. Preserve already-applied migration bytes.
2. Record server/client versions, direct endpoint identity, actual migration creator and resulting owner, old/new readers and writers, workers, exports and external consumers.
3. For every statement, identify target objects, expected lock mode, table rewrite/scan, duration budget, resource effects and repair path from installed-major PostgreSQL documentation.
4. Read [assets/migration-plan.md](assets/migration-plan.md) when recording a migration for review; adapt its fields to the project's existing template.

Done when the candidate files and each reader/writer transition have a phase, invariant, effect bound and observable stop condition. An engine-major upgrade is a separate operational plan; this skill owns application schema evolution. Direct emergency corrections use the `postgres-change-execution` skill when installed, reading it first, rather than weakening the migration gate.

## Lint before rehearsal

Use the repository's pinned migration linter and configuration. If Squawk is selected, resolve the executable from the project's lockfile or pinned tool setup and verify CLI/rules in [Squawk's official docs](https://squawkhq.com/docs/). Read [scripts/check-migration.sh](scripts/check-migration.sh) when a small wrapper is useful for changed SQL files.

```sh
sh scripts/check-migration.sh --squawk path/to/pinned-squawk -- migrations/001_expand.sql
```

The POSIX wrapper lints only; it never connects, applies SQL, fetches tools or guesses a database URL. It accepts local files, delegates to the explicit executable and prints fixed JSON status on stdout; wrapper diagnostics go to stderr. It withholds native output because lint diagnostics may quote sensitive SQL; use the project's protected lint report for finding details. Exit 0 means lint passed, 1 lint findings, and 2 usage/setup failure. Document narrowly justified suppressions with the exact lock and compatibility evidence. A lint pass does not establish a safe rollout.

## Rehearse on an explicitly disposable target

Read [references/rehearsal.md](references/rehearsal.md) when applying candidate migrations in a test environment. Use the project's native runner or a scoped adapter against a named local/Testcontainers database or authorized isolated Neon branch. Require an explicit connection-mode declaration, such as `--connection-mode direct`, on the project adapter. Verify that mode against current provider endpoint inventory and client routing metadata. Pooled or unknown modes refuse rehearsal; a hostname pattern cannot establish direct routing. Never print connection strings, tokens, source rows or raw error payloads with private values.

1. Expand with structures that old and new code can both use. Test old-code/new-schema and new-code/expanded-schema reads and writes using their actual roles.
2. Test concurrent-index creation outside any runner-imposed transaction. After interruption, inspect invalid indexes and repair explicitly before retrying.
3. Use deferred validation only for constraint kinds supported by the installed major. Rehearse `NOT VALID` then `VALIDATE CONSTRAINT` separately where appropriate.
4. Backfill in bounded committed batches with a stable key, idempotent predicate, durable checkpoint and explicit concurrent-write policy. Interrupt after committed work, resume, and compare exact totals and values against an uninterrupted run.
5. Record lock waits and held locks from a separate observer, runner duration, replication/resource effects and workload errors. Deliberately hold a conflicting lock and prove the candidate stops within its lock budget.
6. Validate independent domain constraints and reconciliations. Contract only after every old consumer's measured compatibility/deprecation condition is met.

Set bounded lock and statement timeouts for the operation, using session settings only where the direct runner preserves the session; `SET LOCAL` needs a transaction. A queued DDL statement can itself affect traffic while waiting, so a short lock wait and bounded retry policy need evidence. Do not call a data-losing down migration a rollback; distinguish compatible code rollback, forward repair and recovery from a proved usable point.

Done when representative rehearsal proves mixed-version behavior, lock/duration bounds, interrupted-backfill resume and complete post-migration invariants. An empty-database apply is setup evidence only.

## Execution and completion

Destructive operations and production migrations need applicable explicit user confirmation; existing confirmation for this exact scope persists. Prepare the exact reviewable candidate and rehearsal evidence before asking for missing authority. An explicitly disposable target is mandatory for this skill's automatic rehearsal path; live execution uses the authorized project release process. For a scoped direct operational apply, use the `postgres-change-execution` skill when installed and read first.

Return phase files/digests, role/consumer assumptions, lint output, target identity without secrets, lock/duration observations, compatibility and resume results, repair path, and any unrun proof.

## Sources

At use time read the installed-major [ALTER TABLE reference](https://www.postgresql.org/docs/current/sql-altertable.html), [CREATE INDEX reference](https://www.postgresql.org/docs/current/sql-createindex.html), [explicit locking guide](https://www.postgresql.org/docs/current/explicit-locking.html) and the selected runner's official transaction documentation. For Neon, verify direct endpoints, branch containment and current product behavior in [Neon's documentation](https://neon.com/docs/).
