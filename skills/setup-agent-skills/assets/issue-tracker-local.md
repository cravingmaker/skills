# Issue tracker: local Markdown

Seed for `docs/agents/issue-tracker.md`. The paths below are new-setup defaults; preserve the project's configured paths if they differ.

## Files and operations

- **Feature directory.** `.scratch/<feature-slug>/`.
- **Spec.** `.scratch/<feature-slug>/spec.md`.
- **Delivery tickets.** One file per ticket at `.scratch/<feature-slug>/issues/<NN>-<slug>.md`, numbered from `01`. Preserve exact ticket identities and do not combine them into a second ticket source.
- **State.** A `Status:` line uses the workflow's configured state strings. Where triage is installed, `docs/agents/triage-labels.md` maps its roles.
- **History.** Append comments under `## Comments` rather than overwriting earlier discussion.
- **Read.** Resolve the exact referenced path or ticket identity. Do not guess which similarly named spec is authoritative.
- **Publish.** Write the requested local artifact at its configured destination. Local publication grants no remote authority.

## Wayfinding operations

The decision map is `.scratch/<effort>/map.md` with Notes, Decisions-so-far, and Fog. Each decision ticket is `.scratch/<effort>/issues/NN-<slug>.md` with a `Type:` of `research`, `prototype`, `grilling`, or `task`.

Use the established decision states, including `claimed` and `resolved` when those are configured. Preserve delivery-ticket state vocabulary separately.

A `Blocked by: NN, NN` or `Blocked by: None` line names every dependency unambiguously. Select the first numbered open, unclaimed child whose blockers are all resolved. A missing or ambiguous blocker is unresolved.

Claim by recording state before work. Resolve by appending the answer and evidence under `## Answer`, setting the configured completion state, and appending a gist plus path to the map. Do not start implementation merely because a decision is resolved.
