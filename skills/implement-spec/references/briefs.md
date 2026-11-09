# Worker and reviewer briefs

Read this when briefing a ticket worker, a reviewer or a re-reviewer. These are the run-specific parts; the `agent-briefing` skill's template and checker supply the rest of every brief. Adapted from Superpowers' implementer, task-reviewer and re-review prompts.

## Contents

- [Worker](#worker)
- [Reviewer](#reviewer)
- [Re-reviewer](#re-reviewer)

## Worker

Add these to the brief:

- **Requirements by pointer.** The spec path and hash, the ticket ID and its exact text location, and "read this first: it is your requirements, with the exact values to use verbatim". Exact values (numbers, strings, signatures, test cases) appear only in the ticket or spec, never retyped.
- **What the ticket cannot know.** Interfaces and rulings from earlier tickets that this one consumes, your resolution of any ambiguity you noticed, and a pointer to any parked finding in the area. Never paste accumulated history of earlier tickets.
- **Checkout.** The integration branch revision its checkout is based on; the worker confirms that base before starting and reports it.
- **Skills.** The `implement` skill, which uses the `tdd` and `change-review` skills.
- **Leaf contract.** "Do all of this ticket's work yourself. Do not start subagents, and never start a reviewer: review is the coordinator's, after your report. Self-review means reading your own diff with the `change-review` rubric."
- **When to escalate.** Return BLOCKED or PARTIAL, with what you tried and what you need, when the ticket needs an architectural choice with several valid answers, the code needed is beyond what you can find, or the ticket restructures code in ways it did not anticipate. Bad work is worse than no work.
- **Test runs.** Run the focused test while iterating and the project's relevant suite once before committing; report any failure you saw, including ones you did not cause.
- **Report.** Write the full report to the given path: what was built, the Proof command and observed result, the red and green evidence when the ticket used test-first work, files changed, self-review findings and concerns. Return only status, commits, a one-line test summary, concerns and the report path.
- **After review findings.** When resumed with findings, fix them, rerun the covering tests, and append the command and output to the same report file.

## Reviewer

A ticket reviewer gets the brief, the worker's report, a review package for the exact range (commit list, stat and the diff with context in one file), and the binding constraints copied verbatim from the spec. Add these to the brief:

- **Read-only.** Do not change the working tree, index, HEAD or branches. Do not start subagents or a second reviewer; review a large diff in passes and say so.
- **Do not trust the report.** It is a set of claims, including its design rationales; a stated rationale never lowers a finding's severity.
- **Scope.** Read the package once. Inspect code outside the diff only to check a named risk, such as a changed contract, lock order or shared state, and name the risk and what you checked. Report a requirement that lives in unchanged code as "cannot verify from diff" rather than widening the search.
- **Tests.** The worker's report is the test evidence. Run a focused test only when the code raises a specific doubt no existing run answers; recommend heavier validation instead of running it. Noise in reported test output is a finding.
- **Spec compliance.** Missing requirements, extra unrequested work, and misunderstood requirements, each with file:line.
- **Quality.** Behavior and edge cases, error handling, tests that check real behavior, one clear responsibility per file, and what this change added to file size. Grade by impact: Critical, Important (the ticket cannot be trusted until fixed), Minor. A defect the ticket mandates is still a finding, labelled ticket-mandated.
- **Output.** Start with the spec verdict, then strengths, then findings by severity with file:line and why each matters, then the quality verdict. No preamble.

## Re-reviewer

A re-reviewer gets the ticket, the open findings verbatim with their IDs, the appended report, and a package for the fix range only. It verdicts each finding ADDRESSED or NOT ADDRESSED with file:line evidence ("attempted" is not addressed), lists new breakage the fix introduced with severity, and lists anything outside the fix range under out-of-scope observations, which never block the ticket. The same read-only, no-subagent and test rules apply.
