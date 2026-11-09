# Examples

Run each case with and without this final skill in fresh matched sessions. Hold inputs, required prerequisites, standing rules, host/model/tools, and the shared budget constant; remove equivalent upstream methods from the baseline. Record raw outcomes and limitations before marking evaluated. These are expectations, not observed results.

## Activation

- "Set up this project's Agent skills contract. Keep our configured GitLab project and docs/domain paths." Expect: the selected instruction file has one Agent skills block; tracker and domain docs keep the supplied identity and nondefault paths.
- "Configure local Markdown tickets for this repo; triage is installed and our ready label is bot-ready." Expect: local tracker seed is adapted to the configured ticket root, the role mapping keeps `bot-ready`, and no remote labels or issues are created.
- "Re-run setup with exactly these settings." Expect: on the already configured fixture the second run produces no file diff and preserves custom prose before, inside, and after the owned configuration.
- "Set up this repo with GitHub Issues. Use the connected GitHub tool; no CLI is installed." Expect: supported connected reads suffice, and no CLI, model sheet, startup hook, or upstream cache is installed.

## Near miss

- "Fix the typo in src/parser.ts." Expect: no setup block or configuration files are created.
- "The glossary doesn't exist yet; explain this function." Expect: explanation proceeds with existing context and no empty glossary, ADR, or setup ceremony.
- "Show me how our already configured tracker stores blockers." Expect: read the established contract and answer; do not reconfigure it.

## Outcome

- "Apply the same setup twice in a fixture with unrelated AGENTS.md sections and customized docs/agents prose." Check: byte-identical files after the second run, one effective block, preserved custom content, and no writes outside the selected block and docs/agents files.
- "Configure a single-context repo without triage, glossary, or ADR files." Check: no new triage subsection/file, empty glossary, or ADR directory; domain paths are recorded lazily.
- "An existing block conflicts with another block and an external label is missing." Check: resolve or report the actual conflict without wholesale overwrite; label absence grants no remote-write authority.
