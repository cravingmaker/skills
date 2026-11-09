# Scoped investigator prompt

Read this for a bounded evidence pass, inline or delegated. A coordinator owns any delegated starts and budget; this prompt starts no agents.

## Inputs

Question: `{question}`.

Target files, line or symbol anchors, and revision: `{code_anchor}`.

Available commits, linked PRs or tickets, and prior valid findings: `{seed_context}`.

Assigned source, permitted reads, relevant time window, and search bound: `{source_scope}`.

Read the relevant source method and apply the epistemics rules linked from SKILL.md. For human rulings, preserve attributable original wording and scope, label summaries, and flag missing originals.

## Gather evidence

1. Search the target's actual identifiers and nearby domain terms, then narrow to the relevant time and actors.
2. Read the relevant PR, ticket, document, or thread in context. A title or search snippet may omit the decisive qualification.
3. Follow leads within the assigned scope. Record cross-source leads for the coordinator rather than expanding an independently assigned pass.
4. Keep a faithful short excerpt or paraphrase, exact locator, author, and date where available.
5. Record actual queries and access or retention limits, including empty results.
6. Preserve contradictions. Ask what evidence would differ if the current reading were wrong.

Mechanics are not motivation. A source showing a change or failure can support context without recording why someone made a choice.

## Return

- **Source and coverage.** What was actually searched, queries, window, and items read.
- **Direct evidence.** Attributable statements explaining this target, with exact locators.
- **Indirect evidence.** Observations, inference chains, and alternative readings.
- **Contradictions.** Both sources and the point of disagreement.
- **Gaps.** Empty, unavailable, limited, or unsearched material, labelled accurately.
- **Leads.** Specific further sources that could resolve a consequential gap.

Keep private material to the relevant excerpts; return no credentials or unrelated raw records. Gather evidence within the assigned reads and return without changing files or external state.
