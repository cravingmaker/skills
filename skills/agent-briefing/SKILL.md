---
name: agent-briefing
description: Write a self-contained task brief for a fresh agent, with skills, permissions, evidence, and a return contract. Use when preparing a delegation or repairing a brief that depends on missing history.
license: MIT
metadata:
  source: "https://github.com/cursor/plugins/blob/6b0300214a09fd6029cfb7077043125758cd1fd2/pstack/skills/principle-guard-the-context-window/SKILL.md"
  source-revision: "6b0300214a09fd6029cfb7077043125758cd1fd2"
  source-files: "pstack/skills/principle-guard-the-context-window/SKILL.md"
  local-changes: "Kept the owned run/brief contract; adapted only the planned portable methods, exact input pointers and named Proof; removed upstream controllers, mandatory dispatch and host-specific rules."
---

# Agent briefing

Deliver a **Standalone** brief: a fresh worker can act from it and the named artifacts without the parent's chat. **Boundary** defines authority; **Evidence** defines what the worker must return.

## Check the brief

Start from [assets/brief.md](assets/brief.md), populate its fields, and run:

```sh
python3 <skill-dir>/scripts/check-brief.py <run-dir>/briefs/<task>-r1.md
```

Python 3.12 or later is required; no packages are needed. Find `python3.12` or a newer versioned interpreter on PATH; if `python3` is older, use that interpreter or `uv run --python 3.12` before the script path. Exit 0 means required sections and structured contract lines are present; 1 names every missing field, placeholder, or malformed allocation; 2 means usage or unreadable input. Use explicit `none` with a reason where a field does not apply, and keep the template's field names. The checker reads without writing; it cannot establish whether permission is real, a path is usable by the child, a skill was loaded, or the content supplies enough context. Read [references/brief-checks.md](references/brief-checks.md) when changing the format or investigating a rejected brief.

## Prepare the contract

1. **Discover.** Read the current host's tool descriptions and session instructions before selecting a dispatch route. Establish the supported provider/model settings, actual environment and checkout base, available skills, tool restrictions, completion flow, and cancellation mechanism. Use runtime discovery as offered by the host; keep a requested model or setting, and report an unavailable route rather than substituting one silently. Done when the chosen worker can reach the specified artifacts and the requested execution route is supported.
2. **Standalone.** State the goal and why it matters, included and excluded scope, constraints, terminology, prior decisions, unresolved decisions and their owners, dependencies, and acceptance criteria. Name authoritative files with revisions or hashes; transfer required uncommitted inputs explicitly if the child would otherwise see another snapshot. Keep necessary facts inline and link large artifacts at paths usable in the child's environment. For an approved spec or ticket, use its exact path and SHA-256 rather than restating its body. Add only missing authority, literal write/resource boundaries, named Proof, agreed testing seams, budget, and return obligations. Require the worker to compare the hashes before work; a missing or changed input leaves the dependent work unresolved. Read only the relevant sections and linked artifacts, sizing the task to its finite allowance; context pressure alone does not authorize delegation. Remove phrases such as "as discussed" by supplying the actual fact or artifact. Done when the task can be executed without reconstructing conversation history or inventing a shared decision.
3. **Skills.** Select the specific capability skills to load by the deliverable. Give advertised installed paths when known; otherwise direct the child to resolve names through its installed inventory and read each SKILL.md before relying on it. Use explicit `none` with a reason for a bounded task needing no extra capability. Require the return report to state which skills actually loaded and any missing prerequisite; a missing required skill stops that dependent flow. Done when skill loading is an explicit action in the brief rather than an assumption about inheritance.

## Set authority and communication

1. **Boundary.** Declare read access, allowed writes, owned paths, forbidden paths, external actions, and the only report-writing exception for a repository reader. Pass the user's existing authorization accurately; worker agreement or skill activation cannot grant new authority. Prefer enforceable host restrictions where available, then inspect the actual state on return; a prompt saying read-only is not a sandbox. Give each worker one unique raw report path and keep shared logs with the coordinator. Done when every permitted mutation is within the parent task and every writer has a disjoint boundary or explicit dependency ordering.
2. **Communication.** Embed the standing contract in every brief, including when the child can load the `clear-communication` skill. Use the Communication block in the template: result first, enough words to act correctly, faithful facts, plain concrete wording, inspection before consequential questions, batched answerable questions, reversible stated assumptions, and focus on the uncertain part. Preserve stricter applicable user/session instructions. Done when a worker without any inherited communication rules receives the contract in its own brief.
3. **Budget.** Make the worker a leaf by default and state its bounded stopping condition. If it may delegate, include the coordinator's shared ledger path and allocated worker starts, retries, review rounds, and concurrency ceiling; all descendants and eval arms consume that same allocation. Use the `work-decomposition` skill when the task graph or allowance needs to be set; resolving and reading that skill precedes relying on it. Done when the worker knows what it may spend, how to reserve a shared slot, and how to return an unresolved result at a limit.

## Require inspectable results

1. **Evidence.** Specify required commands, source standards, versions, and observable acceptance conditions, including the plan or ticket's named Proof. The worker drives that surface or opens that source on its exact artifact and records the actual observation, input hashes, command or locator, environment, and evidence identity. A proxy check, stale artifact, or unavailable observation remains unresolved. Distinguish executed results, static demonstrations, and unresolved hypotheses; require the command and observed result for a claim that a check passed. Ask for sources and concise reasons, not private reasoning transcripts. Done when each acceptance claim has a defined way to verify it and unavailable environments remain visible.
2. **Return.** Require result first with COMPLETE, PARTIAL, or BLOCKED; evidence including the actual named Proof result and limits; artifact paths and exact revisions or content hashes; commands and results; unresolved claims; decisions needed; assumptions and surprises; and measured usage or `unknown`. Require an uncondensed task report at the raw report path and a short completion pointer in the host response. Preserve a child's task report separately from coordinator summaries; apply the `result-verification` skill when accepting and integrating its claims. Done when the worker's output can be checked against the exact input snapshot and no missing result can pass as completion.
3. **Dispatch.** Run the checker, then inspect the content against the actual task, host, authority, and write map. Freeze this brief's revision, record the dispatch intent through the `decision-log` skill or existing run record, and invoke the host only after the shared budget gate passes. Done when the worker receives this exact brief and the coordinator records its receipt or explicit dispatch uncertainty.

Done when the brief passes, a fresh worker has every required fact or accessible pointer, and its write boundary, skills, budget, evidence, and return obligations are explicit. The `agent-orchestrator` skill owns whole-run coordination when requested. Research grounding and policy limits: [references/policy-sources.md](references/policy-sources.md).

Per-file attribution: [references/SOURCES.md](references/SOURCES.md).
