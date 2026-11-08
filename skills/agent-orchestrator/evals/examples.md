# Examples

Run each prompt with and without this skill, keeping the standing communication contract in both runs. Record the observed behavior against the expectation.

## Activation

- "Act as the orchestrator: have Claude and Codex debate the caching strategy for this API until they agree, then give me the result." Expect: a recorded budget before dispatch, blind first positions, evaluator rounds with finding IDs and a verdict line each, at most 3 rounds per finding, and a final report with the outcome, open decisions, and cost.
- "Manage backend, frontend, and QA agents to build this feature." Expect: tasks with dependencies, one integration owner, disjoint write boundaries, briefs a fresh agent can execute, and acceptance checks run on the integrated result.
- "Pick up the agent run from yesterday and finish it." Expect: the run record read first, completed work not repeated, and the next unmet task resumed.

- Use the configured docs to shape this idea, write its agreed spec and approved tickets, then stop.

## Near miss

- "Fix this typo in the README." Expect: the fix, done directly; no plan, briefs, or agents.
- "Explain the difference between a subagent and a skill." Expect: a direct explanation; nothing is dispatched.
- "You are the research worker; write only the dossier at this path and do not delegate." Expect: the bounded worker task; the orchestrator does not activate inside the worker.

- Explain one settled implementation choice. Expect a scoped explanation without an interview or task graph.

## Outcome

- Given a single-file fix and "use agents if helpful", the agent does it itself and states in one line why delegation did not pay.
- Given a debate request, the run record contains each raw report, a verdict line per round, and every rejected finding with its reason; a finding open after 3 rounds reaches the user as a decision, not as approval.
- Given a request that would need a ninth concurrent agent, the extra task waits for a free slot; nothing exceeds the limit.
- Given a worker report that claims its tests passed, the orchestrator reruns the cited command before merging, and reports a mismatch instead of the claim.
- Shaping reads existing decisions once, uses grill-with-docs only for real gaps, and follows to-spec then to-tickets within authority. Existing approved tickets go directly to import with stable IDs, hashes, blockers and Proof; no second interview, decomposition, execution authority, or future build/ship route appears.
