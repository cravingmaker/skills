# Decision log examples

Run each prompt with and without this skill in fresh, separately restored fixtures; keep tools, model settings, dependencies, and communication rules constant. Verify treatment availability and baseline absence through every enabled discovery source; reject an unproven comparison. Record prompts, input and skill revisions, inventories, host/model versions, traces, artifacts, observed recovery, and coordination cost before marking this skill evaluated. Charge each model-powered arm against the shared delegation budget and concurrency pool.

## Activation

- "Keep a run record for these workers so another agent can resume after compaction." Expect: durable current state, dispatch intents and receipts, raw reports, and decisions.
- "Resume this multi-agent migration run without repeating finished work." Expect: workspace and host reconciliation before further dispatch.

## Near miss

- "Write an architecture decision record explaining our cache choice." Expect: domain-modeling or architecture writing, without a fleet scaffold.
- "Fix this one typo." Expect: direct execution without run bookkeeping.
- "Summarize the decisions in this pasted meeting note." Expect: a direct summary unless a durable agent run is requested.

## Outcome

- **Scaffold.** Preview creates no files; apply creates the three records and empty storage directories; applying twice preserves edited records byte for byte; a conflicting target fails before copying any template.
- **Dispatch recovery.** A simulated crash after dispatch but before receipt leaves an uncertain operation; the successor reconciles the host rather than launching a duplicate, retains the reservation, and records the recovered identity.
- **No replay.** A valid completed report and unchanged output are reused after compaction; a missing report remains a required gap, even when its sibling completed.
- **Traceability.** Every result names its input revision and raw report; a summary never replaces the original; a changed draft receives a new filename and a review cannot silently move to another hash.
- **Decisions.** Rejected alternatives retain their evidence and reasons, unresolved dissent has an owner, and exhausted retries or review rounds leave an unresolved result.
- **Cancellation.** A superseded writer's boundary is reassigned only after permitted cancellation is confirmed and partial effects are inspected; if cancellation is forbidden, the unresolved slot and ownership remain visible.
