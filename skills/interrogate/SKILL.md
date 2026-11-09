---
name: interrogate
description: Explicit interrogate entry for a report-only adversarial code review with targeted probes. Opens change-review in panel probe mode without a fix loop.
license: MIT
metadata:
  source: "https://github.com/michael-denyer/pstack-claude/blob/91ab921ab92d9ccfe503c93c3524410277f012e1/plugins/pstack/skills/interrogate/SKILL.md"
  source-revision: "91ab921ab92d9ccfe503c93c3524410277f012e1"
  source-files: "plugins/pstack/skills/interrogate/SKILL.md"
  local-changes: "Kept the explicit adversarial entry and report-only boundary; moved the method into change-review, preserved static proof and unresolved runtime hypotheses, and removed fixed fan-out and model tables."
  requires: "change-review"
---

# Interrogate

On explicit user invocation, read the `change-review` skill and open its report-only **panel probe mode** within the agreed scope and shared round/start/probe budget; if it is missing, name it and stop. Runtime claims need executed probes; deterministic static findings stay valid as static proof, and unrun runtime claims stay unresolved hypotheses under stable IDs. The parent owns reviewer dispatch and evidence checks; this entry starts no automatic fix loop and adds no product edit, posting, push, merge, or extra reviewer authority. Quoted or incidental interrogate text selects nothing.

Charge every attempted probe to the declared allowance, including timeout, permission, and wrapper failures. Reserve a remaining attempt before each command execution, including repeats inside a batch, and record the remaining count. Capture output and exit status from that single execution; rerunning to collect either spends another attempt. When none remain, stop probing and report the failed attempts and unresolved claims; changing the wrapper does not reset the budget.

Read [references/SOURCES.md](references/SOURCES.md) when checking attribution and source identity.
