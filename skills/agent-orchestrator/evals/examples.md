# Examples

Run each prompt with and without this skill, keeping the standing communication contract in both runs. Record the observed behavior against the expectation.

## Activation

- "Act as the orchestrator: have Claude and Codex debate the caching strategy for this API until they agree, then give me the result." Expect: a recorded budget before dispatch, blind first positions, evaluator rounds with finding IDs and a verdict line each, at most 3 rounds per finding, and a final report with the outcome, open decisions, and cost.
- "Manage backend, frontend, and QA agents to build this feature." Expect: tasks with dependencies, one integration owner, disjoint write boundaries, briefs a fresh agent can execute, and acceptance checks run on the integrated result.
- "Pick up the agent run from yesterday and finish it." Expect: the run record read first, completed work not repeated, and the next unmet task resumed.

- "Act as the orchestrator: use the configured docs to shape the unsettled refund idea, then write the agreed spec and approved tickets and stop." Expect: read the existing glossary and accepted decisions, interview only the open consequential refund choices, and wait for answers before claiming a spec or ticket breakdown is agreed. No implementation or dispatch.

- Run this approved code-ticket graph at configured nondefault paths. Expect the `implement-spec` skill under the current coordinator, record and remaining budget.

## Near miss

- "Fix this typo in the README." Expect: the fix, done directly; no plan, briefs, or agents.
- "Explain the difference between a subagent and a skill." Expect: a direct explanation; nothing is dispatched.
- "You are the research worker; write only the dossier at this path and do not delegate." Expect: the bounded worker task; the orchestrator does not activate inside the worker.

- Explain one settled implementation choice. Expect a scoped explanation without an interview or task graph.

- A worker asks for its independent review. Expect a report to the coordinator, without a child controller.

## Outcome

- Given a single-file fix and "use agents if helpful", the agent does it itself and states in one line why delegation did not pay.
- Given a debate request, the run record contains each raw report, a verdict line per round, and every rejected finding with its reason; a finding open after 3 rounds reaches the user as a decision, not as approval.
- Given a request that would need a ninth concurrent agent, the extra task waits for a free slot; nothing exceeds the limit.
- Given a worker report that claims its tests passed, the orchestrator reruns the cited command before merging, and reports a mismatch instead of the claim.
- Shaping reads existing decisions once, uses grill-with-docs only for real gaps, and follows to-spec then to-tickets within authority. Existing approved tickets go directly to import with stable IDs, hashes, blockers and Proof; no second interview, decomposition or new execution authority appears. An authorized build enters the owned runner; shipping authority is preserved separately.
- Approved code tickets use exactly one runner without re-interview or decomposition. Source status, hashes, blockers and Proof survive. Every worker/reviewer/retry uses the shared budget; worker and integration acceptance precede authorized tracker closure. Design, read-only code review and authorized fix loops dispatch to their owning skills; no future delivery route is implied.
