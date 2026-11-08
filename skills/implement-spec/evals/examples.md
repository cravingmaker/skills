# Examples

Run each prompt with and without this skill. Record the observed behavior against the expectation.

## Activation

- "Implement the approved spec docs/specs/sync.md and its five tickets." Expect: imports the tickets with their IDs, blockers and Proof through the work-decomposition importer without re-decomposing, records the run and budget, starts only the ready frontier, and accepts each ticket on rerun Proof before closing it.
- "Resume the implement-spec run for the sync spec." Expect: reads the run record, confirms the spec hash, skips accepted tickets and resumes mid-loop tickets at their next round.
- "Run the tickets from to-tickets, but at most two agents at a time." Expect: records a concurrency ceiling of two (below the eight-agent cap) and every start, review and retry against one budget.

## Near miss

- "Implement ticket #12." Expect: one ticket goes to the `implement` skill, not the graph runner.
- "Coordinate three agents to research database options and debate them." Expect: non-code coordination under the `agent-orchestrator` skill and the `agent-debate` skill, not this runner.
- "Break this spec into tickets." Expect: the `to-tickets` skill; this runner never decomposes a spec.

## Outcome

- One coordinator owns every worker, reviewer, replacement and retry start; live subagents never exceed eight or the lower host or user limit, and totals stay within the recorded budget.
- Worker briefs carry the leaf contract; no worker starts a reviewer. An inline review is recorded as a coordinator review, never as an independent panel, and an unavailable requested provider is reported, not replaced.
- A ticket with missing, stale or proxy proof, or an unresolved Critical finding at the round limit, stays open; tracker items close only after accepted worker and integration evidence.
