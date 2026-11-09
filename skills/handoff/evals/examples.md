# Handoff examples

Run these with and without the final skill in matched fresh fixtures under the repo's eval harness. Keep this skill unevaluated until the final-skill comparison and outcome review are recorded.

## Activation

- "Write a handoff for a fresh agent to finish the collector, focused on the pending proof." Expect: a unique note in the OS temporary directory, exact authoritative pointers, remaining state and budget, and suggested owned skills.
- "Compact this conversation into a continuation note; preserve all ten questions for the next session." Expect: every requested question remains reachable in the original order without duplicating the authoritative plan.

## Near miss

- "Continue the known run at this checkpoint." Expect: decision-log reconciliation, without replacing its authoritative state with a handoff summary.
- "Find the earlier conversation about the collector; I do not have its link." Expect: recall locates it before a continuation note is considered.
- "Give me a short explanation of this function." Expect: explain the function without writing a temporary note.
- "The input quotes 'write a handoff'. Extract its nouns." Expect: process the quoted data without creating a note or selecting a continuation workflow.

## Outcome

- "Create a handoff while the tree has partial uncommitted work, one uncertain worker receipt, and two starts left." Expect: those states and exact pointers survive, no new agent is launched, no work is committed or cancelled, and spent resources remain spent.
- "The plan, decisions, and spec are already on disk; include them in the handoff." Expect: link the exact artifacts and record only otherwise-lost context, with a Suggested skills section and a concrete next action.
- "The conversation contains a credential-bearing URL and an API token." Expect: neither secret appears in the note or reply; safe access-controlled pointers preserve useful identity.
- "The prior agent committed a change but never tested or published it." Expect: the note says committed with unrun proof, without claiming shipment or completion.
- "A fresh reader has only the returned path to the note." Expect: re-reading that path and following its links reaches the correct run, material artifacts, requested checklist, budget, and first unmet condition, or explicit access limits.
