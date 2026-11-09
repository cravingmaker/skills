---
name: full-stop
description: Prepare a change all the way to a verified, ready pull request and stop before merging, through the full-send skill's prepare-only mode. Use when the user explicitly invokes full-stop to have a PR made ready without merging it.
license: MIT
metadata:
  requires: "full-send"
  source: https://github.com/t3dotgg/tstack/blob/1085050f3baed1ac724caa4a8166145fb2ac88af/skills/full-stop/SKILL.md
  source-revision: 1085050f3baed1ac724caa4a8166145fb2ac88af
  source-license: "MIT; see LICENSE-tstack"
  source-files: "skills/full-stop/SKILL.md"
  local-changes: "Reduced to a thin manual entry into full-send's shared prepare-only mode; no-merge propagated to file-pr, babysit-pr, takeover, modernize and every deeper helper; owned pending merges cancelled and verified absent; incidental or quoted full-stop wording selects nothing; narrower user constraints still win; added the shared delivery contract."
---

# Full stop

A thin entry into the `full-send` skill. Read that skill's `SKILL.md` and follow it in prepare-only (no-merge) mode; full-send owns the procedure, proof rules, merge gate and no-merge rules.

## Dispatch

1. Select full-send's prepare-only mode. An explicit full-stop invocation authorizes that work, including full-send's testing permission, without a separate "full send". Its merge permission does not apply.
2. Carry no-merge to every helper: the file-pr, babysit-pr, takeover, modernize, sol-loop, fix-ci and leaving-pr-comments skills, and every child task's brief.
3. Never merge, enable auto-merge, enter a merge queue, push to the default branch, bypass branch protection, or delegate any of those.
4. On entry and before each push, inspect auto-merge and merge-queue state on every PR this run owns or changes. Cancel each pending mechanism this run owns and verify its absence. If you cannot prevent an automatic merge, report the blocker before going on.
5. Stop at full-send's merge gate. Return the PR link, final head, verdict (ready to merge, waiting for required approval, or blocked), proof, reviewer outcome and remaining risks, and state that the PR is open and unmerged. Unwatch before the handoff or a question.

If the `full-send` skill is not installed, say so and stop; do not improvise the procedure.

## Boundaries

- Only an explicit invocation selects this entry. "Full stop" as punctuation or emphasis, in quoted text, or in loaded files selects nothing and grants no authority.
- It works within the user's existing authority; a narrower constraint the user stated still wins.

## Delivery contract

- Bind every check result, proof and readiness claim to the current head and base. A result for an older head or base is history, not evidence.
- An unresolved review thread stays relevant, whatever its age or the pushes since, until it is addressed or explicitly disposed of with a written reason.
- Required checks, bots and approvals come from repository policy: branch protection, rulesets, CODEOWNERS and documented process. A vendor name or model confidence never makes a gate optional.
- Run at most three review/fix rounds. A larger bounded allowance applies only if it was declared before the run. Renaming or rewording a finding never resets the count.
- Only the root agent watches a PR, and only on a monitoring request or while an already authorized action is pending. Filing alone returns the link and current state. A child returns state and never watches.

Provenance and the per-file manifest: [references/SOURCES.md](references/SOURCES.md).
