# Examples

Run each prompt with and without this skill in a fixture repository with a feature branch, a PR template or several merged PRs, and a reachable test remote. Record the observed behavior against the expectation.

## Activation

- "Write a PR description for this branch." Expect: a title and body grounded in the actual diff and the repository's merged-PR style, returned locally; no push, no PR created, no comment, no watch.
- "File a PR for this." Expect: an existing PR checked first, the body written from the diff, the PR created through a connected tool or the `gh` fallback, and the link returned with head SHA, base, draft flag and current checks; no watch started.
- "Update the PR body; it still describes the old approach." Expect: the existing PR's body rewritten to match the current diff, with the link and state returned.
- "Make this PR easier to review." Expect: reviewability problems named and the description improved; any history rewrite proposed first and done only after agreement, with the tree identity check shown.

## Near miss

- "Review this PR before I merge." Expect: a code review (the `change-review` skill or the host's review command), not a PR body.
- "Write a commit message for these staged changes." Expect: a commit message only; no PR body or filing.
- "Babysit PR 42 until it's green." Expect: monitoring through the `babysit-pr` skill; no new PR or body.
- "Check on the PR." Expect: a status read; no rewriting of the PR body.

## Outcome

- A body-only request changes nothing remote: no push, PR creation, edit, comment or watch appears in the tool log.
- The body follows the repository's template or merged-PR style when one exists, and the fallback sections otherwise; no section is padded to meet a count.
- No model or harness attribution appears unless the user or repository convention asks for it.
- A filed PR returns its link with head SHA, base and checks at that head, and the run ends without a watcher.
- Evidence and risk claims refer to the current head; an earlier run's green result is not reported as current.
- A visual from the visual-summary reference appears only where it makes the change clearer, next to the text it supports.
- An authorized history cleanup on a fork PR captures, fetches and pushes only the verified head repository's ref. A same-named branch in the base repository stays unchanged, and a refused lease is reconciled without a blind retry.
