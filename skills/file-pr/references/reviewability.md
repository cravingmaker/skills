# Reviewability

Read this when an existing PR is hard to review, or before shaping commits and stacks for a new one. The default goal is reviewability without behavior changes.

## Inspect

1. Resolve the target PR from the user's link or the current branch.
2. Inspect the commits, diff size, changed paths, generated files and the current description.
3. Name the reviewability problems: noisy commits, a stale description, unrelated changes, mechanical and logic changes mixed together, missing tests, or no clear entry point for the reviewer.

## Improve the description first

When code behavior should stay untouched, prefer the description and review notes:

- A short summary that matches the actual diff.
- Core files separated from generated or mechanical files.
- Risky behavior changes, migration order, rollout plan and test coverage called out.
- Links to the issue, dashboard or design doc when they explain intent.

If the PR is too large to make reviewable with notes, recommend splitting it instead of polishing around the problem.

## Commits and stacks

- Prefer several narrow PRs to one large one. Each commit is landable and ordered to tell the story; a commit body does not restate its subject.
- A stack is a base-branch chain: the root targets trunk, and each child rebases onto its parent's exact tip and targets the parent's branch. Branch from trunk only for independent work.
- Good commit groupings usually follow dependency order: schema, storage or generated API definitions; core logic; wiring and integration; UI or surface behavior; tests.
- Before committing from a worktree that other agents may use, make sure no other live agent still holds it, then read `git status` of the tree you are about to ship.

## History cleanup

Rewrite history only when the user asks for it or agrees to the plan, and only on a branch you may rewrite. Propose the plan before rewriting or force-pushing.

Before rewriting, use the connected PR tool to record the head repository, branch and SHA and the separate base repository and branch. A supported fallback is `gh pr view <PR> --json headRepository,headRepositoryOwner,headRefName,headRefOid,baseRefName,state`. Resolve `head_remote` and verify that both its fetch and push URLs identify the recorded head repository; `origin` may instead be the base repository.

Capture the head ref before rewriting:

```bash
git ls-remote --exit-code "$head_remote" "refs/heads/$head_branch"
```

Require exactly that ref with the recorded PR head SHA and save it as `captured_remote_head`. Reconcile any mismatch. Fetch that same ref, confirm its identity, then record the original tree:

```bash
git fetch "$head_remote" "refs/heads/$head_branch"
fetched_head=$(git rev-parse FETCH_HEAD)
test "$fetched_head" = "$captured_remote_head" || exit 1
original_tree=$(git rev-parse "$captured_remote_head^{tree}")
```

After rewriting, verify content identity against the captured object:

```bash
git diff "$captured_remote_head" --stat
test "$(git rev-parse 'HEAD^{tree}')" = "$original_tree" || exit 1
```

Do not push if the tree changed unintentionally. Push to the same verified head remote with the captured lease: `git push --force-with-lease="refs/heads/$head_branch:$captured_remote_head" "$head_remote" "HEAD:refs/heads/$head_branch"`. If the lease refuses, fetch and reconcile rather than refreshing it to overwrite new work. Preserve authorship and co-author trailers through the rewrite.

## Guardrails

- Never hide meaningful behavior changes inside "cleanup".
- Do not bypass hooks unless the user explicitly asks.
- Keep code comments that carry rationale, constraints or legal notices; reviewability work does not strip comments.
