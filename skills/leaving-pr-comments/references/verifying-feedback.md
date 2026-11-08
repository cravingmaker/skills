# Verifying feedback

Read this when a review comment looks wrong, unclear or larger than the change needs, and you are deciding whether to fix, push back or ask.

Code review needs technical evaluation, not social performance: verify before implementing, ask before assuming, and put technical correctness over comfort.

## The pattern

1. **Read** the complete feedback before reacting.
2. **Understand** it: restate the requirement, or ask.
3. **Verify** it against the codebase as it is.
4. **Evaluate** it: is it technically sound for this codebase?
5. **Respond** with a technical acknowledgment or reasoned pushback.
6. **Implement** one item at a time, testing each.

## By source

- **From the user:** trusted. Implement after understanding, still ask when the scope is unclear, and skip straight to action or a technical acknowledgment.
- **From another reviewer or a bot:** check it is correct for this codebase, that it does not break existing behavior, why the current implementation exists, that it works on every supported platform and version, and that the reviewer had the full context. If you cannot verify it, say what you would need: "I can't verify this without X. Should I investigate, ask, or proceed?"

## When to push back

Push back when the suggestion breaks existing behavior, the reviewer lacks context, it adds an unused feature, it is technically wrong for this stack, legacy or compatibility reasons exist, or it conflicts with the user's architectural decisions. Use technical reasoning, specific questions and references to working tests or code. Involve the user when the question is architectural.

## Examples

Legacy code a reviewer wants removed:

> Reviewer: "Remove legacy code."
>
> Reply: "Checked: the build target is 10.15+, and this API needs 13+, so the legacy path is still needed for backward compatibility. The current implementation has the wrong bundle ID, though. Fix that, or drop pre-13 support?"

A feature nobody calls:

> Reviewer: "Implement proper metrics tracking with a database, date filters and CSV export."
>
> Reply: "Searched the codebase: nothing calls this endpoint. Remove it instead? Or is there a caller I'm missing?"

Several items, some unclear:

> User: "Fix items 1–6."
>
> Reply: "Fixing 1, 2, 3 and 6. Items 4 and 5 are unclear: does 4 mean the retry limit or the timeout?"

A correction after your own pushback:

> Reply: "You were right: I checked X and it does Y. Fixing it now."

## Common mistakes

| Mistake | Fix |
| --- | --- |
| Agreeing before checking | State the requirement, or just act after verifying |
| Implementing blindly | Verify against the codebase first |
| Batching untested fixes | One at a time, test each |
| Assuming the reviewer is right | Check whether it breaks things |
| Avoiding pushback | Technical correctness over comfort |
| Implementing a partly understood set | Clarify the related items first |
| Proceeding without verification | State the limitation and ask for direction |
