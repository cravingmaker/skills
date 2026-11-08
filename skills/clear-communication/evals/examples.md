# Examples

Run each prompt with and without this skill, keeping the standing contract from `references/house-style.md` in both runs. Record the observed behavior against the expectation.

## Activation

- "Write the README for this package." Expect: the skill loads; the README leads with what the package does and how to install it, uses real commands, and `scripts/check-prose.sh README.md` reports no errors.
- "Unslop this paragraph: <paragraph with `delve`, `in order to`, and `I hope this helps`>." Expect: those phrases are gone, every fact and number in the paragraph is unchanged.
- "Set up the release pipeline for this repo." (The repo has two package managers' lockfiles and no CI.) Expect: one numbered message with the consequential questions answerable now, each with a recommended answer, and no questions about details the files already answer.

## Near miss

- "Which command validates this repo?" Expect: a direct one-line answer under the standing contract (`./scripts/validate.sh`), no clarifying question, no skill-driven editing pass.
- "Fix the typo in line 3 of AGENTS.md." Expect: the fix, with no restatement of the request and no questions.

## Outcome

- A clear request ("Rename `foo` to `bar` in src/") gets no question, no playback, and no scope expansion.
- A request with two consequential ambiguities gets both resolved, asked together in one message or assumed and stated, with no invented answer to a factual question.
- An over-compressed explanation ("cfg → validator, fail → exit 1, no write") is rewritten into whole sentences that may be longer, with every fact preserved.
- An edited report keeps every number, caveat, and quotation from the original; a diff of the facts shows no change.
- Word count before and after is recorded but never overrides the outcomes above.
