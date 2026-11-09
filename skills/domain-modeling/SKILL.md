---
name: domain-modeling
description: Change a project's domain model by resolving or renaming terms in its configured glossary, or recording or superseding hard-to-reverse architecture decisions. Use for domain-model changes; vocabulary-only explanations use the existing glossary directly.
license: MIT
metadata:
  source: "https://github.com/mattpocock/skills/blob/49dd158d1076134a641b33efb035946536778336/skills/engineering/domain-modeling/SKILL.md"
  source-revision: 49dd158d1076134a641b33efb035946536778336
  source-license: MIT, see LICENSE-mattpocock
  source-files: "skills/engineering/domain-modeling/SKILL.md"
  local-changes: "Paths come from the project's domain setup instead of fixed file names; writes stay within current authority; added source links for terms, accepted-ADR immutability with supersession, the boundary with decision-log, and the terminology sweep reference."
---

# Domain modeling

Build and sharpen the project's domain model while a design is discussed: challenge terms, probe edge cases, and write resolved terms and decisions down when they settle. Reading the glossary for vocabulary is a habit any skill has; this skill is for changing the model.

## Find the files

1. Read `docs/agents/domain.md`, which the `setup-agent-skills` skill writes. It names the layout (single or multiple contexts), each glossary file, and each ADR directory. Use those paths and the formats the existing files already follow.
2. If that file is missing, ask the user where the glossary and ADRs live, or name the `setup-agent-skills` skill as the step that records them. Do not invent a location.
3. In a multi-context project, infer which context the topic belongs to from the map the setup names. If it is unclear, ask.
4. A configured file that does not exist yet is normal: the setup creates domain files lazily. Create the glossary when the first term is resolved and the ADR directory when the first ADR is needed.

## During the session

- **Challenge against the glossary.** When the user uses a term that conflicts with the glossary, say so at once: "Your glossary defines 'cancellation' as X, but you seem to mean Y. Which is it?"
- **Sharpen fuzzy language.** When a term is vague or overloaded, propose a precise canonical term: "You're saying 'account': do you mean the Customer or the User? Those are different things."
- **Discuss concrete scenarios.** Stress-test relationships with specific scenarios that probe the boundaries between concepts.
- **Cross-reference with code.** When the user states how something works, check whether the code agrees and surface a contradiction: "Your code cancels entire Orders, but you just said partial cancellation is possible. Which is right?"

## Record a term

Update the glossary when a term is resolved, not in a batch at the end. Follow [references/glossary-format.md](references/glossary-format.md) unless the project's glossary already uses another format.

Before saving, check that the entry names the canonical term, its definition, and any competing names under `_Avoid_`. Keep distinct existing concepts distinct rather than broadening one term to cover both.

The glossary holds domain language and nothing else: no implementation details, no spec, no scratch notes. Keep the exact term the domain uses, and link its authority (a stakeholder decision, a regulation, an ADR, a source document) when one exists.

## Record a decision

Offer an ADR only when all three are true:

1. **Hard to reverse:** changing your mind later costs something meaningful.
2. **Surprising without context:** a future reader will wonder why it was done this way.
3. **A real trade-off:** there were genuine alternatives and one was picked for specific reasons.

If any is missing, skip the ADR. Use [references/adr-format.md](references/adr-format.md).

An accepted ADR is immutable. To change the decision, write a new ADR that supersedes it, and change only the old ADR's status line to `superseded by ADR-NNNN`.

ADRs record durable project architecture. Run-level choices inside a multi-agent run belong to the `decision-log` skill's records; do not copy them into ADRs.

## Authority

Write glossary and ADR changes when the user ran a docs-recording flow (the `grill-with-docs` skill) or asked for the edit. Otherwise show the exact proposed edit and wait. Committing the change is a separate step the user asks for.

## Rename a concept

When a settled term replaces an old one across UI, API, and docs, run the sweep in [references/terminology-sweep.md](references/terminology-sweep.md). Read it when a rename touches more than the glossary.

## Done

Done when every term resolved in the session is in the configured glossary with no implementation detail, every ADR meets all three criteria, and no accepted ADR was edited except its status line.

## Provenance

Adapted upstream files, their hashes, and the local changes: [references/SOURCES.md](references/SOURCES.md).
