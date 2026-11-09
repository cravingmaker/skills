# Examples

Run each prompt with and without this skill in a fixture repository whose `docs/agents/domain.md` names a glossary path and an ADR directory, with one accepted ADR. Record the observed behavior against the expectation.

## Activation

- "When I say 'account' here I mean the billing customer, not the login user. Let's pin that down in the glossary." Expect: the conflict with existing terms is checked, a precise term is proposed, and the glossary at the configured path is updated with `_Avoid_` variants.
- "We're switching from REST callbacks to domain events between Ordering and Billing. That reverses ADR-0003; record it." Expect: a new ADR that supersedes ADR-0003; only ADR-0003's status line changes.
- "Rename 'workspace' to 'project' everywhere users see it." Expect: the terminology sweep, with public identifiers and quoted text kept and classified.

## Near miss

- "Make this paragraph clearer." Expect: an edit of the prose; no glossary or ADR work.
- "Which logging library should we use for the CLI?" Expect: an answer; no ADR, since the choice is easy to reverse.
- "Explain what an Order is in this codebase." Expect: an explanation that reads the glossary; no writes.

## Outcome

- Glossary and ADR files are written only at the paths `docs/agents/domain.md` names, or the user gave, and never at an invented default.
- A missing configured file is created lazily, only when the first term or ADR is recorded.
- No accepted ADR text changes; a reversed decision gets a new superseding ADR.
- The glossary gains no implementation detail, and no ADR is written for an easy-to-reverse choice.
- Without a docs-recording flow or an explicit request, the skill proposes edits instead of writing them.
