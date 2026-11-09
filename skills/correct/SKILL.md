---
name: correct
description: Turn a repeated agent mistake into a check that fails, at the highest layer that can hold it (architecture, then types, then lint, then tests, docs last), and prove the check catches the real past mistake. Use when the user corrects the same mistake again, says it keeps happening, or asks to make a mistake impossible to repeat.
license: MIT
metadata:
  source: https://github.com/cursor/plugins/tree/6b0300214a09fd6029cfb7077043125758cd1fd2/pstack/skills/correct
  source-revision: 6b0300214a09fd6029cfb7077043125758cd1fd2
  source-license: MIT, see LICENSE-pstack
  source-files: "pstack/skills/correct/SKILL.md"
  local-changes: "Preserved evidenced recurrence, current authority and the smallest enforcement hierarchy; placed judgment rules in change-review standards with bad/good examples and repeat proof; retained compatible encode-lessons methods without history sweeps or automatic commits."
---

# Correct

A **recurrence** is a mistake that has happened at least twice: the user corrected it before, or the history shows it more than once. A correction written only in prose is skipped by the next agent; a check that fails is not. This skill turns a recurrence into the smallest structural remedy that makes the wrong change fail.

Assume the next contributor is an agent that sees only the files it opened, copies the nearest example, and takes the shortest path that compiles.

## Steps

1. **Name the recurrence** with its evidence: the earlier correction, the commit, or the review comment, and the concrete wrong change. Stay within the scope the user authorized.
2. **Pick the highest layer that holds it:**
   1. **Architecture.** Give the state one owner and the task one supported way; hide internals so the wrong import fails; replace a hand-synced list with one source of truth; delete the old way an agent would copy.
   2. **Types.** Make the wrong state impossible to write.
   3. **Lint or a CI check** whose error message names the file, type, or function to use instead. When the pattern is already common, fail only on additions.
   4. **A behavior test** that fails when the behavior breaks.
   5. **A written judgment rule,** only when no structural, static or executable check can decide it. Put it in the project standards the `change-review` skill reads, with the past failure and a valid counterexample. Use agent instructions only when no review-standard home exists and editing them is authorized.
3. **Prove the remedy.** Show it rejecting the real past mistake (or a faithful reproduction) and accepting valid code through the project check or applicable review rubric. Repeat the setup or compare the intended edit against its recorded post-edit state: it needs no further change. Keep an unavailable reject, accept or repeat check unresolved. A structural fix needs no duplicate standing instruction.
4. **Report** the recurrence, its evidence, the layer chosen, why each higher layer did not work, and the proof.

Done when the remedy rejects the historical mistake, accepts valid code, repeats without a further content change, and is enforced by the project's standard check or review.

Commits, history-wide sweeps for other mistake classes, and edits to agent instruction files happen only when the user asks for them.

Per-file provenance: [references/SOURCES.md](references/SOURCES.md).
