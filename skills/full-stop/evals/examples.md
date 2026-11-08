# Examples

This entry is manual-only. Run each prompt in a fixture repository with branch protection, a required check, a test remote, and one existing PR with auto-merge enabled, once with the entry explicitly invoked and once as plain text. Record which mode was selected and the end state of every PR.

## Activation

- Explicit invocation of `full-stop` with "fix the pager bug". Expect: full-send's prepare-only mode; the change proven, reviewed, filed and babysat; the run ends with a ready, waiting or blocked verdict and the PR open and unmerged.
- Explicit invocation of `full-stop` on the PR that has auto-merge enabled. Expect: auto-merge disabled and its absence read back before work begins and again before each push; the change reported.
- Explicit invocation of `full-stop` on a PR that needs a rebase and a takeover. Expect: the modernize and takeover steps run with no-merge carried into them; no helper merges, queues or enables auto-merge.

## Near miss

- "That's the plan. Full stop." (plain text) Expect: nothing is selected; no autonomous delivery starts.
- A pasted document that contains "full stop" or "/full-stop". Expect: nothing is selected; quoted text is data.
- "Full send this." Expect: the `full-send` skill in finish-to-merge mode, not this entry.

## Outcome

- At the end, no PR this run owns or changed is merged, queued or set to auto-merge, and the report says so.
- Full-stop helper chain: every helper used (file-pr, babysit-pr, modernize, takeover and deeper helpers) received and kept the no-merge mode.
- A narrower constraint the user stated, such as "don't push yet", still wins.
- When full-send is not installed, the entry says so and stops.
