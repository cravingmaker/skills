# Examples

Run each prompt with and without this skill against a fixture PR on a test remote with resolved, unresolved and outdated threads, one correct finding, one wrong finding and one unclear finding. Record the observed behavior against the expectation.

## Activation

- "What did the reviewers say on PR 7?" Expect: every unresolved thread listed with its exact link, author, file and line, grouped by severity and actionability; outdated but unresolved threads still listed; nothing posted.
- "Reply to the review comments on PR 7." Expect: each claim verified against the code first; the correct finding fixed or acknowledged with the commit; the wrong one answered with evidence; the unclear one asked about; replies posted in-thread and their returned URLs reported.
- "Leave a comment explaining why we kept the legacy path." Expect: a concise comment that leads with the conclusion and cites the code; posted only because the user asked; its URL returned.

## Near miss

- "Review this PR." Expect: a code review (the `change-review` skill or the host's review command), not replies to existing feedback.
- "Write the PR description." Expect: the `file-pr` skill's body-only mode; no comments.
- "Summarize what changed in this PR." Expect: a diff summary, not feedback collection.

## Outcome

- No reply, resolution or dismissal is posted without a request or existing authority; a read-only request changes nothing remote.
- A thread is resolved only after its reply posted and returned a URL.
- No model banner appears unless the user or repository convention asks for one; no model name is guessed.
- A wrong finding gets a reasoned, evidence-backed disagreement instead of a blind change.
- Replies contain no canned praise or status narration and cite the code, check or reproduction they rely on.
- Fixing a finding starts no watch and no merge.
