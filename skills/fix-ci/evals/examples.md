# Examples

Run each prompt with and without this skill against fixture PRs on a test remote: one with a real code failure, one with a failure in untouched code on a stale base, one that flakes once, and one whose job never started because of a billing limit. Record the observed behavior against the expectation.

## Activation

- "CI is red on my PR, fix it." Expect: the run, attempt, head and first causal error recorded; the cause classified with evidence; the smallest fix for a code failure; the required checks re-read at the new head.
- "The lint job failed on main after my merge." Expect: the failing run bound to the current head of main, the first causal error read from the log, and a focused fix.
- "Why did the build check fail? It worked yesterday." Expect: a stale base or flake checked before any edit; no code change unless the cause is in the diff's code.

## Near miss

- "This unit test fails on my machine." Expect: local debugging through the `diagnosing-bugs` skill or the host's debug command; no CI run binding.
- "Speed up our CI pipeline." Expect: pipeline optimization work, not failure triage.
- "Write a GitHub Actions workflow that runs the tests." Expect: workflow authoring; no failure classification.

## Outcome

- A job that never started because of billing or quota produces a report with the evidence and no code edits.
- A failure in code the diff never touches is checked for a stale base before being called a flake.
- A flake gets at most one fresh workflow run; an identical second failure is reclassified, not retried.
- The report names the run ID, attempt and head SHA, and quotes the first causal error.
- No required check is marked optional, no hook is skipped, and no assertion is loosened just to pass.
- "All green" is claimed only after every required check at the current head was observed.
