# Sources and policy limits

Accessed 2026-11-08.

- **Task shape.** [Anthropic, Building effective agents](https://www.anthropic.com/research/building-effective-agents), published 2024-12-19, recommends simple solutions and distinguishes sequential, routing, parallel, and orchestrator-worker patterns; it supports selecting coordination by the problem's shape, not a compulsory team.
- **Delegation and context.** [Anthropic, How we built our multi-agent research system](https://www.anthropic.com/research/multi-agent-research-system), published 2025-06-13, describes independent research, context compression, clear task boundaries, and the costs of shared context and many dependencies; its measured gains concern that research system and are not a promise for this skill.

The four delegation reasons, eight-run ceiling, finite total-start limit, ownership rules, accounting definitions, and JSON contract are local operating policies from the agreed fleet design. They are original instructions, not copied upstream skill text or empirically optimal numerical settings. The script checks recorded structural invariants; actual authorization, usefulness, active runs, resource conflicts, and integrated behavior need separate evidence. Host capabilities are discovered live; this skill asserts no fixed host API, model list, or vendor concurrency default.
