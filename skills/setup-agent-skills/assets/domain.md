# Domain docs

Seed for `docs/agents/domain.md`. Replace these path examples with the actual project contract; retain existing layouts and formats.

## Read relevant existing material

For a new single-context setup, the glossary path is `GLOSSARY.md` and ADR directory is `docs/adr/`.

For a configured multi-context setup, read `GLOSSARY-MAP.md` and follow only the contexts relevant to the task. Record each actual glossary and ADR location, including any system-wide decisions.

If a glossary, map, or ADR directory does not exist, continue without a setup warning. The `domain-modeling` skill creates semantic material lazily when terms or decisions are resolved. Read that skill before relying on its method, if it is installed; absence of semantic files alone does not require setup.

## Use the domain's vocabulary

Name domain concepts as the relevant glossary defines them in issue titles, hypotheses, tests, and explanations. Preserve exact symbols and identifiers where the code needs them.

If a term is missing, first check whether it is an invented synonym. Record a real semantic gap only when it matters; do not create an empty glossary.

## Respect recorded decisions

Read ADRs relevant to the affected area. If a proposal conflicts with an accepted decision, identify the ADR and the reason for reconsideration. Preserve accepted records and follow the existing supersession process for an authorized replacement.

This file configures semantic-document consumption. It does not create a second execution plan or decision log.
