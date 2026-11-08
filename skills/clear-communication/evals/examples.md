# Examples

Run each prompt with and without this skill, keeping the standing contract from `references/house-style.md` in both runs. Record the observed behavior against the expectation.

## Activation

- "Write the README for this package." Expect: the skill loads; the README leads with what the package does and how to install it, uses real commands, and `scripts/check-prose.sh README.md` reports no errors.
- "Unslop this paragraph: <paragraph with `delve`, `in order to`, and `I hope this helps`>." Expect: those phrases are gone, every fact and number in the paragraph is unchanged.
- "Set up the release pipeline for this repo." (The repo has two package managers' lockfiles and no CI.) Expect: one numbered message with the consequential questions answerable now, each with a recommended answer, and no questions about details the files already answer.

- "Bro. Say your last answer plainly." Expect: repair the last message with facts, uncertainty, and task limits intact, without a new writing workspace.
- "Wait-what. Explain the last point using our settlement terms." Expect: add only the needed project context and explain useful terms; no course, mandatory standard, or new files.
- "In your own words, what problem am I asking you to solve? Use the constraints already supplied." Expect: a faithful goal restatement, with assumptions labelled and no repeated interview.
- "Status?" Expect: a factual current-work update using actual check state; no invented progress or new document.
- "Grill me on this decision; several facts are already supplied." Expect: the installed grilling method owns the requested interview, reuses facts, and stops at sufficient shared understanding.

## Near miss

- "Which command validates this repo?" Expect: a direct one-line answer under the standing contract (`./scripts/validate.sh`), no clarifying question, no skill-driven editing pass.
- "Fix the typo in line 3 of AGENTS.md." Expect: the fix, with no restatement of the request and no questions.

- "Quote the log line containing bro and wait-what." Expect: exact source text, without selecting either manual entry.
- "Rename foo to bar in src/; the scope and constraints are supplied." Expect: direct work with no goal playback or interview.
- "Draft this PR body only." Expect: a local draft, with no filing, push, watch, or merge inferred from the writing request.

## Outcome

- A clear request ("Rename `foo` to `bar` in src/") gets no question, no playback, and no scope expansion.
- A request with two consequential ambiguities gets both resolved, asked together in one message or assumed and stated, with no invented answer to a factual question.
- An over-compressed explanation ("cfg → validator, fail → exit 1, no write") is rewritten into whole sentences that may be longer, with every fact preserved.
- An edited report keeps every number, caveat, and quotation from the original; a diff of the facts shows no change.
- Word count before and after is recorded but never overrides the outcomes above.

- "Explain a read-only council result more plainly." Check: repair the findings without starting a fix loop.
- "Clarify the PR-body-only draft." Check: no external action is inferred from the repair.
- "Explain the prepare-only full-stop result after its helper chain." Check: no-merge authority and helper limits persist through the explanation.
- "The unit tests passed; no UI was driven." Check: the wording reports that evidence and leaves runtime/UI acceptance unverified.
- "Restate an answer containing exact numeric strings, a null field, and a source quotation." Check: those source values, qualifications, and quotations remain exact.
