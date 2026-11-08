# Issue tracker: GitLab

Seed for `docs/agents/issue-tracker.md`. Replace the project example with the configured identity and preserve existing custom operations.

Project: `<host>/<group>/<project>`.

Issues and specs live in that project's GitLab Issues. Use sufficient connected GitLab tools first. Where needed, use supported CLI/API equivalents after checking the installed tool's help and access.

## Operations

- **Read.** Fetch an issue's project-local number, title, complete description, state, labels, and relevant notes.
- **List.** Scope by project, state, and configured labels. Follow pagination before claiming complete coverage.
- **Publish.** Create a GitLab issue only when publication is authorized. A draft can remain local.
- **Comment, label, or close.** GitLab calls comments notes. Use supported operations and record the explanation before closing when the flow requires one.
- **Parent and blockers.** Prefer native relationships when available in this project. Otherwise keep `Part of #<parent>` in the child and an unambiguous `Blocked by: #<n>, #<n>` or `Blocked by: None` line. Confirm current support before choosing native blocking links.

Issues and merge requests have separate number spaces. Preserve project identity and the surface type when resolving a reference.

## Merge requests as a triage surface

**MRs as a request surface: no.**

Set this to yes only when the project's triage contract includes external merge requests. In that mode, read the description, diff, notes, and review state; use the configured labels and existing authority.

## Wayfinding operations

Use one issue as the map, or the project's established epic convention. The map carries Notes, Decisions-so-far, and Fog. Children name their map and type: `research`, `prototype`, `grilling`, or `task`. The configured label may be `wayfinder:<type>`.

Keep decision tickets distinct from delivery tickets. Select the first map-ordered child with no incomplete blocker or claimant. Preserve existing assignments; claim only within current authority.

Record the resolved question's answer and evidence, then its configured completion state and a gist plus link in the map. A decision answer does not authorize implementation or closing delivery tickets.
