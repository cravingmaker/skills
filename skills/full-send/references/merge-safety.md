# Merge safety

Read this before merging, arming auto-merge, rebasing or retargeting a PR in a full-send run. These steps add revision and destination checks; they grant no merge authority.

## Contents

- [Record the landing revision](#record-the-landing-revision)
- [Pending merge mechanisms](#pending-merge-mechanisms)
- [What the service guards](#what-the-service-guards)
- [Land a stack](#land-a-stack)
- [After the merge](#after-the-merge)

## Record the landing revision

Before review starts, capture the affected chain bottom-to-top: each PR's head branch and SHA, base branch and SHA, and the intended destination repository and branch. Leave unrelated PRs alone. Record each proof with the head SHA, base SHA, base branch and the stable `git patch-id` of the base-to-head diff it covered.

## Pending merge mechanisms

A pending auto-merge or merge-queue entry lands whatever the branch and base hold when it fires, proven or not.

1. On entry, read the auto-merge request and queue membership of every affected PR, with the revision each applies to. Use the host's PR tool or a connected forge tool first; otherwise `gh pr view <pr> --json autoMergeRequest,headRefOid,baseRefName,mergeStateStatus` and the GraphQL `mergeQueueEntry` field.
2. Cancel a pending request this run owns that lacks the gates below before a lengthy review, and before any push, rebase or base edit: `gh pr merge <pr> --disable-auto`, and the `dequeuePullRequest` mutation for a queue entry.
3. Read the state back and require both mechanisms to be absent on the same open revision. Missing fields and unsupported APIs never mean absent. If cancellation fails, state is unavailable, or a PR merges meanwhile, stop and reconcile the actual state first.

Cancellation is an observed condition, not a lock; another actor can re-arm it. Check again at each wakeup, and cancel a pending request whose evidence no longer applies.

## What the service guards

GitHub's immediate merge head condition is `--match-head-commit` in `gh pr merge`, `expectedHeadOid` in the GraphQL `mergePullRequest` mutation, or `sha` in the REST merge endpoint. Use one, carrying the exact verified SHA. None of them guards the base branch: observe the base immediately before and after, and coordinate retargeting. Do not call those observations atomic.

Arm auto-merge or queue admission only on a PR whose proof covers its current head, and only behind repository rules that enforce the required checks on the revision that will land. A queue-required branch can turn a plain merge into queue admission, so the same rule applies. A prose verdict or a green check on an older head is not such a gate. If those guarantees cannot be established, keep watching for an immediate guarded merge, or stop at merge-ready and report the limitation.

Service references: [GitHub CLI merge flags](https://cli.github.com/manual/gh_pr_merge), [GraphQL pull requests and queue mutations](https://docs.github.com/en/graphql/reference/pulls), and [REST merge endpoint](https://docs.github.com/en/rest/pulls/pulls#merge-a-pull-request). Recheck the installed service's capabilities when they differ. Test service behavior in a disposable repository, never with production PRs.

## Land a stack

1. **Land only the contiguous proven run from the bottom.** Walk up from the lowest unmerged PR and stop at the first one whose proof does not cover its current head. A proven PR above an unproven one waits, because it cannot land without the code below it.
2. **Check that the proof still describes the code.** A rebase moves every PR above it to a new SHA without failing any check. Compare `git patch-id` at the proof's SHA with the current head before trusting older proof. When the patches differ only in tests, docs or lint config, a result stands if what it ran builds the same at both SHAs apart from noise; report each kind of noise with its files. A matching patch-id keeps a review only after you check that it applies to the new destination and dependencies. Re-verify changed behavior or uncertain applicability, and rerun checks and mergeability after every rewrite or retarget.
3. **Land bottom-up, one PR at a time,** always the lowest unmerged PR of the run, with the head guard above. A PR whose base is still its parent's branch merges into that branch, not trunk.
4. **Move the next child.** After a merge lands, cancel the child's pending mechanisms as above, retarget its base to trunk, and replay only its own commits onto the merge result from the recorded old parent tip. Never infer the boundary from the squash commit. Push with a lease on the remote SHA captured before the rewrite; if the lease refuses, fetch and reconcile instead of retrying.
5. **Leave the stack alone while it lands.** That move is the only change to a branch or base. A base that moves to trunk when its parent merges is expected, not damage to repair. If a merge stalls, find out why before you change anything.
6. **Stop at the ceiling.** Extending the run takes new proof for each added PR.

## After the merge

Confirm the PR reads merged, with the approved final head, the intended base and a non-null merge commit. Fetch the destination and run `git merge-base --is-ancestor "$merge_commit" "$destination_tip"`, then check the resulting content before advancing. If the service cannot report these facts, the outcome remains unconfirmed; say so.
