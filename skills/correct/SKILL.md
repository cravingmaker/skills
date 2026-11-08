---
name: correct
description: Turn a repeated agent mistake into a check that fails, at the highest layer that can hold it (architecture, then types, then lint, then tests, docs last), and prove the check catches the real past mistake. Use when the user corrects the same mistake again, says it keeps happening, or asks to make a mistake impossible to repeat.
license: MIT
metadata:
  source: https://github.com/cursor/plugins/tree/6b0300214a09fd6029cfb7077043125758cd1fd2/pstack/skills/correct
  source-revision: 6b0300214a09fd6029cfb7077043125758cd1fd2
  source-license: MIT, see LICENSE-pstack
  source-files: "pstack/skills/correct/SKILL.md"
  local-changes: "Limited work to evidenced recurrence and authorized remedies; removed history sweeps, mandatory commits, approval and expiry ceremonies, and automatic instruction edits."
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
   5. **A rule in the agent instructions,** only for a judgment call no check can make.
3. **Prove the remedy.** Show it failing on the real past mistake (or a faithful reproduction of it) and passing on valid code. Run it through the same command the project uses locally and in CI.
4. **Report** the recurrence, its evidence, the layer chosen, why each higher layer did not work, and the proof.

Done when the remedy rejects the historical mistake, accepts valid code, and runs in the project's standard check command.

Commits, history-wide sweeps for other mistake classes, and edits to agent instruction files happen only when the user asks for them.
