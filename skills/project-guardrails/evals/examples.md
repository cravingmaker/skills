# Examples

Run each prompt with and without this skill in a temporary fixture project. Record the observed behavior against the expectation.

## Activation

- "Set up guardrails for this new TypeScript package." Expect: an inventory first, then the smallest changes that wire format, lint, type, and test checks into one command used locally and in CI, with reject, accept, and rerun proof for each.
- "Audit what this repo actually enforces." Expect: a capability table in goal order with enforced, unwired, broken, missing, or not applicable per row, each with evidence, and no changes made unless asked.
- "Harden the CI workflows." Expect: pinned SHAs, least-privilege `permissions`, and workflow analysis assessed and proven, without unrelated changes.

## Near miss

- "Fix this failing unit test." Expect: the test is fixed directly; no guardrail audit.
- "What does our ESLint config do?" Expect: an explanation; no setup or changes.

## Outcome

- A fixture project with a configured but unwired linter gets it wired into CI before any new tool is added.
- Each changed guardrail rejects a planted violation, accepts valid code, and running the setup a second time changes nothing.
- The report lists versions with their sources, and any capability whose current guidance could not be confirmed is reported as open, not filled with a guess.
- A project that already enforces a capability with a different tool keeps that tool.
