---
name: postgres-change-execution
description: Prepare and execute a scoped direct PostgreSQL or Neon data fix, grant or emergency administrative change on a non-disposable target. Use for an operational apply; bind the exact candidate, current preconditions, effect bounds, authority and independent verification.
license: MIT
---

# PostgreSQL change execution

Turn an operational change into an exact candidate with target-bound preconditions and independent proof of its effects. Use a native tool or project-specific adapter; this package supplies no privileged SQL runner.

## Prepare the reviewable candidate

1. Resolve the requested outcome, affected objects/keys, target deployment/branch/endpoint, database, server identity and effective principal from authorized read-only evidence.
2. Locate existing applicable authority. Confirmation for this exact target, candidate and effect persists; request only missing authority after the concrete candidate and evidence are ready.
3. Inspect the actual constraints, triggers, sequences, security-definer functions, foreign tables and other indirect effects. Separate transactional effects from effects that rollback cannot undo.
4. Store exact candidate bytes and digest, independent precondition queries, exact expected row/key set, maximum affected rows, positive lock/statement timeouts, stop conditions and independent post-change assertions.
5. For a destructive change, locate explicit user confirmation and a verified usable recovery point for the affected target and objects. A successful backup job or a configured history window alone does not prove recovery.

Read [assets/change-plan.json](assets/change-plan.json) when recording these fields; it is a synthetic comparison starter, never an execution instruction. Read [references/execution-contract.md](references/execution-contract.md) when building the native/project adapter or assessing transaction and recovery boundaries.

Done when the exact candidate and its effects are reviewable, authority is located or explicitly pending, and each precondition has an independent observation and stop rule. For deployable schema evolution, use the `postgres-migrations` skill when installed and read first. An emergency schema correction that must persist also gets a follow-up deployable migration through that method. For role-policy choices, use the `postgres-role-administration` skill when installed and read first; return here for the authorized direct apply.

## Rehearse and compare

Rehearse nontransactional, sequence, trigger and external effects on an explicitly isolated disposable copy with external jobs, subscriptions, egress and live credentials contained. A `BEGIN`/`ROLLBACK` exercise is insufficient for effects outside that transaction, including consumed sequence values. `EXPLAIN ANALYZE` executes its statement; use non-executing inspection first and execution only on an authorized contained target.

The read-only helper compares plan and observation files before the native adapter's final recheck:

```sh
python3 scripts/check-change.py change-plan.json current-observation.json candidate.sql
```

It uses Python 3.12+ stdlib and never opens a database connection or writes files. It prints a JSON summary to stdout and value-free diagnostics to stderr; exit 0 means ready for native recheck, 1 rejection, and 2 usage/unreadable input. It rejects changed candidate bytes, wrong target/principal, stale observations, changed preconditions or selected keys, and excess effects. It checks receipt references and declarations, not whether an authority or recovery receipt is valid; inspect those sources before relying on them. Keep observations and candidate files free of credentials and personal record values; publish only allowlisted summaries.

Done when isolated rehearsal covers the actual side effects and the helper accepts fresh matching evidence. A helper pass neither authorizes the change nor closes the race between observation and apply.

## Apply through the bounded adapter

1. Reconnect to the intended target and check both connection metadata and server-side identity. Abort on a mismatch; do not rely on a hostname or `current_database()` alone.
2. In the same session/transaction as the change, set bounded timeouts and stop-on-error behavior, acquire the relevant locks or use a proved conditional mutation, and recheck predicates, key/value fingerprints and counts before applying the exact candidate.
3. Assert the actual affected rows/keys against the exact expectation and maximum before commit. On error, mismatch, timeout or unexpected partial effects, stop; inspect state before any retry.
4. For nontransactional operations, use the rehearsed stepwise adapter, recorded checkpoints and repair/stop conditions. Do not pretend a later rollback undoes an earlier committed step.
5. Commit only when in-transaction assertions pass and commit is inside the applicable authority. If the result is uncertain after a disconnect, read actual state and the operation marker before retrying.
6. Verify through independent catalog/data/application observations, including unchanged neighboring records, ownership/access and external effects where applicable. Preserve the old state and recovery evidence for the agreed window.

Done when the observed committed state meets the requested outcome and independent assertions, with actual effect counts and any remaining partial effects recorded. If concurrency protection, recovery or authority is missing, return the concrete package and missing condition; diagnostic access does not grant execution authority.

## Report

Return target/principal identity without secrets, candidate digest, applicable authority reference, observation/rehearsal receipts, actual counts, commit/result status and independent verification. Distinguish prepared, rehearsed, attempted, committed and verified states. On failure, include the durable checkpoint and next safe inspection, with no automatic unbounded retry. For unavailable backup/recovery tooling, hand over the target, required recovery coverage and evidence gap to its owner; keep missing future capabilities out of runtime routes.

## Sources

At use time verify the installed-major [transaction command](https://www.postgresql.org/docs/current/sql-begin.html), [read-only limits](https://www.postgresql.org/docs/current/sql-set-transaction.html), [sequence behavior](https://www.postgresql.org/docs/current/functions-sequence.html), [EXPLAIN execution](https://www.postgresql.org/docs/current/sql-explain.html) and [locking guide](https://www.postgresql.org/docs/current/explicit-locking.html). For managed targets, verify branch/endpoint identity and supported recovery behavior in [Neon's official documentation](https://neon.com/docs/).
