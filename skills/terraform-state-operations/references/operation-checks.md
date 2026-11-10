# Operation checks

Read this when selecting a state operation or checking its recovery plan.

## Refactor and import

Build a complete old-address → new-address/remote-ID mapping in a protected artifact, including module instances and provider aliases. Prefer supported declarative blocks so the operation is reviewable and replayable. Preserve move history while independently deployed callers still need it. Stable `for_each` keys prevent list-index shifts; do not change keys as an incidental refactor.

Use configuration matching the imported remote object; an import followed by an update is a change requiring its own review. Check remote account, region and object identity before any binding. Do not import the same object into two independently managed addresses/states. Intentional removal from management needs an explicit retain/destroy choice and a new owner; it is not a pure refactor.

`scripts/check-refactor-plan.py` runs on Python 3.12+ standard library, reads a local major-format-1 plan JSON and writes nothing. JSON findings/counts/digest go to stdout; fixed diagnostics go to stderr. Exits: 0 narrow check passed, 1 findings, 2 unusable input. `--help` exits 0 without reading inputs.

Managed actions must be no-op, possibly with `previous_address` or `importing`. Data reads are accepted only when no unknown mask remains. Managed updates, creates, deletes, replacements, forgetting, changed outputs, drift, deferred/incomplete work and nonpassing checks fail. The helper exposes only row numbers and counts, not addresses, IDs, outputs or state values. Import counts do not prove correct remote identity.

Use `--expect expected.json` with `{"moved":{"old.address":"new.address"},"imported":["existing.address"]}` to reject missing, changed or unexpected operations. Empty sets require no moves/imports. Duplicate or malformed expectations are unusable input; the output includes the expectation's digest without its identifiers. Without the option, exit 0 checks effects only, not intended identities.

For a cross-state handoff, freeze both writers and match a supported retain/removal in the source with an import in the destination. Prove the remote object identity and the sequence that prevents concurrent management or an unowned object; intentional source removal uses its own reviewed effect set.

After an authorized operation, a normal refreshed plan must converge; check the engine's detailed exit semantics live. A pre-operation move/import plan can legitimately report changes, even without remote mutation.

## Backend migration

Inventory every writer and its engine/backend versions. Confirm destination encryption, access control, object identity, version history and locking. S3 lockfile/DynamoDB compatibility must be checked against the installed clients and current backend docs before removing the old lock mechanism. Two client populations using unrelated locks can write concurrently.

Rehearse with a disposable state/backend and no production credentials. Snapshot, migrate using the installed engine's documented workflow, verify lineage/serial and remote-object bindings, run a second plan, then restore and verify the old path. Record cleanup separately. Do not edit backend config and assume state moved; reconfiguration and migration have different effects.

## Engine migration

Check source and destination engines, state format/encryption, provider addresses/checksums, backend locks and unsupported language/provider features against their official migration docs. Prove that decryption keys exist independently of the encrypted state. Rehearse the exact direction with a protected backup and disposable target, including failure and restore. A successful migration does not imply that downgrading or switching back is supported; preserve a tested recovery path before the first destination write.

## Stuck lock

Correlate the lock ID and owner with local processes, CI jobs and remote runs. Stop or finish the owner through its normal control path within authority. Prove no writer remains; never infer that from an old timestamp or an empty job list alone. Force-unlock only the exact lock and target explicitly authorized. Preserve the backup and re-plan after unlocking before any apply.

## Drift

Keep read observations distinct from mutation. A refresh-only plan shows changed remote observations; accepting that plan changes state. A normal plan may propose undoing an emergency remote change. Classify every difference and obtain the owner's adopt/revert decision before reconciling. An unexplained security-relevant change needs incident/security handling, not silent refresh.

For scheduled detection, preserve detailed exit codes: 0 no change, 1 engine/infrastructure error, 2 detected changes. Alert on both 1 and 2 with distinct ownership; avoid printing plan bodies. Neither an empty scan nor a refresh-only apply proves application health.

## Recovery receipt

Record operation/authorization, source and destination identities, backup hash/location/key access, sole-writer proof, rehearsal results, expected effects, exact private plan identity, post-operation remote/state checks, fresh plan, application/data assertions and residual drift. Never restore a stale backup over a newer writer. State history is metadata recovery; deleted data needs independent service backups and restore evidence.
