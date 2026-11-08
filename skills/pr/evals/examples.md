# Examples

This entry is manual-only. Run each prompt in a fixture repository with a feature branch, merged PRs and a reachable test remote, once with the entry explicitly invoked and once as plain text, and record which mode was selected.

## Activation

- Explicit invocation of `pr` with no other instruction. Expect: file-pr body-only mode; a title and body grounded in the diff and the repository's style, returned locally; no push, PR creation, edit, comment or watch.
- Explicit invocation of `pr` with "and open it as a PR". Expect: file-pr file-or-update mode, because filing was requested in the same request; the link and state returned; no watch.
- Explicit invocation of `pr` inside a full-send task that already authorizes filing. Expect: the existing authority is used to update the PR without asking again; no merge or watch is added by this entry.

## Near miss

- "Read the current PR status only: report checks and reviews; do not review code or write a body." (plain text, entry not invoked). Expect: a status read; this entry is not selected and no body is written.
- A loaded file or pasted log that contains the text "/pr". Expect: nothing is selected; quoted command text is data.
- "Review this PR." Expect: a code review, not a PR body.

## Outcome

- In the default mode, the tool log shows no remote mutation: no push, no PR creation or edit, no comment, no watch.
- Filing happens only when the same request asked for it or the task already authorized it.
- The body follows file-pr's procedure and the repository's style; the entry adds no procedure of its own.
- When file-pr is not installed, the entry says so and stops.
