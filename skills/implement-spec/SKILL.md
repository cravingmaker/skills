---
name: implement-spec
description: Run an approved spec's tickets to an integrated, verified result, in dependency order, with one coordinator that owns every worker and reviewer start under a finite budget. Use when the user asks to implement a spec and its tickets, or the approved ticket graph from to-spec and to-tickets.
license: MIT
metadata:
  requires: "work-decomposition agent-briefing decision-log result-verification implement"
  source: "https://github.com/mattpocock/skills/blob/49dd158d1076134a641b33efb035946536778336/skills/engineering/implement-spec/SKILL.md"
  source-files: "skills/engineering/implement-spec/SKILL.md"
  source-revision: 49dd158d1076134a641b33efb035946536778336
  local-changes: "Made this the single approved-ticket runner on our run record, importer, briefs and verification; one coordinator owns every start under a finite budget of at most eight live subagents; leaves start no reviewers; bounded fix rounds; tickets close only on accepted worker and integration proof; merged Superpowers preflight, batching, report handling, review and resume methods; dropped model routing, extra controller scripts and workspace deletion."
---

# Implement spec

The goal is the entire approved spec implemented on one **integration branch**, every ticket accepted on evidence, and the tracker closed the way it closes work. The tickets are a **task graph** with blocking relationships, so there is always a **frontier** of tickets ready to start.

You are the **coordinator**. You alone start workers, reviewers, replacements and retries, and every start is charged to one budget. Workers are **leaves**: they implement and self-check; they never start reviewers or other agents. This skill is the only runner for approved code tickets; the `agent-orchestrator` skill routes such work here rather than running its own.

Communicate through **context pointers**: the spec, the tickets, research notes and commits, each with its revision. Do not paste what a pointer already holds.

## Before you start

Resolve each required skill (`work-decomposition`, `agent-briefing`, `decision-log`, `result-verification`, `implement`) through the installed inventory and read its SKILL.md. If one is missing, name it and stop.

Read the project's configured tracker and domain paths (for example `docs/agents/issue-tracker.md`). If the tracker contract is missing, say so; the `setup-agent-skills` skill creates it. Existing user authority for commits, pushes, PRs and tracker updates carries into the run; this skill adds none.

## Import command

Resolve `<work-decomposition-dir>` from the installed inventory and use the #5 read-only importer with the actual configured inputs:

```sh
python3 <work-decomposition-dir>/scripts/import-tickets.py <ticket-directory> --spec <approved-spec> --workspace <workspace> --run-id <run-id>
```

Resolve tracker and domain paths from the project's configuration; pass the exact approved spec explicitly with `--spec`. Success emits the source-bound graph on stdout; an invalid graph emits diagnostics without success JSON. Fill only the coordinator-owned execution overlays and pass that skill's plan checker before dispatch. For a hosted tracker, preserve the equivalent exact source bodies, native links and immutable receipts.

## Steps

1. **Import the approved graph.** Use the `work-decomposition` skill's ticket import on the exact approved spec and its tickets: stable ticket IDs, wording, status, acceptance checks, Proof lines and `Blocked by` lists, with the spec's path and hash. Do not decompose the spec again or rewrite tickets. An unresolved placeholder, an ambiguous blocker, a duplicate title match or a ticket without Proof stops the import; report it for the ticket owner to fix. Done when the imported graph matches the tracker exactly and every ticket has an owner-ready Proof.

2. **Record the run.** Reuse or scaffold the run record with the `decision-log` skill: the imported graph, spec hash, integration branch, ledger and next action. If a record for this spec already exists, resume from it: read [references/run-loop.md](references/run-loop.md#resume) first. Done when a successor with no chat history could resume from disk.

3. **Set the budget.** With the `work-decomposition` skill, record finite allowances before the first start: implementer starts, reviewer starts, fix rounds per ticket (three by default; declare any larger bound now), replacements, retries, optional exploration, and a reserve for the final review and integration checks. Live subagents never exceed eight or the lower host or user limit. Done when the budget is on disk and covers the whole graph plus the reserve.

4. **Pre-flight.** Scan the tickets once for conflicts: tickets that share a file or interface, a ticket that contradicts the spec or itself, and anything a ticket mandates that the review rubric treats as a defect. Write the table and your rulings to the run record; the spec is the binding authority. See [references/run-loop.md](references/run-loop.md#pre-flight). Done when every shared interface has a row and every conflict has a recorded ruling.

5. **Prepare the integration branch.** Create or reuse it with the host's checkout mechanism. If the tracker closes work through PRs, or the user asked for one, and opening a PR is authorized, open a draft PR after the first merge (a branch with no commits ahead of its base can't open one). Optional: one exploration worker, charged to the budget, saves notes outside the repo for later briefs. Done when the branch exists at a recorded base revision.

6. **Start the frontier.** For each ready ticket, pass the budget gate, then brief a worker with the `agent-briefing` skill by pointer: spec path and hash, ticket ID and Proof, accepted test seams, write boundary, base revision, its report path, and the leaf contract. The worker builds the ticket with the `implement` skill in its own host-isolated checkout based on the integration branch. Run tickets in parallel only when their write sets are disjoint; serialize shared files, schemas, lockfiles and live resources. Batch several small same-shape edits into one worker. Read [references/briefs.md](references/briefs.md) for the worker contract. Done when every started ticket has a recorded dispatch, base revision and report path.

7. **Take each report.** Save it raw, then accept or reject with the `result-verification` skill: outputs at the stated revision, write boundary, a rerun of the Proof on the worker's artifact, and the status. PARTIAL, BLOCKED, missing or stale proof stays unresolved. A blocked worker needs something to change (context, capability, a smaller ticket, or a ruling) before a retry; never retry it unchanged. See [references/run-loop.md](references/run-loop.md#reports). Done when each report has a recorded decision.

8. **Review.** When a ticket's risk warrants an independent review, reserve one reviewer from the budget and brief it with the `change-review` skill's rubric over the ticket's exact range: spec compliance and quality, with file:line evidence. Findings keep stable IDs. Doing the review inline is fine when independence is optional; record it as a coordinator review, never as an independent one. A requested provider that is unavailable is reported, not replaced. See [references/briefs.md](references/briefs.md#reviewer). Done when the ticket has a review result, or a recorded reason none was needed.

9. **Fix within the round limit.** Send open Critical and Important findings back to the same worker when the host can resume it, otherwise to a fresh worker with the report path. Each round ends with a scoped re-review of the fix range. At the limit, rule on each open finding: park it with a reason, or keep it open as unresolved. A ticket with an unresolved Critical or Important finding is not accepted. Minor findings go to the run record for the final review. See [references/run-loop.md](references/run-loop.md#fix-loop). Done when every finding is addressed, parked with a ruling, or carried as unresolved.

10. **Merge and advance.** Merge each accepted ticket into the integration branch, rerun the checks its Proof names on the integrated revision, and record the result. If the frontier grows, return to step 6. Done when every ticket is merged and accepted, or unresolved with its reason.

11. **Accept the whole.** Run every acceptance check on the final integrated revision with the `result-verification` skill. Reserve one whole-branch review with the `change-review` skill; send all its findings to one fix worker, then one scoped re-review. Close a tracker item, or mark the draft PR ready, only when its ticket and the integration evidence are accepted and the action is authorized. Done when the integration evidence and every tracker update are recorded.

12. **Clean up and report.** Remove only the checkouts and branches this run created and no longer needs; keep the run record. Lead the report with the outcome, then: per-ticket state, the integration revision and its checks, every ruling with what it costs if wrong, deferred minors, unresolved items and the decision each needs, and budget used against limits.

## Stops

Stop and ask only when a required action lacks existing authority, including an irreversible, destructive, security-sensitive or outward-facing action, or when the graph is so broken that every path forward is a guess. Reuse explicit authority already granted for the same action and scope; do not request it again. Decide everything else, record the ruling, and continue. Budget exhaustion is a stop with unresolved work, never an approval.

## Provenance

Adapted from Matt Pocock's implement-spec skill, with methods from Superpowers' subagent-driven-development. See [references/SOURCES.md](references/SOURCES.md), `LICENSE-mattpocock` and `LICENSE-superpowers`.
