# Examples

Run each prompt with and without this skill. Record the observed behavior against the expectation.

## Activation

- "Debug this: the export button throws 'undefined is not a function' in production." Expect: builds a red-capable loop on the reported surface before theorizing, minimises, ranks 3–5 falsifiable hypotheses, and fixes a proven cause with a regression test at a correct seam.
- "The dashboard got twice as slow after last week's release. Diagnose it." Expect: measures a baseline on a realistic workload first, bisects or profiles, and vets numbers with the `benchmark-checklist` skill.
- "Here's a heap snapshot from prod; why is memory growing? We can't reproduce it locally." Expect: diagnoses from the capture, labels the result "from capture" with its limits, and does not call the cause confirmed without a paired capture.

## Near miss

- "Use the installed debug command explicitly." Expect: the selected host command keeps its route; diagnosing-bugs is not substituted.

- "Walk me through a structured incident postmortem for yesterday's outage." Expect: the skill does not load; incident response (the engineering incident-response skill) fits.
- "Add a retry to this HTTP call." Expect: ordinary implementation, no diagnosis loop.
- "This test fails only when run after another test." Expect: test-order pollution is specialist flaky-test work; this skill does not reproduce the polluter-bisection recipe.

## Outcome

- After two fixes sharing one premise fail, the premise is written down and tested before any third fix; a design concern is reported, not rewritten automatically.
- Shown commands and artifacts are redacted; no environment, config or transcript is dumped.
- The original un-minimised repro is rerun after the fix, debug logs are removed by their tag, and the confirmed hypothesis is stated with its evidence.
