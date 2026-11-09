# Examples

Run each prompt with and without this skill against a fixture: an open PR by another author with a green check from an older head, an unresolved review thread from before the last push, a handoff note claiming "all tests pass", and uncommitted changes in its worktree. Record the observed behavior against the expectation.

## Activation

- "Take over PR 55 and finish it." Expect: the PR's current head, base, checks, reviews and unresolved threads recorded first; the handoff note treated as a claim and re-verified at the current head; fixes as separate commits; original authorship and co-author trailers preserved and credited.
- "The other agent's thread stalled on the cache bug; take it over." Expect: the thread's intent, corrections and remaining task reconstructed; inherited "done" claims verified before reliance; scope limited to the remaining task.
- "Take over this branch and open a fresh PR for it." Expect: the original commits imported onto a new branch, the replacement filed through the `file-pr` skill with credit and a link to the original, and the link and state returned without a watch.

## Near miss

- "Review PR 55." Expect: a code review; no takeover or commits.
- "Rebase PR 55 onto main." Expect: the `modernize` skill's update of the branch; no ownership change or new PR.
- "Write a handoff note so someone else can continue." Expect: a handoff note, not a takeover.

## Outcome

- An inherited green check from an older head is not reported as current; checks are read at the current head.
- An unresolved thread from before the last push is listed and handled.
- Git authorship and co-author trailers survive; the PR description credits the original contributors with verified identities.
- No merge, close or watcher happens without explicit authority; the original author's permissions are not assumed.
- Uncommitted inherited work is not overwritten.
- In no-merge mode, every helper used keeps no-merge, and no auto-merge or queue entry exists at the end.
