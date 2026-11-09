# Resume from evidence

## File responsibilities

- **PLAN.md.** Current goal, scope, authority, work graph, owners, task states, budget, acceptance, open gaps, and next action; update it after an event is recorded.
- **LOG.md.** Append-only event history linking dispatch intent to receipt and terminal result; preserve measured usage, uncertain operations, cancellations, scope changes, and corrections.
- **DECISIONS.md.** Chosen and rejected alternatives, their evidence, decision authority, dissent, consequences, and reopening conditions.
- **briefs/.** Exact dispatched briefs by task and revision; a later clarification becomes a new revision or a linked event rather than an invisible replacement.
- **raw/.** Full task reports as received, one path per worker execution or round; coordinator summaries live separately and point back to these files.
- **drafts/.** Frozen draft versions with input/output identity, so a review can name the artifact it actually saw.

Store inspectable source evidence and concise reasons; private reasoning transcripts are not needed. Keep secrets out of briefs and shared logs, use appropriate access controls for private reports, and retain safe evidence pointers when a source cannot be copied into the run folder.

## Reconciliation sequence

1. Open the known run/checkpoint locator and identify its workspace, run identity, and authority from PLAN.md; read recent LOG.md events, relevant decisions, and requested linked continuation material. A missing locator needs scoped discovery; an unreadable, changed, malformed, or incomplete known checkpoint needs a specific gap and recovery action rather than a silent fallback.
2. Inspect the actual workspace and relevant changes without resetting, cleaning, or overwriting another owner's edits; compare the current revision with recorded input and output hashes.
3. Reconcile dispatch intents against returned host identities and its supported completion or recovery mechanism; a timeout or lost receipt does not prove that execution stopped.
4. If a live worker is still authoritative, preserve its slot and write boundary; if it is superseded, use the permitted cancellation mechanism and wait for confirmation before assigning a conflicting writer.
5. Inspect confirmed cancellation's partial outputs and effects; retain spent starts, retries, and usage, and record which artifacts may be reused.
6. Check each expected raw report for existence, substantive content, task identity, input revision, output identity, and the brief's return contract.
7. Reuse completed work whose evidence still applies; rerun only a changed or unproven acceptance condition, and record why prior evidence is insufficient.
8. Reconcile total starts, retries, review rounds, reserves, and active runs across providers, descendants, and eval sessions; neither a fresh coordinator nor a new finding resets counters.
9. Follow the material evidence pointers used for continuation and check their contents against the original acceptance condition. Preserve original human rulings and distinguish them from an agent summary or interpretation; a current artifact can contradict a historical completion claim.
10. Append a reconciliation event, update current state, and continue the first ready unmet acceptance condition. Reuse valid completed results; fresh context does not justify replaying investigations, resetting budget, or reopening settled choices without new evidence.

## Interpret gaps honestly

- **Intent without receipt.** Execution is uncertain; keep its reservation and reconcile with the host before another launch.
- **Receipt without report.** The task is active, failed, or missing evidence; host completion alone does not establish deliverable acceptance.
- **Report without receipt.** Preserve it as unverified evidence and establish provenance before using it as the contracted result.
- **Empty or malformed report.** Keep the gap visible and use only an allocated retry; an existing filename is not sufficient.
- **Report for an older snapshot.** Retain its history and identify which claims still apply; check changed acceptance conditions against the current revision.
- **Missing required slice.** Preserve the task even if all siblings succeeded; assign recovery or report unresolved scope explicitly.
- **Budget exhausted.** Record an unresolved result with evidence and next owner; agreement or a missing reply cannot satisfy acceptance.
- **User changed scope.** Append the requirement change, identify invalidated evidence and dependent tasks, and preserve unaffected completed work.

## Idempotent scaffolding

The scaffolder checks target collisions before writing and copies only missing PLAN.md, LOG.md, and DECISIONS.md templates. Rerunning it never refreshes those files from templates or resets task state. Empty raw, brief, and draft directories are storage locations rather than claims that any worker has run. It refuses symlinks at the run root or scaffold targets; it is a convenience tool, not a security sandbox for a hostile filesystem or simultaneous writers. After a write failure, inspect any partial new file before retrying; existing files are deliberately preserved rather than repaired silently.

## Checkpoint locator and evidence

Use the existing task-owned run path or the project's established run index; preserve exact paths/links and content identities in PLAN.md and LOG.md. This is a locator convention, not a new task scheduler, execution lock, hidden runtime-specific store, or second source of current state.

Publish a checkpoint through the existing records. The coordinator first appends a checkpoint intent to LOG.md with its identity and the preceding completed checkpoint's identity. Prepare changes to PLAN.md and any current-state decision document in temporary sibling files on the same filesystem; validate complete content and links before atomically replacing each destination. Preserve append-only events, corrections, immutable drafts and raw reports. Atomic file replacement prevents a partial write from truncating the previous record; it does not make several files one transaction.

After all necessary writes and readback succeed, append one complete checkpoint-ready event to LOG.md naming the checkpoint and the content identities it covers. That event is the completion marker, not a second store or controller. A crash, failed replacement, truncated event or intent without a matching ready event leaves publication incomplete. Reconcile the actual files and hashes before resuming; do not silently promote partial state or erase the preceding completed identity.

Reopen the checkpoint from the recorded locator and follow each requested artifact. Retain complete requested content and order; ten questions means all ten are reachable. Ensure the storage survives the anticipated interruption; otherwise state the limit and use an authorized durable destination. If a linked artifact changes, record the difference and evaluate which proof remains valid rather than silently accepting the old hash or overwriting its history.

Evidence fields contain precise pointers; command observations, interpretation, and reasons stay separate. Check that an anchor resolves and actually supports the claim. Append corrections with source pointers, preserving the original entry and unchanged raw reports. A missing pointer or unavailable transcript leaves an explicit gap, not an invented audit pass.
