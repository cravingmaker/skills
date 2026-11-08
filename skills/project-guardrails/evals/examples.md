# Examples

Run each prompt with and without this skill in a temporary fixture project. Record the observed behavior against the expectation.

## Activation

- "Set up guardrails for this new TypeScript package." Expect: an inventory first, then the smallest changes that wire format, lint, type, and test checks into one command used locally and in CI, with reject, accept, and rerun proof for each.
- "Audit what this repo actually enforces." Expect: a capability table in goal order with enforced, unwired, broken, missing, or not applicable per row, each with evidence, and no changes made unless asked.
- "Harden the CI workflows." Expect: pinned SHAs, least-privilege `permissions`, and workflow analysis assessed and proven, without unrelated changes.

- "The audit finds one missing CLI proof; keep the fix small." Expect: discover existing commands first and conditionally use the `create-verification-skill` skill in bounded-gap mode, without a full feature sweep or new local recipe.

- Wire the already-authorized staged lint hook using this project's existing package manager and hook setup.

## Near miss

- "Fix this failing unit test." Expect: the test is fixed directly; no guardrail audit.
- "What does our ESLint config do?" Expect: an explanation; no setup or changes.

- Audit only; do not install hooks. Expect evidence and gaps without policy, dependency or hook writes.

## Outcome

- A fixture project with a configured but unwired linter gets it wired into CI before any new tool is added.
- Each changed guardrail rejects a planted violation, accepts valid code, and running the setup a second time changes nothing.
- The report lists versions with their sources, and any capability whose current guidance could not be confirmed is reported as open, not filled with a guess.
- A project that already enforces a capability with a different tool keeps that tool.
- "A repeatable real-surface proof is missing, and the generator is unavailable." Expect: retain the gap assessment and report the missing helper; do not invent a second procedure, product repair, or hook/policy change.
- An existing deterministic check wins. A recurring uncovered gap justifies a small repeat-safe tool; authorized hook setup preserves formatter/package-manager/configuration and demonstrates staged/local/CI reject, accept and repeat parity.
