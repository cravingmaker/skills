# Examples

Run each prompt with and without this skill. Record the observed behavior against the expectation.

## Activation

- "Implement ticket #42 from the tracker." Expect: fetches the ticket and states its title, reuses the approved spec decisions, uses the `tdd` skill at the agreed seam, runs checks, self-reviews with the change-review rubric and reports the Proof result.
- "Build ticket T3 against the spec at docs/specs/export.md (sha256 …). You are a leaf." (a coordinator's worker brief) Expect: builds only T3, self-reviews, returns COMPLETE with evidence, and starts no reviewer or other agent.
- "Implement the agreed refactor: merge the three validators into one module." Expect: pins current behavior before moving code, migrates controlled callers in the same change, and preserves exact values and rationale comments.

## Near miss

- "Implement the whole spec and all its tickets." Expect: graph-wide work within the existing execution and tracker authority, not one leaf slice; the manual `implement-spec` entry is tested only when explicitly invoked.
- "Should we split this module? Give me options." Expect: design discussion (the `architect` or `codebase-design` skill), not implementation.
- "Fix this crash; I don't know why it happens." Expect: the `diagnosing-bugs` skill first.

## Outcome

- A leaf worker returns evidence and never starts a second controller or an independent reviewer.
- Commits happen only when committing is within the task's authority; push, PR and tracker updates need their own authority.
- The diff contains only the slice: cleanup is limited to lines the agent introduced, and defensive checks at real trust boundaries and others' work are kept.
