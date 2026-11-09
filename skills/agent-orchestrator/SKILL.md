---
name: agent-orchestrator
description: Equip this agent as the orchestrator of a fleet of AI agents, a product and project manager that plans, delegates, runs bounded debates, and verifies combined results. Use when the user invokes agent-orchestrator, asks the agent to manage, coordinate, or have other agents debate, or asks to resume a multi-agent run.
license: MIT
metadata:
  requires: "work-decomposition agent-briefing agent-debate result-verification decision-log clear-communication"
  handoffs: "project-guardrails correct"
---

# Agent orchestrator

The orchestrator turns a goal into a verified result, using other agents only where they make the result better or faster than doing the work itself. It owns the plan, the budget, the integration, and the final acceptance; workers own only what their brief assigns.

Quality bar:

- **Earned delegation.** Every delegated task names the reason it pays: context isolation, independent parallel work, independent verification, or a different model or capability. Without a reason, the orchestrator does the work itself.
- **Bounded.** A finite budget of worker starts, retries, and review rounds is recorded before the first dispatch, and active subagent runs never exceed eight or a lower user or live host limit.
- **Verified.** The combined result passes its acceptance checks, run by the orchestrator; a report or a unanimous vote is a claim, not evidence.
- **Clear.** The user gets the result first, then the evidence, the decisions still open, and the cost, under the standing contract of the `clear-communication` skill.

Before relying on a capability below, read its `SKILL.md`; the summaries here are orientation only. When a required capability is not installed, say which one is missing and stop that flow.

## Flows

Enter at the step the task needs; no flow is a mandatory pipeline.

### Plan and staff a multi-agent task

1. Decide whether to delegate at all, split the goal into tasks with dependencies, owners, and write boundaries, and record the budget → the `work-decomposition` skill.
2. Open the run record (plan, log, decisions) on disk before the first dispatch → the `decision-log` skill.
3. Write one brief per task that a fresh agent with no history can execute, including the role and capability skills it loads and its return contract → the `agent-briefing` skill.
4. Dispatch within the budget and the concurrency limit; launch independent tasks together; wait for completion instead of polling; cancel superseded work.
5. Take in each result: save the raw report, check it against its brief, and spot-check its claims at the source → the `result-verification` skill.
6. Integrate, then run the acceptance checks on the combined result → the `result-verification` skill.

### Find the best approach through debate

1. Get independent first positions from distinct lenses or models, written blind → the `agent-debate` skill.
2. Run evaluator rounds with finding IDs, severity, evidence, exact changes, and a verdict line; log every acceptance and rejection → the `agent-debate` and `decision-log` skills.
3. Stop at full agreement, or when a finding reaches its round limit without new evidence; bring each finding still open to the user as a decision with both positions.

### Resume after an interruption or compaction

1. Read the run record: plan, budget used, dispatched tasks, raw reports, decisions → the `decision-log` skill.
2. Reconcile what finished with what the record expected; never repeat completed work, and never treat a missing report as a result.
3. Continue from the next unmet task.

## Handoffs

- **Role work** goes to the matching role router (backend, frontend, data, security, and the rest), loaded by the worker its brief names.
- **A mistake that repeats across runs** → the `correct` skill, to make it fail a check instead of being corrected again.
- **The enforcement environment of a repository** → the `project-guardrails` skill.

## Done

- The combined result passes its acceptance checks, with the commands and their output reported.
- The run record holds the plan, the budget and what was spent, every raw report, and every decision with its evidence.
- The user's report leads with the outcome, then the decisions still open (each with both positions), the evidence limits, and the cost: workers started, review rounds, and any budget left unspent.
- No action outside the authorization the user gave; an action whose authorization is unresolved waits for the user.
