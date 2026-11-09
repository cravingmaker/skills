---
name: agent-orchestrator
description: "Coordinate a multi-agent run: plan, delegate, debate, and verify combined results. Use when asked to act as agent-orchestrator, manage agents, or pick up an earlier agent run and finish it; resume from its durable record."
license: MIT
metadata:
  source: "https://github.com/mattpocock/skills/blob/49dd158d1076134a641b33efb035946536778336/skills/engineering/ask-matt/SKILL.md"
  source-revision: "49dd158d1076134a641b33efb035946536778336"
  source-files: "skills/engineering/ask-matt/SKILL.md"
  local-changes: "Merged the shaping stage map into the owned orchestrator; reuse settled inputs and current authority; merged stage selection, coverage/competing-attempt modes and bounded recovery; routed approved code tickets to implement-spec under the same coordinator, record and budget; added owned design/review dispatch without a competing runner; added owned shipping modes, root-only authorized watching and retrospective routing."
  requires: "work-decomposition agent-briefing agent-debate result-verification decision-log clear-communication grill-with-docs to-spec to-tickets implement-spec retro"
---

# Agent orchestrator

The orchestrator turns a goal into a verified result, using other agents only where they make the result better or faster than doing the work itself. It owns the plan, the budget, the integration, and the final acceptance; workers own only what their brief assigns.

Quality bar:

- **Earned delegation.** Every delegated task names the reason it pays: context isolation, independent parallel work, independent verification, or a different model or capability. Without a reason, the orchestrator does the work itself.
- **Bounded.** A finite budget of worker starts, retries, and review rounds is recorded before the first dispatch, and active subagent runs never exceed eight or a lower user or live host limit.
- **Verified.** The combined result passes its acceptance checks, run by the orchestrator; a report or a unanimous vote is a claim, not evidence.
- **Clear.** The user gets the result first, then the evidence, the decisions still open, and the cost, under the standing contract of the `clear-communication` skill.

Before relying on a capability below, resolve its installed entry and read its `SKILL.md`; the summaries here are orientation only. Confirm absence in the complete installed inventory, including entries selected only by explicit invocation, before reporting a required capability as missing. An omitted automatic suggestion is not evidence of absence. When absence is confirmed, name the missing capability and stop that flow.

## Flows

Enter at the step the task needs; no flow is a mandatory pipeline.

### Shape an idea into approved tickets

1. Reuse the conversation, configured domain paths, accepted ADRs, and prior decisions. Fill only unresolved consequential design gaps with the `grill-with-docs` skill when recording domain changes is authorized; otherwise use the `grilling` skill for a plain interview. Skip another interview when the understanding is already settled.
2. Write the agreed understanding as a spec with bound inputs, acceptance, and named Proof through the `to-spec` skill. Preserve draft-only or other existing task limits.
3. Turn the approved spec into stable vertical slices through the `to-tickets` skill. Keep ticket identities, blockers, acceptance and Proof; an approved breakdown is not decomposed again.
4. Return the approved artifacts, or continue authorized code-ticket execution through the `implement-spec` skill below. Shaping creates no implementation or external-action authority.

### Build from an approved spec and code tickets

Read the `implement-spec` skill and use it as the single approved-code-ticket runner. Resolve the exact approved spec, ticket source and closure rules from the configured tracker contract, and the configured domain paths; preserve lazy absent glossary or ADR files. Import stable IDs, status, blockers, source hashes and named Proof through the `work-decomposition` skill without a second interview or decomposition.

When required dispatch or host-owned isolation is unavailable, keep this flow at source-bound preflight and report worker execution and integrated acceptance as blocked.

Continue under this same coordinator, PLAN.md/LOG.md/DECISIONS.md and remaining finite budget. The runner owns dependency-frontier scheduling, host-owned isolation, leaf briefs, scoped review/fix rounds, worker acceptance and integration proof. It adds no second controller or ledger. Close tickets only after worker and integrated evidence are accepted, and only within current tracker authority. A child returns artifact/check state; monitoring belongs to the root only when requested or while an already authorized action waits.

For one authorized slice, use the `implement` skill; an accepted testing seam can use the `tdd` skill. Generic non-code coordination continues through the flow below. A mixed run keeps one graph and budget, with code-ticket execution assigned to the same runner.

### Plan and staff a multi-agent task

1. For generic work without an approved code-ticket graph, decide whether to delegate at all, split the goal into tasks with dependencies, owners, and write boundaries, and record the budget → the `work-decomposition` skill.
2. Open the run record (plan, log, decisions) on disk before the first dispatch → the `decision-log` skill.
3. Write one brief per task that a fresh agent with no history can execute, including the role and capability skills it loads and its return contract → the `agent-briefing` skill.
4. Dispatch within the budget and the concurrency limit; launch independent tasks together; wait for completion instead of polling; cancel superseded work.
5. Take in each result: save the raw report, check it against its brief, and spot-check its claims at the source → the `result-verification` skill.
6. Integrate, then run the acceptance checks on the combined result → the `result-verification` skill.

### Design, review or debate

For a concrete interface or module design, use the `architect` skill with the `codebase-design` skill's vocabulary. It optionally consumes the `agent-debate` skill's blind alternatives engine. A code review uses the `change-review` skill in report-only mode; an authorized code review/fix loop uses the `sol-loop` skill. An explicit `council` entry dispatches code fixes to that loop, design/non-code deliberation to debate, and read-only work to a report-only panel. The `interrogate` skill selects report-only code probes. Preserve requested providers and scope; every seat and retry is reserved from this run's budget.

For non-code deliberation or choosing between approaches:

1. Get independent first positions from distinct lenses or models, written blind → the `agent-debate` skill.
2. Run evaluator rounds with finding IDs, severity, evidence, exact changes, and a verdict line; log every acceptance and rejection → the `agent-debate` skill and the `decision-log` skill.
3. Stop at full agreement, or when a finding reaches its round limit without new evidence; bring each finding still open to the user as a decision with both positions.

### Ship a verified result

Enter at the requested delivery stage after acceptance on the integrated artifact. Preserve the existing authority, run record, remaining budget and finish mode; an installed or loaded entry grants no external action.

1. **Draft or file.** Read the `file-pr` skill. A title/body request selects its local body-only mode; create or update a PR only when requested or already authorized. Use the repository's template and merged style, include actual acceptance evidence, and return and host-link each created or updated layer with its current head, base and check/review state.
2. **Watch when needed.** Read the `babysit-pr` skill only for requested monitoring or while an already authorized action still waits on checks or reviews. Only the root owns one watcher per PR; handle available work, then use the host's completion mechanism. A filing-only task returns its link and state. Every child returns PR/head/check/review state and never watches. With no supported watch mechanism, report one bounded status pass and the next action.
3. **Carry the finish mode.** An explicit finish-to-merge request uses the `full-send` skill. An explicit prepare-without-merge request uses the `full-stop` skill, which selects full-send's shared prepare-only mode. Carry no-merge through every helper and child; cancel relevant owned pending auto-merge/queue entries and verify absence. Neither filing nor taking over work supplies merge authority.

Bind proof, checks and readiness to the current relevant head and base. Keep every unresolved review thread regardless of age until addressed or disposed of with a written reason. Repository policy decides required checks, bots and human approvals; confidence and vendor identity waive no gate. Three review/fix rounds is the default, with any larger bounded allowance declared before starting; stable or renamed finding IDs consume the same run budget. The delivery capabilities own their procedures; do not start a second shipping controller.

### Review the session workflow

For a requested session retrospective or workflow improvement, read the `retro` skill (required) and compare the actual available session evidence with the requested process. Keep missing history explicit and apply only supported improvements within current authority. Completion alone starts no retrospective, instruction edit or public issue. Record any improvement and its proof in this run's existing decision trail.

### Resume after an interruption or compaction

1. Read the run record: plan, budget used, dispatched tasks, raw reports, decisions → the `decision-log` skill.
2. Reconcile what finished with what the record expected; never repeat completed work, and never treat a missing report as a result.
3. Continue from the next unmet task.

Read [the workflow modes](references/workflow-modes.md) when choosing a stage, splitting coverage, comparing competing attempts or resuming a bounded run. It supplies routing and recovery checks; the named capabilities own their procedures.

## Handoffs

- **Role work** goes to the matching role router (backend, frontend, data, security, and the rest), loaded by the worker its brief names.
- **A mistake that repeats across runs** → the `correct` skill, to make it fail a check instead of being corrected again.
- **The enforcement environment of a repository** → the `project-guardrails` skill.

## Done

- The combined result passes its acceptance checks, with the commands and their output reported.
- The run record holds the plan, the budget and what was spent, every raw report, and every decision with its evidence.
- The user's report leads with the outcome, then the decisions still open (each with both positions), the evidence limits, and the cost: workers started, review rounds, and any budget left unspent.
- Delivery reports distinguish a local draft, filed PR, ready state and observed merge; a child returns state without a watcher.
- No action outside the authorization the user gave; an action whose authorization is unresolved waits for the user.

Per-file attribution: [references/SOURCES.md](references/SOURCES.md).
