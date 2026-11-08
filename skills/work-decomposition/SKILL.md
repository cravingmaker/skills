---
name: work-decomposition
description: Decide whether delegation earns its cost, then map tasks, dependencies, ownership, and a finite run budget. Use when planning work across agents or deciding whether a complex task should be split.
license: MIT
metadata:
  source: "https://github.com/mattpocock/skills/blob/49dd158d1076134a641b33efb035946536778336/skills/in-progress/loop-me/SKILL.md"
  source-revision: "49dd158d1076134a641b33efb035946536778336"
  source-files: "skills/in-progress/loop-me/SKILL.md"
  local-changes: "Kept the owned run/brief contract; adapted only the planned portable methods, exact input pointers and named Proof; removed upstream controllers, mandatory dispatch and host-specific rules."
  requires: "decision-log"
---

# Work decomposition

Deliver the smallest work graph that can meet the user's acceptance criteria within a finite budget. **Direct** is the default; **Owner**, **Order**, and **Budget** govern any delegation.

## Check the plan

Before dispatch, run the checker against the plan's JSON object or its single fenced JSON block:

```sh
python3 <skill-dir>/scripts/check-plan.py <run-dir>/PLAN.md
```

Python 3.12 or later is required; no packages are needed. Exit 0 means the recorded owners, proofs, reasons, dependency graph, literal write paths, and budget pass, with no unresolved `{{placeholder}}`; 1 names findings and fixes; 2 means usage or unreadable input. The checker compares every pair of unordered tasks, even when their owner names match, and resolves existing local symlink aliases. It cannot discover undeclared writes, enforce live host limits, establish authorization, or judge whether a delegation is useful. Read [references/plan-format.md](references/plan-format.md) when creating or changing the checked block.

## Import approved tickets

Approved tickets are the task graph: import their identities, titles, status, acceptance, blockers, and Proof without another decomposition. The caller resolves the ticket directory and exact approved spec from its configured tracker and domain locations; the importer reads the paths passed to it, not freeform project configuration. Project-facing flows use `docs/agents/issue-tracker.md` and `docs/agents/domain.md` when those are their configured contracts. Missing setup never imposes a ritual on generic planning: obtain the actual input paths, or name the `setup-agent-skills` skill when project setup is the requested fix.

```sh
python3 <skill-dir>/scripts/import-tickets.py <ticket-directory> --spec <approved-spec> --workspace <workspace> --run-id <run-id>
```

The read-only importer prints success JSON for PLAN.md from local `NN-slug.md` files. Each ticket needs its title, Status, acceptance checkboxes, non-empty Proof, and Blocked by. It binds the exact ticket bytes and spec by SHA-256, preserving status spelling and Proof text. Tickets marked `done`, `closed`, or `resolved` satisfy their dependents and leave the active task list. No Proof is invented: a missing, blank, or placeholder Proof rejects the ticket before JSON is printed.

Use comma-separated ticket numbers or `None`, as the `to-tickets` skill's template specifies. Legacy input also accepts `#01`, `ticket 01`, exact unique titles, matching `01: Title` labels, list items, and semicolon or `and` separators; every token must resolve. Ambiguous titles, unknown or duplicate blockers, self-blockers, and active cycles fail. Comments and fenced examples do not supply ticket fields or acceptance.

Owners, reasons, write paths, outputs, shared resources, and the budget remain coordinator-owned placeholders; the plan checker rejects them until resolved. Exit 0 prints the plan on stdout; 1 lists ticket findings on stderr; 2 reports usage or unreadable input on stderr. The sibling `spec.md` fallback is only for a caller whose configured layout uses it; pass `--spec` for the actual approved input. The importer writes nothing and makes no network request.

Keep approved wording and graph edges. An execution dependency needed to separate writers is a logged overlay; merging, splitting, or rewording approved tickets needs authority. For a hosted tracker, construct the same shape from the exact issue bodies, stable IDs, status, native blocking links, acceptance and Proof, binding exported source bytes or immutable receipts. Read the `to-tickets` skill only when an approved decomposition is actually missing; installation preference supplies no new authority.

## Choose direct work or delegation

1. **Inspect.** Read the goal, existing work, acceptance criteria, current workspace, and session rules before proposing workers. Done when each required outcome and the authority to delegate are known; tool availability alone supplies neither.
2. **Direct.** Keep tightly coupled edits, a shared diagnosis, and sequential phases with the current owner when another agent adds no useful separation. Delegate only for **context isolation**, **independent parallel work**, **independent verification**, or **a different capability**, including an authorized model with a useful different lens. Name the specific benefit and the cost of briefing, duplicated reading, checking, and integration; different job titles alone supply no benefit. Honor an explicit delegation request within its authorized settings and budget, and record which of these purposes it serves. Done when every proposed child has a concrete reason, or the work proceeds directly without a team.

## Assign ownership and order

1. **Record.** Resolve the `decision-log` skill (required) through the installed inventory and read its SKILL.md; if it is missing, report the prerequisite and stop this delegation flow. Reuse the existing run record or scaffold one through that skill. Done when one coordinator can recover the plan and its budget from disk.
2. **Owner.** Give every task one owner, inputs with revisions, outputs, acceptance checks, named Proof (the surface to drive or source to open, and result to observe), dependencies, literal write paths, and shared mutable resources. Include each worker's unique raw report path in its write boundary, even for a repository reader. Appoint one integration owner for the final artifact and cross-component checks. Done when every required outcome has an accountable task and every mutable resource has one writer at a time.
3. **Order.** Each dependency names the artifact or decision needed before the successor starts. Set shared interfaces before fan-out. Separate independent owners and artifacts before adding serialization; where sharing is real, enforce one writer or an explicit lock/dependency. Serialize tasks that share a schema, lockfile, generated output, browser session, database, port, or external resource. Parallel writers own disjoint paths; separate checkouts still need a single owner for each path in the integrated result. When two proposals need the same eventual file, give them separate draft paths and let the integration owner apply one result later. Done when tasks without dependency ordering can run independently and the checker reports no overlapping writers.

Read [the planning methods](references/planning-methods.md) when a recurring workflow, a risky unknown, interface constraints, or workspace isolation needs an execution overlay. Reuse approved slices and the one run record; these methods do not produce another spec, ticket graph, or runner.

## Allocate and account for the budget

1. **Budget.** Copy [assets/budget.md](assets/budget.md) into the run record and choose finite allowances before the first dispatch. Record total worker starts, retries, review rounds, a concurrency ceiling, and a reserve plan for integration and verification. Eight concurrent subagent runs is this fleet's hard ceiling; use the smaller user or live host limit, and start fewer when the work needs fewer. Zero worker starts is valid for direct work. Done when the recorded limits cover the planned work and leave capacity for checking the combined result.
2. **Account.** One coordinator charges every provider, descendant, replacement, reviewer, resumed child execution, and model-powered eval arm to the same ledger. Workers remain leaves unless their briefs explicitly allocate further work from that ledger; an allocation reserves part of the parent's allowance rather than creating a new budget. Count failed and cancelled execution already spent; keep uncertain dispatches reserved and active until reconciled. A new finding, renamed task, or replacement worker carries forward the same counters. Read [references/accounting.md](references/accounting.md) for start, retry, round, reserve, and unknown-usage rules. Done when the shared counts include every outstanding or spent run without counting the same receipt twice.
3. **Gate.** Immediately before each launch or retry, check dependencies, authorization, remaining allowances, reserve, and active slots; record the dispatch intent before invoking the host. Use host enforcement where available and queue the next run when any limit would be exceeded. A completed parent turn whose descendants are active still occupies the relevant run's slot. At exhaustion, retain the incomplete task and report its evidence and next decision as unresolved; a cap supplies no approval. Done when no launch can escape the shared accounting and the plan checker passes again.

## Hand off

Use the `agent-briefing` skill for self-contained child contracts, the `agent-debate` skill for a bounded disagreement, and the `result-verification` skill for executed acceptance on the integrated revision. The `agent-orchestrator` skill coordinates the whole run when that role is requested. Resolve a named handoff through the installed inventory and read its SKILL.md before using it. Carry forward existing authorization; checkpoint only the action whose authorization remains unresolved.

Done when each task is direct or justified, owners and write boundaries are clear, the graph passes, the finite budget is recorded, and the next ready work is identifiable. Report a direct decision or the graph path, critical dependency, limits and remaining capacity, and any unresolved scope or evidence gap. Research grounding and the limits of these local policies: [references/policy-sources.md](references/policy-sources.md).

Per-file attribution: [references/SOURCES.md](references/SOURCES.md).
