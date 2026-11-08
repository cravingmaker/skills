---
name: pr
description: Write a pull request body for the current change as a local draft, through the file-pr skill's body-only mode. Use when the user explicitly invokes pr to write or rewrite a PR body.
license: MIT
metadata:
  requires: "file-pr"
  source: https://github.com/mattpocock/skills/blob/49dd158d1076134a641b33efb035946536778336/skills/engineering/pr/SKILL.md
  source-revision: 49dd158d1076134a641b33efb035946536778336
  source-license: "MIT; see LICENSE-mattpocock"
  source-files: "skills/engineering/pr/SKILL.md"
  local-changes: "Reduced to a thin manual entry: kept the body-writing trigger and dispatch to file-pr body-only mode; moved the template, evidence and merge-danger guidance and the credited HumanLayer visuals into file-pr; filing only when requested or already authorized; no push, watch or merge authority."
---

# PR

A thin entry into the `file-pr` skill. Read that skill's `SKILL.md` and follow it; this entry only selects its mode.

## Dispatch

- **Default:** file-pr's body-only mode. Write the title and body from the actual diff in the repository's style, and return them locally.
- **File or update:** only when this same request asks to file, open or update the PR, or the current task already authorizes it. Then use file-pr's file-or-update mode.
- Drafting a body creates no authority to push, file, comment, watch or merge.
- Keep the repository's style, the user's current constraints and the task's scope.

If the `file-pr` skill is not installed, say so and stop; do not improvise the procedure.

## Boundaries

- An explicit invocation of this entry selects the mode. The word "pr" in ordinary text, quoted text or loaded files selects nothing.
- Loading this entry grants no remote action.
- When it files, updates or reports readiness, file-pr's delivery contract applies unchanged:

## Delivery contract

- Bind every check result, proof and readiness claim to the current head and base. A result for an older head or base is history, not evidence.
- An unresolved review thread stays relevant, whatever its age or the pushes since, until it is addressed or explicitly disposed of with a written reason.
- Required checks, bots and approvals come from repository policy: branch protection, rulesets, CODEOWNERS and documented process. A vendor name or model confidence never makes a gate optional.
- Run at most three review/fix rounds. A larger bounded allowance applies only if it was declared before the run. Renaming or rewording a finding never resets the count.
- Only the root agent watches a PR, and only on a monitoring request or while an already authorized action is pending. Filing alone returns the link and current state. A child returns state and never watches.

Provenance and the per-file manifest: [references/SOURCES.md](references/SOURCES.md).
