# One budget for the whole run

The run's coordinator owns the allowance and is the only writer of its totals. An authorized child allocation is a reservation within those totals, with the same run ID and ledger path. The child sends dispatch intents and receipts to that coordinator before using the allocation; concurrent parents use an equivalent serialized reservation mechanism. When coordination cannot reserve a slot reliably, keep the child a leaf and dispatch through the coordinator.

## Count each resource separately

- **Worker starts.** Charge one for each child model execution, including a new worker, replacement, resumed child turn, reviewer, descendant, and each with-skill or without-skill eval arm; moving to another provider does not create capacity.
- **Retries.** Charge each repeated dispatch or failed operation being retried against its retry allowance; an actual new model execution also consumes a worker start.
- **Review rounds.** Charge each requested evaluation cycle against the run's round allowance; each participating model execution also consumes a worker start; a new finding retains the same run totals.
- **Concurrency.** Count every active subagent run across all routes, including a parent waiting on active descendants and separately launched model-powered eval sessions; keep an uncertain start counted until reconciled.
- **Reserve.** Hold the stated starts for integration or verification; use zero only when those activities are explicitly covered by direct work or another remaining allocation; record release of the reserve before its intended use.

Record per-finding round counts when using the `agent-debate` skill; they add a bound inside the run budget rather than replacing it. A supported host may apply stricter limits; the coordinator uses the smallest applicable ceiling. If other work shares the user's concurrency pool, reserve its active slots too or lower this run's available slots accordingly. Run-local arithmetic does not establish that the wider pool has room.

## Dispatch and reconciliation

1. Persist an intent with a stable request key, task, parent, purpose, brief revision, estimated charges, and the counters after reservation.
2. Check the live active count and every relevant allowance immediately before invoking the host; queue when full.
3. Persist the receipt and actual task/run identity; do not charge that same receipt again when an idempotent retry retrieves it.
4. If the host conclusively rejected execution, record that evidence and release the unspent start reservation; the retry still consumes its retry allowance.
5. If the receipt is missing or a wait times out, reconcile through the host's supported completion or recovery mechanism before dispatching a replacement; an uncertain execution retains its start and slot.
6. On completion or confirmed cancellation, release the active slot while retaining the start and resources already spent; inspect partial writes before transferring ownership.

This policy counts started executions and unresolved reservations; it does not manufacture provider usage receipts. Keep measured tokens, duration, and cost when available, and record `unknown` otherwise. Separate estimates from measurements and avoid adding child usage to a parent total that already includes it.

## Exhaustion and changes

At any exhausted limit, preserve the unmet acceptance condition, evidence, owner, and next decision. Report a partial or blocked result appropriate to the evidence; exhaustion cannot accept a result or erase a required task. Replacing a worker, changing providers, opening a finding, or resuming after compaction preserves spent counters. When a larger allowance is genuinely needed, record who has authority to change it and the explicit decision; a retry or task rename supplies no new authority. Keep prior limits in the log so the change remains reviewable.
