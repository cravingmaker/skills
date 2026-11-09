# Examples

Run each prompt with and without this skill. Record the observed behavior against the expectation.

## Activation

- "Fix the empty-email bug test-first." Expect: writes a focused test at the form's public seam, runs it and quotes a failure that shows the predicted mismatch, makes the minimal fix, then runs the project's suite.
- "Let's do red-green-refactor on the discount calculator." Expect: proposes seams with catch/miss notes and confirms them with the user, then works one vertical slice at a time.
- "Implement ticket 4 test-first; seams were not specified." (sent to an unattended worker) Expect: picks the highest existing seam that reaches the behavior, records it in the report, and proceeds without waiting for confirmation.

## Near miss

- "Write a test strategy for our payments service." Expect: the skill does not load; test planning (the engineering testing-strategy skill) fits.
- "Bump the timeout constant from 30 to 60 seconds." Expect: no new test is written for a trivial config value; the change is made and checked.
- "Why is this test flaky?" Expect: diagnosis (the `diagnosing-bugs` skill), not a TDD loop.

## Outcome

- The red step fails for the behavior, not for a syntax, import or setup error, and the report quotes that failure; a test that passed first is reported as a finding.
- No existing code is deleted to restart test-first, no assertion is weakened, and no failing commit is pushed to prove red.
- When only a bad test is possible, the report says so and names the closest executable check used instead.
