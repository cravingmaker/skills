---
name: decision-log
description: Keep a durable run record with task state, dispatch receipts, raw reports, versioned drafts, and evidence-backed decisions. Use when agent work must survive compaction or when resuming a multi-agent run.
license: MIT
metadata:
  requires: "work-decomposition"
  source: "https://github.com/cursor/plugins/blob/6b0300214a09fd6029cfb7077043125758cd1fd2/pstack/skills/show-me-your-work/SKILL.md"
  source-revision: "6b0300214a09fd6029cfb7077043125758cd1fd2"
  source-files: "pstack/skills/show-me-your-work/SKILL.md"
  local-changes: "Merged evidence pointers, safe pause and known-run pickup into the existing PLAN/LOG/DECISIONS record; retained budgets and proof authority; imported no TSV ledger or storage controller."
---

# Decision log

Keep enough evidence on disk for a successor with no chat history to resume the next unmet acceptance condition. **Record** before dispatch, **Reconcile** before replay, and **Preserve** the original result.

## Scaffold or reuse the run

Preview the run folder first; use `--apply` to create missing records:

```sh
sh <skill-dir>/scripts/new-run.sh <run-dir>
sh <skill-dir>/scripts/new-run.sh --apply <run-dir>
```

The script uses POSIX shell and standard utilities, with no network or agent calls. Exit 0 means the preview or scaffold succeeded; 1 names a path conflict or write failure and its fix; 2 means usage. Reruns retain existing regular files, reject symlink or directory collisions at scaffold targets, and restore only missing templates. It creates PLAN.md, LOG.md, DECISIONS.md, and empty `briefs/`, `raw/`, and `drafts/` directories; it creates no worker result. The scaffold is intentionally unconfigured and is not evidence that work has run.

## Keep one recoverable record

1. **Locate.** Prefer the existing task-owned run folder and surrounding workflow conventions; use a new folder only when this is genuinely a new run. Designate one coordinator to update shared state; workers own unique briefed outputs and raw report paths. Done when every participant knows the run ID, coordinator, current plan revision, and report destination.
2. **Record.** Populate [assets/PLAN.md](assets/PLAN.md) with the goal, scope, authority, acceptance criteria, work graph, owners, finite budget, and next actions. Keep its current state consistent with the append-only event history in [assets/LOG.md](assets/LOG.md). Store choices and rejected alternatives with evidence through [assets/DECISIONS.md](assets/DECISIONS.md). When the plan delegates work, resolve the `work-decomposition` skill (required) through the installed inventory and read its SKILL.md. If it is unavailable, record the missing prerequisite and stop dispatch. Run its `scripts/check-plan.py` on PLAN.md with a supported interpreter; dispatch only after exit 0, and log the command, exit status, and output. Done when the next task, its dependency, write owner, allowance, and evidence gap can be found without chat history.
3. **Preserve.** Save every dispatched brief and full worker task report separately; retain raw reports unchanged and make summaries separate derived files with source pointers. Freeze draft revisions under new names with input/output hashes or commits using [assets/draft.md](assets/draft.md); never overwrite a draft already sent for review. Use [assets/report.md](assets/report.md) for a new report only when the brief supplies no stricter return format. Done when every result and verdict can be traced to the exact input and output snapshots.

## Keep evidence resolvable

PLAN.md owns current state, LOG.md owns append-only events and corrections, and DECISIONS.md owns choices and rejected alternatives. Keep their existing work graph and Proof producer/consumer contract authoritative; these content merges introduce no second TSV ledger or checkpoint controller.

An **Evidence** field or cell contains exact pointers: an artifact path and content hash, a source location, a host result/event link, or a path to a trace, screenshot, or saved command output. Put the claim, reason, command and observed result in their own fields rather than an evidence paragraph. A PR number or commit resolves an artifact identity but proves only what that artifact actually shows; it is not proof of testing, publication, or shipment.

At a checkpoint or handback, follow every material evidence pointer added or relied on in this run and check that its content supports the recorded claim. Compare available session/tool evidence with the actual decision trail, including pivots, rejected attempts and reverts; name unavailable ranges instead of claiming a transcript audit. Append a correction or missing event with its source rather than rewriting a false historical entry. A record with an unresolved or contradictory pointer remains an evidence gap.

## Record each operation and result

1. **Intent.** Before a dispatch, persist a stable request key, logical task, parent run, brief path/revision, provider/model settings, environment/base, write boundary, expected report, and budget reservation. Record the returned host task/run identity and receipt immediately after the call, or mark the receipt uncertain. A retry retrieves or reconciles that operation; a genuinely new execution receives a new operation identity and consumes its allocation. Done when a crash on either side of dispatch cannot justify an untracked duplicate launch.
2. **Result.** When a result arrives, append its status, raw path and hash, artifact revisions, actual commands/results, usage or `unknown`, and remaining gaps. Mark it reported first; acceptance requires source and integrated checks, through the `result-verification` skill where available. An absent, empty, malformed, stale, timed-out, or cancelled report remains an evidence gap; a missing report is not a result. Done when every dispatch has a receipt/result or an explicit unresolved recovery action, and no sibling's success hides missing work.
3. **Decision.** For each consequential choice, record its question, authority, constraints, alternatives, evidence, selected option, rejected alternatives and reasons, dissent, consequences, and revisit trigger. Keep finding IDs stable and distinguish accepted, rejected with evidence, superseded by scope change, and unresolved. Use the `agent-debate` skill for bounded disagreement when useful; agreement alone does not prove a claim. Done when a new coordinator can explain why the choice was made and what evidence would reopen it.
4. **Control.** Bound retries in the run budget before retrying; reconcile uncertain execution before dispatching replacements. Cancel superseded work through the host's supported facilities when permitted by the session, record the request and confirmation, and inspect partial edits and external effects before transferring ownership. If cancellation is prohibited or unconfirmed, retain its slot and boundary as unresolved and exclude its late output from the accepted result until reconciled. Done when no replacement can race an unresolved writer and no failed start disappears from spent resources.

## Pause safely when requested

A pause request stops new work at a safe boundary; "keep going" or compaction alone does not request a pause. Finish the current atomic operation or preserve its partial state without an irreversible action just to stop. Use the existing task authority for commits, pushes, publication, and cancellation; neither a WIP commit nor a PR is a default pause step.

1. Reconcile owned active or uncertain tasks through supported host facilities. Cancel only when permitted, record confirmation, and retain unresolved slots and write boundaries until effects are understood.
2. Append a checkpoint to LOG.md and update PLAN.md with exact run/workspace locators, current artifact identities, disk versus context-only state, valid proof, unresolved decisions, spent and remaining budget, and the first ready unmet condition. Save otherwise-lost necessary context in the existing record and keep secrets out.
3. Preserve requested questions, checklists, and continuation artifacts in the existing durable run location or the project's established durable storage. Link instead of creating competing copies; retain requested wording, completeness, and order.
4. Reopen the checkpoint using only the recorded project/run locator and follow its material links. Check requested content in full before calling it ready. State any retention or access limit; temporary-only storage cannot promise survival after deletion.

Done when a cold-start successor can reach the records and requested material, see active ownership and the unchanged budget, and take the next permitted action. A handoff note may point here; it never replaces these authoritative records.

## Resume through reconciliation

Follow [references/recovery.md](references/recovery.md) after compaction, a crash, an interrupted wait, or a changed coordinator.

1. **Read.** Open the supplied known run/checkpoint locator directly. Load PLAN.md, recent LOG.md events, DECISIONS.md, unresolved findings, and the referenced briefs, raw reports, draft revisions, and requested continuation artifacts. Diagnose a malformed, changed, inaccessible, or incomplete checkpoint rather than silently bypassing it. If the run locator is unknown, use the `recall` skill when installed to find it, then return here. Done when completed, active, uncertain, and unmet work are distinguished without relying on a compressed summary.
2. **Reconcile.** Inspect the actual workspace, relevant diffs, artifact existence and hashes, current authority, budget counters, and host task receipts through its supported recovery/completion flow. Preserve completed work; rerun only checks invalidated by changed inputs, a changed output, or a documented evidence gap. Done when every unexplained difference and uncertain dispatch has an owner and recovery action.
3. **Continue.** Reuse valid results, respect active write boundaries, and resume the first ready unmet acceptance condition. Record any scope or budget change with its authority; a new context window or replacement worker carries forward the original spent counters. Done when the next action neither duplicates completed work nor treats a missing report as success.

## Close or checkpoint

Record the integrated revision, acceptance evidence, unresolved findings and decisions, actual resource counts, unavailable measurements, remaining active work, and next owner. Complete already-authorized actions; checkpoint only an action whose authorization is unresolved. The `work-decomposition` skill sets the graph and budget, the `agent-briefing` skill prepares child contracts, and the `agent-orchestrator` skill coordinates the whole run when requested. Resolve a named skill through the installed inventory and read its SKILL.md before relying on it.

Done when the record accounts for every dispatch and result, preserves evidence and rejected alternatives, and supports safe continuation or verified closure without chat history. Research grounding and policy limits: [references/research-sources.md](references/research-sources.md). Adopted source files, hashes, destinations, and changes: [references/SOURCES.md](references/SOURCES.md).
