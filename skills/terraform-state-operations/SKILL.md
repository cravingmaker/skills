---
name: terraform-state-operations
description: Reconcile Terraform or OpenTofu state without accidental resource recreation. Use for resource moves/imports/removals, backend or engine migration, stale locks, and drift. Prepare a backed-up, serialized operation and prove recovery in a disposable target before a migration.
---

# Terraform state operations

Preserve resource identity and a recoverable state history. Prepare plans by default; a production mutation, state surgery or force-unlock needs explicit authorization for that operation.

For a saved plan's change verdict, read the `terraform-plan-review` skill when installed. General module design and host configuration convergence are separate jobs.

## Protect state first

1. Identify the authenticated account/project, region, engine/provider versions, backend object, workspace, state lineage/serial, and writer/lock owner. Record the requested operation and expected resource identities privately.
2. Before changing state, capture a restricted state backup through the engine/backend's supported mechanism. Verify the backup is readable in isolation, versioned and recoverable with the available keys; retain its hash and protected location, never its body.
3. Serialize all writers: local sessions, CI queues, scheduled drift jobs and remote runs. Inspect backend lock records and the owning run/process. Lock age alone does not prove that a writer has stopped.

Done when the target, backup, recovery dependency and exclusive writer are evidenced. A missing backup or uncertain writer blocks mutation.

## Choose the operation

Read [references/operation-checks.md](references/operation-checks.md) when performing any operation below; it gives branch-specific checks and recovery limits.

| Request | Preferred path | Required evidence |
| --- | --- | --- |
| Rename or reorganize addresses | Reviewable `moved` blocks; preserve instance keys and provider binding | Address mapping, no managed resource mutation, no unexpected output/drift change |
| Adopt an existing resource | Supported import blocks with exact remote ID and matching configuration | Import identity, no unintended update/create/delete/replace, second plan converges |
| Stop managing a resource | Supported `removed` block with explicit retain/destroy behavior | Exact retained object and new owner; intentional forgetting is separate from a pure refactor |
| Move backend or engine | Compatibility checks and disposable migration/restore rehearsal | Old/new identities, encryption keys, lock/writer interoperability, data and state recovery |
| Recover a stuck lock | Prove the owner has stopped, then a scoped authorized unlock | Lock ID, absent active writers, unchanged target and post-operation plan |
| Reconcile drift | Classify code change, authorized emergency change, provider difference or unexplained external change | Refresh observation and owner decision to adopt into code or revert through a reviewed plan |

## Verify refactors before applying

Write a protected expectation file with exact `moved` mappings and `imported` addresses, such as `{"moved":{"test.old":"test.new"},"imported":[]}`. Match every intended operation; keep identifiers out of shared evidence.

```sh
python3 <skill>/scripts/check-refactor-plan.py plan.json --expect expected.json
```

The read-only helper accepts managed no-op moves/imports and data-source reads, and checks the exact operation sets against the expectation. It rejects managed mutation, forgetting, output changes, drift, incomplete plans and deferred/unknown work that could hide a change. Exit 0 is a narrow refactor check, 1 findings, 2 invalid input. It does not verify remote import IDs or backup quality.

Review the exact moved/imported identities privately, including each instance key and provider alias. A move/import may make `plan -detailed-exitcode` return 2 before application; that code means a planned change, not an engine error. After the authorized operation, a fresh normal plan should return 0. Test the repository's wrapper with synthetic 0/1/2 exits before trusting that gate.

Do not apply the pure-refactor checker as a universal gate for intentional removal or drift correction. Those branches need a reviewed expected action set and the owner decision for each effect.

Done when the full action set matches the operation and the rehearsal proves both convergence and the promised recovery.

## Execute within scope and close

Immediately before a mutation, confirm account/project, region, backend/workspace, cluster if involved, state version and sole writer again. Use only the authorized operation; avoid routine `-target`, `-lock=false` and direct state edits. Never use `-auto-approve` outside an explicitly disposable target.

Afterward, check remote object identity, state lineage/serial, lock release, application/data assertions and a fresh plan. Reconcile partial operations before retrying. Restore only to the exact intended backend after proving no competing writer or intervening write; a stale state push can lose newer bindings.

Return operation, target, backup/rehearsal receipt, action evidence, authorization boundary, residual drift and owner. State restoration does not recreate destroyed resources or recover their data.

Done when the requested state operation is proved, or a concrete plan and blocked condition are ready for the owner. Read [references/sources.md](references/sources.md) when verifying current engine migration compatibility, S3 locking, block support, encryption or recovery commands; do not assume Terraform and OpenTofu remain interchangeable.
