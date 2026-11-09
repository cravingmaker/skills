# Examples

Run each prompt with and without this skill in a fixture repository that holds the plan's code and one already-made decision in its docs. Record the observed behavior against the expectation.

## Activation

- "Grill me on this plan: move session storage from cookies to Redis before the launch." Expect: numbered rounds with a recommended answer per question; facts about the current session code are looked up, not asked.
- "Stress-test my design for the export queue before I build it. I already decided on Postgres, not SQS." Expect: the Postgres choice is listed as settled and never asked; only open consequential choices appear.

## Near miss

- "What does the session middleware do?" Expect: an explanation; no interview rounds.
- "Write the spec from what we just discussed." Expect: the `to-spec` skill's job; no new interview.
- "Rename `getUser` to `fetchUser` everywhere." Expect: the rename; no questions about design.

## Outcome

- No question asks for a fact present in the repo, the docs, or the conversation.
- No question in a round depends on another open question in the same round.
- The session stops when remaining answers would not change the plan, and the close lists settled, deferred, and next-step items.
- No project files are written by the default interview, and an explicit interview waits for the user to confirm its close before building.
- Embedded use asks only about its unresolved gap. Once the user answers that gap in an already authorized task, control returns to the caller without requiring another confirmation of the whole plan.
