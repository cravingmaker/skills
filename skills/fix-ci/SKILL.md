---
name: fix-ci
description: CI failure triage and repair for a failing check on the current head. Bind the run, attempt and first causal error. Classify the cause as code, test, stale base, flake, runner, outage, quota or billing. Then apply the smallest justified fix or one bounded retry. Use when a PR's or branch's CI is red.
license: MIT
metadata:
  requires: "diagnosing-bugs"
  source: https://github.com/michael-denyer/pstack-claude/blob/91ab921ab92d9ccfe503c93c3524410277f012e1/plugins/pstack/skills/fix-ci/SKILL.md
  source-revision: 91ab921ab92d9ccfe503c93c3524410277f012e1
  source-license: "MIT; see LICENSE-cursor-team-kit, LICENSE-pstack-claude, LICENSE-pstack and NOTICE-pstack-claude.md"
  source-files: "plugins/pstack/skills/fix-ci/SKILL.md"
  local-changes: "Bound the run, head, attempt and first causal error; folded the ci-failure-triage classification (code, test, stale base, flake, runner, outage, quota, billing); one bounded fresh retry only for evidenced flake or runner failure; no edits for a no-step billing or quota failure; required repository gates kept; three rounds by default; diagnosing-bugs required; added the shared delivery contract."
---

# Fix CI

Get a red check green for the right reason. Read the real logs, find the first error that caused the failure, classify it, and make the smallest change the cause justifies. A failure that no code change can fix gets a report, not an edit.

## Steps

1. **Bind the failure.** Record the PR or branch, the current head SHA and base, the failing check, its workflow run ID, attempt number, job, step and log link. Read the checks from a connected forge tool, or `gh pr checks --json name,bucket,state,workflow,link`. If the failing run is for an older head, re-read the checks at the current head first; an old failure is history.
2. **Read the real logs.** Use `gh run view <run-id> --log-failed` for GitHub Actions, or the external check's own link. Find the first causal error, not the last line or a cascade of follow-on failures. When no step ran at all, read the run's annotations and the job's runner assignment instead.
3. **Classify the cause** with the evidence that decides it:
   - **Code:** the failure is in code the diff changed.
   - **Test:** the test itself is wrong, or it pinned behavior the change was meant to alter.
   - **Stale base:** the failure is in code the diff never touches. Check whether the branch contains the current base with `git merge-base --is-ancestor origin/<base> HEAD` before assuming a flake.
   - **Flake:** the same SHA passes and fails without a change, or the failure matches a known nondeterministic pattern.
   - **Runner or infrastructure:** the runner was lost, ran out of disk, or failed to provision.
   - **Third-party outage:** a registry, API or service the job depends on was down; cite its status or error.
   - **Quota or billing:** the job never started or stopped on an account limit, such as spending limits or exhausted minutes.
4. **Act on the class:**
   - **Code or test:** reproduce the narrow failure locally with the same command CI runs. When the cause is not obvious, follow the `diagnosing-bugs` skill. Fix one actionable failure at a time with the smallest safe change. Change an assertion only when the behavior genuinely changed and the assertion pinned the old behavior.
   - **Stale base:** report that the branch needs its base brought in; update it through the `modernize` skill only when the task authorizes branch updates.
   - **Flake or runner:** one fresh run of the whole workflow, not a single-job retry. An identical second failure means it was never a flake: reclassify and read the child logs instead of retrying again.
   - **Outage, quota or billing:** change no code. Report the blocker, its evidence and who can clear it, such as the account owner.
5. **Re-check.** Push the fix within the task's authority, then read the full set of required checks at the new head. Repeat from step 1 for the next failure, within the round budget.

## Guardrails

- Never mark a failing check as not required, skip hooks, bypass branch protection or loosen a test just to pass.
- Never claim "all green" without observing every required check at the current head.
- Prefer minimal, low-risk changes over broad refactors.
- A retry needs evidence of flake or runner failure; a blind retry is not a fix.

## Delivery contract

- Bind every check result, proof and readiness claim to the current head and base. A result for an older head or base is history, not evidence.
- An unresolved review thread stays relevant, whatever its age or the pushes since, until it is addressed or explicitly disposed of with a written reason.
- Required checks, bots and approvals come from repository policy: branch protection, rulesets, CODEOWNERS and documented process. A vendor name or model confidence never makes a gate optional.
- Run at most three review/fix rounds. A larger bounded allowance applies only if it was declared before the run. Renaming or rewording a finding never resets the count.
- Only the root agent watches a PR, and only on a monitoring request or while an already authorized action is pending. Filing alone returns the link and current state. A child returns state and never watches.

## Report

- The failing check, run ID, attempt and head SHA.
- The first causal error, quoted from the log.
- The class and the evidence that decided it.
- Fixes in the order applied, each by commit SHA, or the retry and its result.
- The required checks' state at the current head, and the next action or blocker.

Provenance and the per-file manifest: [references/SOURCES.md](references/SOURCES.md).
