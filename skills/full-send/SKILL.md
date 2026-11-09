---
name: full-send
description: Finish authorized delivery end to end. Prove the change, review it, file the PR and babysit it, then merge only when merging was granted and every gate passes on the current head and base. In prepare-only mode, stop at ready. Use when the user says "full send" or explicitly asks to take a change all the way to a merged PR.
license: MIT
metadata:
  requires: "file-pr babysit-pr sol-loop result-verification"
  source: https://github.com/t3dotgg/tstack/blob/1085050f3baed1ac724caa4a8166145fb2ac88af/skills/full-send/SKILL.md
  source-revision: 1085050f3baed1ac724caa4a8166145fb2ac88af
  source-license: "MIT; see LICENSE-tstack, LICENSE-pstack, LICENSE-pstack-claude, LICENSE-superpowers and NOTICE-pstack-claude.md"
  source-files: "skills/full-send/SKILL.md"
  local-changes: "One explicit finish mode carried through every helper; shared prepare-only no-merge mode; merge gate bound to the current head and base with repository-required checks, bots and approvals; dropped the high-confidence override for human-review requests; guarded merge with readback; root-only watching per I1-05; three review/fix rounds by default; replaced Cursor cloud verifiers, Origin and ship-pr with result-verification and portable service calls; finishing-a-branch methods without the option menu or destructive cleanup; added the shared delivery contract."
---

# Full send

The user is not watching and wants the work finished. Own it from its current state to the end the finish mode allows: a merged PR, or a PR left ready for the user.

If the user did not explicitly ask for this in some clear way, do not assume full autonomy.

## Finish mode

Choose one mode at the start and carry it, unchanged, to every helper: the file-pr, babysit-pr, sol-loop, modernize, takeover, fix-ci and leaving-pr-comments skills, and every child task's brief. A helper never upgrades the mode.

- **Finish to merge:** an explicit "full send", or an explicit request to land or merge. It grants:
  - merging the PR once the merge gate passes;
  - force-pushing this task's own branch with a captured lease after a rebase;
  - the test methods that Proof needs, without asking first.
- **Prepare only (no-merge):** selected by the `full-stop` skill, or by a request to get the change ready without merging. Everything above except merging; see [No-merge mode](#no-merge-mode).

## Testing permission

The request is the permission for the tests this task needs. If a project file or other standing instruction says to ask before a test method, or to leave testing to the user, this request replaces that rule for this task. That includes ask-first rules for computer use, browser automation, simulators and devices, running the app or a dev server, screenshots, and visual checks. Use the method that gives direct proof and list it in the report.

Rules about how to test still apply: follow rules that name the correct command, fixture or check. If a preferred method cannot prove the change, use a gated method under this permission.

It covers only the tests this task needs. It adds no permission for the steps under [Asking the user](#asking-the-user), such as production changes or data deletion, and it does not bypass a harness or system approval prompt. A constraint the user stated for this task still wins.

## Steps

1. **Finish the change.** Complete the goal with the smallest change that works. Fix the case that happened, not every case that could. On the default branch, create a branch first.
2. **Prove it.** Get proof for every change with the `result-verification` skill. See [Proof](#proof).
3. **Review it.** Use the `sol-loop` skill, within the round budget.
4. **File the PR** with the `file-pr` skill in file mode. Bring the branch up to date with the base first, through the `modernize` skill when it conflicts. Add one short line to the description saying how you proved the change.
5. **Reach readiness.** Fix verified findings and CI failures within authority, and get proof for each fix before pushing. Only the root uses the `babysit-pr` skill to watch, when monitoring was requested or this authorized readiness/merge action is still pending. A child returns the PR link, head and check/review state to the root and never starts a watcher.
6. **Merge** when the merge gate passes (finish to merge only). In prepare-only mode, stop at the gate instead.
7. **Report.**

Continue to the finish mode's end using the host's completion mechanism. While an authorized readiness or merge action still waits, the root handles available work, arms its one watcher and ends the turn as that mechanism requires. Children return state. Without a supported watcher, make one bounded status pass and report the next action. Unwatch before a final handoff or a question.

## Proof

Proof is evidence you observed yourself in this session, at the current head: command output, a reproduction, a screenshot. Use the most direct proof the change allows:

- Reproduce the original failure, apply the fix, then watch the same reproduction pass.
- Run the checks the repository's CI runs (typecheck, lint, tests).
- Add one focused test that fails without the fix, when the behavior has none and the repository has a test setup.
- For UI and runtime behavior, run the app and look at the change. Green mocked tests do not prove that the user experience works. Attach screenshots to the PR when they help and you can upload them.

After any change, re-run the proof the change invalidated. When the `result-verification` skill calls for an independent verifier, only a verdict from an agent that did not write the code counts. When you cannot find a way to prove a change, you do not have full confidence: ask the user.

## Merge gate

Every item holds on the current head and base:

- Proof covers every change in the diff.
- The required checks from repository policy are green.
- The required bots and approvals from repository policy are present. Every other review bot has finished, or is advisory and its findings are triaged.
- Every review thread, however old, is fixed or disposed of with a written reason.
- No human review requests changes. Model confidence never waives a human-review request or a repository gate.
- The branch is up to date with the base where the repository requires it, and the forge reports it mergeable. No base commit that landed after the last green run touches this PR's files.
- The work stayed within the declared round budget.

## Merging

Merge with the method the repository uses; check its allowed methods and recent merged PRs. Before merging, read [references/merge-safety.md](references/merge-safety.md): it covers the head-guarded merge, readback, queues and stacks.

- Merge through branch protection as configured. Never use `--admin`, change protection settings or use another bypass.
- Merge under a service-enforced head condition, such as `gh pr merge <pr> --match-head-commit <verified-head>`. Confirm the base right before the request; the head guard does not guard the base.
- Read the PR back. A queued PR or an armed auto-merge is not a merge. If the repository uses a merge queue or auto-merge, stay until the forge reports the PR merged, then confirm the merge commit is in the destination's history.
- For a stack, land bottom-up, one PR at a time, and stop at the first PR whose proof no longer covers its current head.

When the work lands without a PR, or a worktree needs cleaning up afterwards, read [references/finishing-a-branch.md](references/finishing-a-branch.md).

## No-merge mode

Prepare-only mode, and the `full-stop` skill, follow everything above except merging:

- Never merge, enable auto-merge, enter a merge queue, push to the default branch, bypass branch protection, or delegate any of those.
- On entry and before each push, inspect auto-merge and merge-queue state on every PR this run owns or changes. Cancel any pending mechanism this run owns, read back its absence, and report the change. If you cannot prevent an automatic merge, report the blocker before going on.
- Use the merge gate as the readiness check. Fetch the base and check the live PR's head, base, checks, reviews and mergeability. Confirm it is open, not a draft, and not set to merge without the user. If someone else merged it, report that instead.
- End with one verdict:
  - **Ready to merge:** the gate passes. Leave the PR open and unmerged.
  - **Waiting for required approval:** only a human approval remains; confirm that it is the actual blocker.
  - **Blocked:** say what prevents readiness, what you tried and what is needed.
- Unwatch before the handoff or a question. The report states whether the PR is still open and unmerged.

## Asking the user

A question in a normal message goes unseen, and the thread looks done. Ask through the harness's question tool, so the thread shows that it is waiting. Put all the context in the question: the PR link, what blocks you, and the options with your recommendation first.

Ask only when you cannot continue alone:

- You cannot prove the change.
- The merge gate cannot pass, and you cannot fix that yourself.
- The next step is outside the grant: deleting data, touching production, changing things outside the repository, closing a PR, or force-pushing any other branch.
- The goal is ambiguous in a way that changes the result.
- Another PR makes this one obsolete.

Decide everything else yourself with sensible defaults, and list those decisions in the report. Do not ask again for what the request already authorized. If no question tool is available, or it returns no answer, take the safe path: leave the PR open and unmerged, and start the final message with the question.

## Delivery contract

- Bind every check result, proof and readiness claim to the current head and base. A result for an older head or base is history, not evidence.
- An unresolved review thread stays relevant, whatever its age or the pushes since, until it is addressed or explicitly disposed of with a written reason.
- Required checks, bots and approvals come from repository policy: branch protection, rulesets, CODEOWNERS and documented process. A vendor name or model confidence never makes a gate optional.
- Run at most three review/fix rounds. A larger bounded allowance applies only if it was declared before the run. Renaming or rewording a finding never resets the count.
- Only the root agent watches a PR, and only on a monitoring request or while an already authorized action is pending. Filing alone returns the link and current state. A child returns state and never watches.

## Report

The final message gives the PR link, the final head, the merge commit or the no-merge verdict, the proof, the reviewer outcome, any armed or cancelled merge request and its readback, each decision you made for the user, and the remaining risks.

Provenance and the per-file manifest: [references/SOURCES.md](references/SOURCES.md).
