# Coverage

Every job the collection covers, mapped to the skills that cover it. Status: shipped or deferred.

Coverage rows describe scope; only `metadata.requires` defines installation edges. Optional routes are conditional prose pointers checked against shipped names or the supported external inventory.

| Used by | Job | Capabilities | Upstream providers | Status |
| --- | --- | --- | --- | --- |
| agent-orchestrator | Manage other agents like a product or project manager | `agent-orchestrator` (router), `work-decomposition`, `agent-briefing`, `result-verification`, `decision-log` | none | shipped |
| agent-orchestrator | Agents discuss and debate to find the best approach | `agent-debate`, `decision-log` | none | shipped |
| all | Clear, lean communication in both directions | `clear-communication` | none | shipped |
| all | An enforcement environment that makes work right by construction | `project-guardrails`, `toolchain-upgrade`, `correct` | none | shipped |
| agent-orchestrator | Shape an idea into approved, source-bound work | `grilling`, `grill-with-docs`, `to-spec`, `to-tickets`, `domain-modeling`, `grill-me` | none | shipped |
| agent-orchestrator | Import exact tickets and verify their actual Proof | `work-decomposition`, `agent-briefing`, `decision-log`, `result-verification` | none | shipped |
| agent-orchestrator | Configure tracker paths and triage incoming work | `setup-agent-skills`, `triage` | none | shipped |
| agent-orchestrator | Resolve an unclear destination and outside knowledge | `wayfinder`, `research`, `prototype`, `to-questionnaire` | none | shipped |
| all | Explain mechanism and intent, refine a prompt, repair an unclear answer | `how`, `why`, `sharpen`, `bro`, `wait-what`, `clear-communication` | none | shipped |
| agent-orchestrator | Run approved code tickets through one coordinator | `implement-spec`, `implement`, `work-decomposition`, `result-verification`; shared record and budget | none | shipped |
| all | Deep modules, design alternatives and architecture reports | `codebase-design`, `architect`, `improve-codebase-architecture` | none | shipped |
| all | Build and diagnose an authorized slice | `implement`, `tdd`, `diagnosing-bugs` | none | shipped |
| agent-orchestrator | Resumable setup for human-only steps | `wizard` | none | shipped |
| all | Code review, bounded fix loops and downstream effects | `change-review`, `sol-loop`, `interrogate`, `blast-radius` | none | shipped |
| all | Explicit code, design or read-only provider panels | `council`, `sol-loop`, `agent-debate`; requested mode preserves authority | none | shipped |
| all | Comparable benchmarks and explainable numbers | `benchmark-checklist` | none | shipped |
| all | Real-surface project drivers and feature-map maintenance | `create-verification-skill`, `maintain-verification-skill`; scope and actual proof gaps decide mode | none | shipped |
| agent-orchestrator | Draft, file and continue verified PR delivery | `file-pr`, `pr`, `babysit-pr`, `leaving-pr-comments`, `modernize`, `takeover`, `full-send`, `full-stop`; root-only authorized monitoring | none | shipped |
| agent-orchestrator | CI failure triage and repair | `fix-ci`, `diagnosing-bugs`; search aliases ci-failure-triage and ci-failure-diagnosis | none | shipped |
| all | Session evidence, continuation and instruction craft | `retro`, `handoff`, `writing-for-agents`, `recall`, `decision-log`; one authoritative record | none | shipped |
| all | Grounded teaching and read-only catch-up | `teach`, `ketchup`, `clear-communication`; learning workspace and wider status window only on request | none | shipped |
