# Restack safety

Read this before rewriting a branch that is part of a stack, or any branch with a pending auto-merge or merge-queue entry. These steps add revision checks; they grant no merge authority.

## Cancel pending merges first

A pending automatic merge lands whatever the branch and base hold when it fires. Before a push, rebase or base edit:

1. List every PR the change can affect: this PR and each descendant whose base or contents will change. Leave unrelated PRs alone.
2. For each, read the auto-merge request and merge-queue membership, with the head SHA, base branch and base SHA they apply to. Use the host's PR tool or a connected forge tool first; otherwise `gh pr view <pr> --json autoMergeRequest,headRefOid,baseRefName,mergeStateStatus` and the GraphQL `mergeQueueEntry` field.
3. Cancel the ones this task owns: disable auto-merge (`gh pr merge <pr> --disable-auto`) and remove the PR from the queue (the `dequeuePullRequest` mutation). A request someone else made is theirs; report it and stop before rewriting under it.
4. Read the state back and require both mechanisms to be absent on the same open head. Missing fields and unsupported APIs never mean absent. If a PR merged meanwhile or the state changed, stop and reconcile before rewriting.

Cancellation is an observed condition, not a lock: another actor can re-arm it. Check again before each push.

## Lease on a captured SHA

Resolve `head_remote` from the PR's recorded head repository and verify both its fetch and push URLs. Keep the base remote separate. Capture the remote branch SHA right before rewriting with `git ls-remote --exit-code "$head_remote" "refs/heads/$branch"`, and require exactly the intended ref with the recorded PR head SHA. Reconcile a mismatch before rewriting. Keep the repository identity, ref and captured SHA in the operation record. An implicit lease or an earlier fetch is not enough; a background fetch can move a tracking ref.

```sh
git push --force-with-lease="refs/heads/$branch:$captured_remote_head" \
  "$head_remote" "HEAD:refs/heads/$branch"
```

If the lease refuses the push, fetch and reconcile the concurrent work. Do not refresh the lease and retry the overwrite blindly.

## Child ranges after a parent squash

After a parent PR squash-merges, its child still carries the parent's old commits. Rebase only the child's own work:

1. Confirm the parent squash landed in the intended destination, and fetch trunk.
2. Find the recorded old parent tip the child was built on. Verify it is an ancestor of the child, and inspect `old-parent..child` to confirm the range holds only child work. If it does not, reconstruct the boundary before going on. Never infer it from the parent's new squash commit.
3. Resolve the child's head repository and verify its fetch and push remote as `child_head_remote`; capture `captured_remote_head` from that exact remote and child ref as above. In the child's clean worktree, where `HEAD` is the prepared child:

```sh
git merge-base --is-ancestor "$old_parent_tip" "$child"
git rebase --onto "$trunk_tip" "$old_parent_tip" "$child"
git push --force-with-lease="refs/heads/$child:$captured_remote_head" \
  "$child_head_remote" "HEAD:refs/heads/$child"
```

4. Inspect the resulting diff and content, reassess whether earlier reviews still apply, and run checks at the new head.
5. Retarget the child's base only after the cancellation above was verified. Keep the recorded boundary for each remaining child when preparing later levels.

Test unfamiliar service behavior in a disposable repository, never on production PRs.
