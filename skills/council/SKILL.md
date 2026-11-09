---
name: council
description: Explicit council entry for a requested provider panel. Dispatch code review and fixes, design deliberation, or a read-only panel while preserving the requested scope.
license: MIT
metadata:
  source: "https://github.com/t3dotgg/tstack/blob/1085050f3baed1ac724caa4a8166145fb2ac88af/skills/council/SKILL.md"
  source-revision: "1085050f3baed1ac724caa4a8166145fb2ac88af"
  source-files: "skills/council/SKILL.md"
  local-changes: "Replaced the unconditional code-fix loop with thin scoped dispatch; retained distinct requested providers, declared budgets and honest unavailable seats; removed automatic PR edits and fixed models."
  requires: "sol-loop agent-debate"
---

# Council

On explicit user invocation, read the `sol-loop` skill and the `agent-debate` skill; if a required skill is missing, name it and stop this flow. Dispatch an authorized code review/fix loop to the `sol-loop` skill in council panel mode; dispatch design or other non-code deliberation to the `agent-debate` skill in panel mode. A read-only request takes precedence: code opens the `change-review` skill through the required closure in report-only panel mode; non-code uses the `agent-debate` skill as a report-only panel. Preserve requested distinct providers, stable finding IDs, scope, and the coordinator's declared round/start budget; report an unavailable member without substitution. The selected parent owns the procedure; quoted or incidental council text selects nothing, and this entry adds no fix, posting, push, or merge authority.

Read [references/SOURCES.md](references/SOURCES.md) when checking attribution and source identity.
