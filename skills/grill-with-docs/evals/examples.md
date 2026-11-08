# Examples

Run each prompt with and without this skill in a fixture repository with `docs/agents/domain.md`, a glossary that defines "Order", and one accepted ADR. Install `grilling` and `domain-modeling` in both arms. Record the observed behavior against the expectation.

## Activation

- "grill-with-docs: I want to add partial order cancellation." Expect: the glossary and ADR are read first; rounds probe what "partial" means against the "Order" definition; resolved terms are written to the configured glossary.
- "Grill me on the new refund flow and keep the glossary and ADRs updated as we go." Expect: the same flow; an ADR is offered only for a hard-to-reverse trade-off.
- "grill-with-docs" in a repository with no `docs/agents/domain.md`. Expect: the missing setup is named with the `setup-agent-skills` skill as the next step, and a plain interview is offered without doc writes.

## Near miss

- "Grill me on this plan." Expect: the `grilling` skill alone; no glossary or ADR writes.
- "Turn our discussion into a spec." Expect: the `to-spec` skill; no new interview.
- "Add a feature flag for the refund flow." Expect: the change itself; no interview and no design gate.

## Outcome

- No question asks for a fact the repo, the docs, or the conversation already answers, and no settled decision is reopened.
- Glossary and ADR writes land only at the paths the domain setup names.
- Nothing blocks ordinary building: there is no design-approval gate and no second spec document.
- When a builder check runs, it runs once within the budget and its "theirs" questions arrive in one message.
