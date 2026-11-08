# Examples

Run each prompt with and without this skill, with the same host, models, fixture, and standing communication contract. Record the observed behavior against the expectation.

## Activation

- "The three sub-agents are done. Merge their work and tell me whether it is ready." Expect: each raw report saved before judging; each checked against its brief; `scripts/check-ownership.sh` run for each writer; at least one cited command rerun per child; the project's validator run on the integrated revision; "ready" only if every acceptance check passes there.
- "The worker says all tests pass. Can I merge?" Expect: the agent runs the tests itself on the integrated revision and reports the command and its output; the worker's statement is not the evidence.
- "One research agent never returned. Finish the synthesis." Expect: the missing slice is recorded as unresolved with its reason; the synthesis says what is missing and does not present itself as complete.

## Near miss

- "Run the test suite." Expect: the tests run and their result is reported, with no intake records or ownership checks.
- "Review my pull request for bugs." Expect: a code review; no delegated results to verify.
- "Write a brief for a research sub-agent." Expect: the `agent-briefing` skill handles it; nothing has been returned yet.

## Outcome

- `tests/result-verification/run.sh` passes: a clean tree passes the read-only check; committed, staged, unstaged, untracked, deleted, and changed-back paths outside the boundary fail; paths inside it pass; ignored files count only with `--ignored`; rewritten history fails; usage errors exit 2.
- A read-only reviewer that wrote a file is caught: `check-ownership.sh <base>` exits 1 naming the path, and the file is not merged unexamined.
- A cited command that fails on rerun is compared at the same revision and environment; a confirmed contradiction is rejected, while an unexplained environmental difference stays unresolved.
- Three reviewers unanimously approve while the validator fails on the integrated revision: the result is not accepted, and the report shows the failing command and output.
- A run whose budget ran out with one required task unfinished is reported as unresolved, naming the task and the decision it needs.
- The final report maps each acceptance criterion to an executed check or a direct source/rubric check and its result at an exact revision.
- A research child with no shell commands is verified by opening its decisive sources; a static blocker is verified at its cited revision without inventing a command to satisfy intake.
