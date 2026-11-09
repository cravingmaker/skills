# Finishing a branch

Read this when authorized work lands without a PR (a local merge), when the branch sits in a detached-HEAD workspace, or when a worktree needs cleaning up after the work lands. The finish mode already decided what is authorized; do not present a menu asking again.

## Verify the tree you integrate

Run the project's full test suite on the exact tree you are about to integrate. A green run only proves the tree it ran on; "tests passed earlier this session" is not evidence. If tests fail, report the failures and stop.

## Know the workspace

Capture these while still inside the workspace, because later steps change directory:

```bash
GIT_DIR=$(cd "$(git rev-parse --git-dir)" 2>/dev/null && pwd -P)
GIT_COMMON=$(cd "$(git rev-parse --git-common-dir)" 2>/dev/null && pwd -P)
WORKTREE_PATH=$(git rev-parse --show-toplevel)
```

- `GIT_DIR == GIT_COMMON`: a normal repository; no worktree to clean up.
- `GIT_DIR != GIT_COMMON` on a named branch: a worktree; cleanup depends on who created it.
- `GIT_DIR != GIT_COMMON` on a detached HEAD: an externally managed workspace. Push as a new branch (`git push origin HEAD:refs/heads/<new-branch>`) and open the PR from it; never merge locally from here, and leave the workspace in place.

## Confirm the base

The base is whatever this work forked from, usually named in the plan, the conversation or the branch's upstream. If it is not known, confirm it before merging; merging into the wrong base is expensive to undo.

## Local merge

Only when the finish mode authorizes merging and the repository does not land work through PRs:

```bash
MAIN_ROOT=$(git -C "$(git rev-parse --git-common-dir)/.." rev-parse --show-toplevel)
cd "$MAIN_ROOT"
git checkout <base-branch>
git pull
git merge <feature-branch>
<test command>
```

If tests fail on the merged result, stop and leave the worktree and branch in place; nothing is pushed yet, so the merge is local and recoverable. Delete the branch with `git branch -d` only after the merged result is green and landed.

## Keep evidence until the work lands

- While a PR is open, keep its worktree: feedback gets fixed there.
- A rejected push means the remote moved. Investigate; force-push only this task's own branch, with a captured lease.
- Discarding work happens only on an explicit request for it. Show exactly what would be deleted (branch, commits, worktree path) and wait for confirmation.

## Clean up a worktree

Only after the work landed, and only a worktree this run created (for example one under `.worktrees/` or `worktrees/`, or one the host's tool made for this task). Everything else belongs to the host or another agent; leave it, or use the host's own workspace-exit tool.

```bash
git worktree remove "$WORKTREE_PATH"
git worktree prune
```

If removal is refused because the worktree holds modified or untracked files, those files exist nowhere else. Never `--force` it on your own initiative. Show the user what is at stake (`git -C "$WORKTREE_PATH" status --porcelain -uall`) and ask whether to commit them, move them, or delete them.
