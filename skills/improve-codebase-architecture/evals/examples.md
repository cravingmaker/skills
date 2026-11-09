# Examples

Run each prompt with and without this skill. Record the observed behavior against the expectation.

## Activation

- "Survey this repo for architecture improvements and give me a report of deepening candidates." Expect: scopes by commit hot spots, gathers file:line and commit evidence, renders the candidates with the script into the temp directory, reports the path and asks which to explore.
- "Find the shallow modules in src/billing that make it hard to test, and show me before/after sketches." Expect: takes the named direction, applies the deletion test, and produces cards with before/after diagrams and evidence.

## Near miss

- "Make me a list of our tech debt with priorities." Expect: the skill does not load; tech-debt triage (the engineering tech-debt skill) fits better.
- "Design the interface for the new export module." Expect: the `architect` skill, not a codebase survey.
- "Refactor OrderHandler into one module now." Expect: a scoped refactor with no survey report; the manual `implement` entry is tested only when explicitly invoked.

## Outcome

- Source text with `<script>`, quotes and Mermaid click directives appears escaped as text in the report; the default report contains no scripts and makes no network request.
- With diagrams requested, the report pins one Mermaid version, uses `securityLevel: "strict"` and states the network dependency; `loose` never appears.
- No product code changes before the user picks a candidate; claims stay within the surveyed scope; repository terms such as "service" are kept.
