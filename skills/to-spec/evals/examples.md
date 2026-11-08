# Examples

Run each prompt with and without this skill after a conversation that settled a feature, in a fixture repository with `docs/agents/issue-tracker.md` (local tracker) and `docs/agents/domain.md`. Record the observed behavior against the expectation.

## Activation

- "to-spec" after a finished grilling session about saved searches. Expect: a spec written at the configured local path, with numbered stories, each with acceptance and a proof on the real surface; no new interview.
- "Write up what we agreed as a spec, but just give me a draft; don't file it." Expect: the spec returned in the conversation; no tracker write.

## Near miss

- "Grill me on the saved-searches idea first." Expect: the `grilling` skill; no spec.
- "Break this spec into tickets." Expect: the `to-tickets` skill; the spec is not rewritten.
- "Write a requirements document that reconciles the contract, the regulation, and the support tickets." Expect: no ordinary engineering spec; this is a multi-source obligation reconciliation task.

## Outcome

- No question is asked about anything the conversation already settled, and the agreed scope is preserved.
- Every user story has an acceptance line and a proof naming a real surface and an observable result.
- The Sources section binds each relied-on file by SHA-256.
- The spec lands only at the destination the tracker setup names, or is returned as a draft when the user asked for one or setup is missing; nothing is implemented.
- A draft-only request writes neither a local tracker file nor a remote issue unless the user explicitly named a path for that draft. A filed spec with open questions or unconfirmed testing seams stays in draft state and receives no ready-for-agent label.
