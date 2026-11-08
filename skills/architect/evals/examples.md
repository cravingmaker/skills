# Examples

Run each prompt with and without this skill. Record the observed behavior against the expectation.

## Activation

- "Architect this: we need a rate limiter shared by the API and the job runner. Sketch it before writing code." Expect: grounds in the existing code, writes caller usage first, produces at least two structurally distinct candidates, screens them against the red flags, and records a chosen design with a rationale; no implementation.
- "Design the interface for the new plugin loader; it's consequential, so get independent alternatives." Expect: declares a design budget and uses the `agent-debate` skill for blind candidates rather than copying an arena process; the synthesis section records the base, grafts and rejections.
- "We've added three special cases to the sync engine this week; is the design wrong?" Expect: checks the Phase E pattern tells against evidence, and presents any redesign as a proposal within scope, not an automatic rewrite.

## Near miss

- "Write an ADR comparing Kafka and SQS for our event bus." Expect: the skill does not load; an architecture decision record (the engineering architecture skill or the `domain-modeling` skill) fits.
- "How should we architect a globally distributed video platform?" Expect: system design (the engineering system-design skill), not an interface sketch.
- "Rename this function and update its callers." Expect: no design artifact; ordinary editing.

## Outcome

- The design artifact contains caller usage, a type sketch with `not implemented` bodies, at least one rejected alternative with its reason, and accepted trade-offs; it stops before code unless implementation was authorized.
- Candidates written by one agent in sequence are labelled sequential, not independent; no hidden parallel sketches are started outside the shared budget.
- No model slugs, runner sheets or mandatory tournaments appear; blind comparison goes through the `agent-debate` skill only when it pays.
