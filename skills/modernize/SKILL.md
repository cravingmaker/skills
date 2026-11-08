---
name: modernize
description: Bring an aging or conflicted pull request up to date with its base without losing either side's intent. Re-establish what the PR is for and check what changed around it. Then rebase, resolve conflicts, test, and push with a captured lease. Use when asked to rebase, update, fix conflicts on, or modernize a PR.
license: MIT
metadata:
  source: https://github.com/t3dotgg/tstack/blob/1085050f3baed1ac724caa4a8166145fb2ac88af/skills/modernize/SKILL.md
  source-revision: 1085050f3baed1ac724caa4a8166145fb2ac88af
  source-license: "MIT; see LICENSE-tstack, LICENSE-cursor-team-kit, LICENSE-pstack-claude and NOTICE-pstack-claude.md"
  source-files: "skills/modernize/SKILL.md"
  local-changes: "Merged fix-merge-conflicts resolution and lockfile rules; host-owned isolation; leases on a captured remote SHA, with a refused lease reconciled instead of retried; child range boundaries after a parent squash; owned pending merges cancelled and verified absent before topology rewrites; unresolved feedback, scoped push authority and no-merge mode preserved; no replacement PR, broad cleanup or watcher; added the shared delivery contract."
---

# Modernize

Modernize the idea, not just the branch. A clean rebase does not prove that the PR still belongs in the product.

## Authority

- Modernizing authorizes rebasing and updating the PR branch named in the request. It does not authorize merging, closing, changing the base branch, expanding scope, opening a replacement PR or starting a watch.
- Another contributor's branch, a fork or a shared stack branch needs its owner's go-ahead before you rewrite it.
- Treat existing worktree changes as the user's. Work in the host's isolation mechanism, such as its worktree tool, or a disposable `git worktree` when the host has none.
- Never use an unqualified force push. Push with a lease on the remote SHA captured before the rewrite.
- When the task runs in no-merge mode (the `full-stop` skill), keep it.
- Post no PR comment unless the user asked for one; use the `leaving-pr-comments` skill for one.

## Establish the PR's intent

1. Resolve the PR and record its URL, state, base, head repository and branch, current head SHA, author, checks, review state and every unresolved thread.
2. Read the title, body, linked issues, commits, review threads and the complete diff. State the smallest coherent goal the PR was trying to reach before judging its implementation.
3. Fetch the latest remote base and PR head. Use the PR's actual base branch, not the local branch's idea of it. Record the merge base, so the original PR and later base changes can be compared separately.

## Check what changed around it

Inspect commits and diffs added to the base since the PR diverged. Search merged and open PRs when titles, code paths or behavior suggest a replacement or competing implementation. Look beyond overlapping lines:

- Has the same user-facing problem already been solved?
- Did APIs, types, schemas, dependencies or architectural boundaries change?
- Do both sides now claim ownership of the same behavior or invariant?
- Was the code being changed deleted, moved or intentionally simplified?
- Would landing the PR restore an old behavior or create two ways to do the same thing?
- Is the original benefit still large enough to justify the maintenance cost?

Do not call a PR current merely because Git reports no conflicts.

## Choose a disposition before pushing

- **MODERNIZE:** the goal is still useful and the implementation is still the right shape. Rebase, resolve, test and update the branch.
- **REWORK:** the goal is still useful, but a mechanical rebase would preserve the wrong implementation. Explain the smallest credible rewrite and stop before pushing, unless the user also asked for that rework.
- **CLOSE:** the PR is superseded, obsolete, directionally wrong or no longer worth its cost. Cite concrete evidence and stop. Do not rebase an obsolete branch, and do not close it without explicit permission.

Be willing to recommend CLOSE. Age alone is not evidence, and sunk effort is not a reason to keep a PR alive.

## Rebase without losing intent

For a MODERNIZE disposition:

1. Resolve a remote whose fetch and push URLs identify the PR's head repository, and record it as `head_remote`, separately from the base remote. Capture the remote head with `git ls-remote --exit-code "$head_remote" "refs/heads/<branch>"`. Require exactly that ref and the recorded PR head SHA; reconcile a mismatch before rewriting. The name `origin` alone establishes no repository identity.
2. Before rewriting, inspect auto-merge and merge-queue state on this PR and on every PR whose base or contents the rewrite changes. Cancel any pending merge you own and read back its absence. Read [references/restack-safety.md](references/restack-safety.md) for stacks and the cancellation readback.
3. In the isolated worktree, start a branch at the recorded PR head and rebase its commits onto the freshly fetched base. Merge the base in instead when the repository or user prefers merges. After a parent squash-merged, rebase a child from its recorded old parent tip, never from the squash commit.
4. Resolve each conflict by the PR's intent and the base's newer invariants:
   - Find every conflicting file from `git status` and the conflict markers.
   - Make minimal, correctness-first edits. Preserve both sides when that is safe; otherwise keep the variant that compiles and keeps public behavior stable.
   - Regenerate lockfiles with the project's package manager instead of editing them by hand.
   - Leave no conflict markers, and avoid broad refactors while resolving.
   - If a conflict reveals a product or architecture disagreement, stop and reconsider the disposition instead of guessing.
5. Compare the series before and after with `git range-diff`, and read the final diff. Confirm no intentional behavior disappeared and no already-landed behavior came back.
6. Run the repository's compile, lint and focused tests for the touched area. Distinguish real failures from pre-existing or infrastructure failures.
7. Push to that same verified head remote with the captured lease: `git push --force-with-lease="refs/heads/<branch>:<captured-sha>" "$head_remote" "HEAD:refs/heads/<branch>"`. If the lease refuses the push, fetch and reconcile the new work; do not refresh the lease and retry the overwrite.
8. Read the PR back at the new head: checks, mergeability and every unresolved thread. Rebasing does not resolve review feedback.

Do not merge the PR.

## Delivery contract

- Bind every check result, proof and readiness claim to the current head and base. A result for an older head or base is history, not evidence.
- An unresolved review thread stays relevant, whatever its age or the pushes since, until it is addressed or explicitly disposed of with a written reason.
- Required checks, bots and approvals come from repository policy: branch protection, rulesets, CODEOWNERS and documented process. A vendor name or model confidence never makes a gate optional.
- Run at most three review/fix rounds. A larger bounded allowance applies only if it was declared before the run. Renaming or rewording a finding never resets the count.
- Only the root agent watches a PR, and only on a monitoring request or while an already authorized action is pending. Filing alone returns the link and current state. A child returns state and never watches.

## Report

Lead with MODERNIZE, REWORK or CLOSE and the reason. Then summarize:

- meaningful changes on the base;
- conceptual conflicts, or confirmation that none were found;
- notable conflict resolutions and lockfile regeneration;
- the rebase and push result, with the old and new head SHAs and any cancelled merge request;
- checks run and their results at the new head;
- unresolved threads that still need answers;
- the remaining decision or work, with a link to the PR.

Separate observed facts from judgment. Say what could not be verified instead of manufacturing confidence.

Provenance and the per-file manifest: [references/SOURCES.md](references/SOURCES.md).
