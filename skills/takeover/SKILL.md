---
name: takeover
description: Take over existing work and finish its original goal. Reconstruct the author's intent and the PR's current head, base and review state, verify inherited claims instead of trusting them, and preserve the original contributors' credit. Use when the user asks to take over a PR, branch or agent thread.
license: MIT
metadata:
  requires: "result-verification"
  source: https://github.com/t3dotgg/tstack/blob/1085050f3baed1ac724caa4a8166145fb2ac88af/skills/takeover/SKILL.md
  source-revision: 1085050f3baed1ac724caa4a8166145fb2ac88af
  source-license: "MIT; see LICENSE-tstack"
  source-files: "skills/takeover/SKILL.md"
  local-changes: "Reconstruct exact PR, head, base, credit, prior record and remaining task before any change; inherited green checks and reports are claims until result-verification establishes current evidence; unresolved older feedback kept; modernize only when the base or conflicts need it; no inherited merge or watch authority; full-stop no-merge mode propagated; filing-only work returns link and state; added the shared delivery contract."
---

# Takeover

Take responsibility for finishing the original goal while preserving the original contributors' credit. Do not defend an implementation just because another agent already built it.

## Reconstruct before changing anything

1. Read the source PR, branch or thread, including review findings and the user's later corrections.
2. Record the exact current state: PR link and state, head SHA, base branch and SHA, checks at that head, review decision and every unresolved thread, however old.
3. Account for uncommitted work in any worktree you inherit. Treat it as someone else's until you know otherwise.
4. Find the prior record: plans, decision logs, handoff notes and earlier reports. Treat the handoff as context, not proof.
5. State the author's intent and the remaining task the user asked you to finish. Scope your work to that task.

## Verify inherited claims

An inherited green check, test report or "done" note is a claim. Re-establish it with the `result-verification` skill at the current head and base before you rely on it. A check that ran on an older head, a mocked test or a summary without output is not evidence for the current code. State what remains unverified.

Independently verify the original failure and realistic workflows, following repository guidance and permissions. Green mocked tests do not prove the user experience works.

## Continue the work

- For a replacement PR, import the original commits onto a new branch and add your fixes as separate commits. Honor an explicitly requested in-place or stacked continuation instead.
- Do not overwrite unrelated work, and do not change the original PR without authorization.
- When the base moved or conflicts block the work, use the `modernize` skill, with its captured leases and current-revision checks.
- Rework what the goal needs, not unrelated features. Simplify without dropping intended behavior or surfaces.
- Recheck the source PR before you finish; it may have improved while you worked.

## Preserve credit

Preserve Git authorship and existing co-author trailers. Credit the original contributors in the PR description and link the original PR when there is one. If the work will be squashed, keep human author and co-author credit in the merge commit too, using verified identities rather than guessed emails. Model attribution is not a substitute for contributor credit.

## Authority

Taking over a PR, or reading a helper skill, grants neither merge nor monitoring authority. The original author's permissions do not transfer to you.

- When the requested finish includes a PR, use the `file-pr` skill to file or update it. A filing-only task ends with the link and current state.
- Continue with the `babysit-pr` skill only as the root agent, and only when the user asked for monitoring or an authorized action is still pending.
- Use the `leaving-pr-comments` skill for replies.
- Merge or close the original PR only when that is explicitly authorized.
- When the task runs in no-merge mode (the `full-stop` skill), carry it into every helper you use.

## Delivery contract

- Bind every check result, proof and readiness claim to the current head and base. A result for an older head or base is history, not evidence.
- An unresolved review thread stays relevant, whatever its age or the pushes since, until it is addressed or explicitly disposed of with a written reason.
- Required checks, bots and approvals come from repository policy: branch protection, rulesets, CODEOWNERS and documented process. A vendor name or model confidence never makes a gate optional.
- Run at most three review/fix rounds. A larger bounded allowance applies only if it was declared before the run. Renaming or rewording a finding never resets the count.
- Only the root agent watches a PR, and only on a monitoring request or while an already authorized action is pending. Filing alone returns the link and current state. A child returns state and never watches.

## Report

What you inherited (with the head and base you started from), what you changed, how you verified it at the current head, how credit was preserved, unresolved threads, and any remaining decision.

Provenance and the per-file manifest: [references/SOURCES.md](references/SOURCES.md).
