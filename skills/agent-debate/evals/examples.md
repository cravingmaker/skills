# Examples

Run each prompt with and without this skill, with the same host, models, fixture, and standing communication contract. Record the observed behavior against the expectation.

## Activation

- "Have Claude and Codex debate whether this service should use a queue or a cron job, then bring me the result." Expect: the frame, rubric, and budget are on disk before the first dispatch; two blind first positions are saved raw with their lens and model; the disagreements are typed; the final report leads with the recommendation and lists any open decision with both positions.
- "Get an independent second opinion on this migration plan from a different model before I apply it." Expect: one evaluator from a different model family than the plan's author, without new drafting participants, briefed from `assets/evaluator-brief.md`; the raw report passes `scripts/check-review.py`; every finding has a logged disposition with evidence.
- "Keep reviewing the draft with the evaluator until you both fully agree." Expect: the per-finding round limit still applies; a finding open after 3 rounds without new evidence goes to the user as a decision with both positions, and the report does not call it agreement.

## Near miss

- "Review this diff for bugs." Expect: a single code review; no participants, rounds, or verdict ceremony unless the user asks for agents.
- "Argue against my plan to rewrite the CLI in Rust." Expect: the agent challenges the user directly; no other agents are launched.
- "Which of these two regular expressions is faster on this input?" Expect: a benchmark is run and its numbers reported; no debate.

## Outcome

- Invoked directly with an existing fleet ledger, blind positions and evaluator starts consume the same allowance; an occupied shared pool queues the next run, and missing required budget support stops dispatch.

- `tests/agent-debate/run.sh` passes: the checker accepts well-formed reports and rejects two verdict lines, a verdict whose counts do not match, `FULL AGREEMENT` with open findings, a duplicate ID, an invalid severity, a missing or unlabeled evidence line, a missing `Change:` line, a dropped prior finding, and a finding past its round limit without `Extension:`.
- Given two participants who agree on a claim that one executed check disproves, the result follows the check, and the report names the overturned claim.
- Given an evaluator round where every finding is accepted, the log shows a source verification for each acceptance, and the report states the acceptance rate.
- Given a finding the coordinator rejects with counter-evidence, the rejection is logged with that evidence, and the next round's brief carries it to the evaluator.
- Each round's record states the artifact's net size change, and the final report states rounds and evaluator starts spent against the budget.
- Given an abstract migration plan with nothing built yet, each hypothesis-only finding becomes a spike task that runs its check instead of a second round; `check-review.py --round 2` rejects a carried finding whose only evidence is a hypothesis.
- Scheduling a spike preserves the unresolved finding ID; full agreement waits for evidence or an authorized scope withdrawal with its reason. A later review keeps the original ID and cites the new evidence.
