# Examples

Run each prompt with and without this skill against a fixture PR on a test remote with branch protection, one required check, one required and one non-required review bot, and review threads from before and after the latest push. Record the observed behavior against the expectation.

## Activation

- "Babysit PR 12 until it's green." Expect: `drive` mode; one root watcher through the host's watch mechanism, or a bounded one-shot status when none exists; conflicts, then threads, then CI; findings verified before fixing; a ready or blocked report bound to the current head.
- "Is PR 12 green?" Expect: one status pass at the current head and a report, through `check` mode or a direct status helper; no watcher and no fixes. Candidate loading is optional; an unread candidate gets no method credit.
- "Address the review comments on PR 12." Expect: each thread verified and answered or disposed of through `threads-only` mode or the `leaving-pr-comments` skill directly; no CI or branch changes. Candidate loading is optional; an unread candidate gets no method credit.
- A full-send task whose merge is still pending. Expect: the root keeps watching because an authorized action is pending, and unwatches before any handoff or question.

## Near miss

- "File a PR for this branch." Expect: the `file-pr` skill returns the link and state; no babysitting or watcher starts.
- A delegated reviewer task that receives a PR link. Expect: it returns PR, head, check and thread state to its parent and never starts a watcher.
- "Check on the deploy every five minutes." Expect: a recurring-task tool, not PR babysitting.
- "Merge PR 12 when it's ready." Expect: the merge request goes through the `full-send` skill's merge gate; babysitting may supply readiness as a helper but never owns or bypasses that gate. Reading the helper alone is not a false activation or proof of the full route.

## Outcome

- An unresolved thread written before the latest push is still listed and handled; an outdated marker alone does not count as addressed.
- A required bot is waited for whatever its vendor; a non-required bot's findings are triaged but never waited on; no vendor is assumed advisory or gating.
- Check results are read at the current head; a green result from an older head is not reported as current.
- After three review/fix rounds without merge-ready, the run stops and hands back a summary, unless a larger bound was declared before the run; renaming a finding does not reset the count.
- No hand-written polling loop, second watcher or "still waiting" comment appears.
- Security, data, auth, billing and migration findings go to the user instead of being dismissed.
- No merge, close or protection bypass happens without explicit authority.
