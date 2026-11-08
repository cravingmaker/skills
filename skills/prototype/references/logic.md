# Logic prototype

Read this for state transitions, data shapes, legal actions, or behavior that needs to be tried. The artifact answers the decision stated in SKILL.md.

## Choose the smallest useful form

A single self-contained HTML file lets a non-developer press buttons and watch state change without installing a framework. A short script is enough when outputs or timing answer the question without interaction.

Keep model logic separate from presentation: a reducer, explicit state machine, pure functions, or a small module with a clear method interface. The page calls the model; the model does not reach into the DOM. That separation makes the idea inspectable without claiming it is production-ready.

## Expose realistic cases

1. State the model and decision visibly at the top.
2. Show the full relevant state after every action, using labelled domain fields rather than an unexplained JSON dump.
3. Offer free-play actions and a reset so unexpected action orders can expose a flaw in the idea.
4. Add guided scenarios for the happy path, an awkward case, and an illegal transition where relevant. Each starts at a known state and names the expected observation.
5. Record actual inputs and outcomes, including cases that contradict the proposed model.

Use in-memory state unless the question is specifically about persistence. Keep any scratch store isolated and named. Do not wire a throwaway interaction to production mutations.

## Preserve the answer

Return the runnable artifact, the cases exercised, and the conclusion or unresolved question. Keep only checks needed to trust the experiment; do not build a production test suite or ban a useful assertion.

The model is a candidate for a later build, not automatically validated production code. Preserve the experiment at its authorized location; branch creation, commits, pushes, and promotion follow existing task authority.
