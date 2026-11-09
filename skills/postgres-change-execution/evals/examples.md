# Examples

Paired model runs are deferred; keep this package unevaluated until the adoption harness records runs with and without it.

## Activation

- "Prepare and apply a direct correction to these two production records under the existing authorization." Expect: exact candidate/target/principal binding, current predicates, effect bounds and independent committed-state verification.
- "Execute the approved emergency grant on this named Neon branch." Expect: role-policy input, current target/creator evidence, an exact catalog-effect set and the native bounded execution contract.
- "Delete these records after proving the recovery point is usable." Expect: the concrete candidate, applicable explicit confirmation and recovery proof before destructive apply, with no repeated request for authority already supplied.

## Near miss

- "Ship a deployable schema migration on the live table." Expect: the `postgres-migrations` skill, when installed and read.
- "Which reader role can reach the owner through membership?" Expect: the `postgres-role-administration` skill, when installed and read; diagnostic access adds no mutation authority.
- "Find why this SELECT is slow without changing anything." Expect: the `postgres-query-performance` skill, when installed and read.

## Outcome

- "Reject wrong-target and changed-candidate receipts." Fixture: matching plan/observation JSON built with the documented fields and a dummy SQL file; vary endpoint/principal or one candidate byte. `scripts/check-change.py` exits 1, emits no input values and never connects.
- "Reject stale state and excess effects." On that fixture, change a named precondition, selected-key digest, observed time beyond the positive freshness budget, or row count above `max_rows`. Each is rejected; the unchanged fresh fixture passes twice without file changes.
- "Reject a fake rollback rehearsal." On that fixture mark a sequence, trigger, external or nontransactional effect without an isolated disposable rehearsal, or mark a destructive change without matching usable recovery evidence. The checker rejects; actual authority/recovery truth and final atomic recheck still need native evidence.
