---
name: grill-with-docs
description: Interview the user about a plan or design while recording the resolved terms in the project glossary and justified decisions as ADRs at the configured paths. Use when the user invokes grill-with-docs or asks to be grilled with the glossary and ADRs updated as decisions land.
license: MIT
metadata:
  requires: "grilling domain-modeling"
  source: "https://github.com/mattpocock/skills/blob/49dd158d1076134a641b33efb035946536778336/skills/engineering/grill-with-docs/SKILL.md"
  source-revision: 49dd158d1076134a641b33efb035946536778336
  source-license: MIT, see LICENSE-mattpocock and LICENSE-superpowers
  source-files: "skills/engineering/grill-with-docs/SKILL.md"
  local-changes: "Replaced Skill-tool calls with reads of the owned skills; reads the domain setup and existing decisions first; added Superpowers context grounding and an optional budgeted builder check; dropped the brainstorming hard gate, design approval, visual companion, and second spec pipeline."
---

# Grill with docs

Run the `grilling` interview with the `domain-modeling` discipline active, so the glossary and ADRs grow as decisions land. Read both skills before starting; this skill only says how they combine.

## 1. Ground the interview

1. Read `docs/agents/domain.md` for the glossary and ADR locations. Missing glossary or ADR files are normal; the `domain-modeling` skill creates them when the first entry is written.
2. If `docs/agents/domain.md` itself is missing, say so and name the `setup-agent-skills` skill as the step that records the paths. Offer to continue as a plain `grilling` interview, with no doc writes until setup exists or the user names the paths.
3. Read the glossary entries and ADRs in the area under discussion, the files the user pointed at, and the code they touch. Keep reading until you can explain how the relevant parts work today and what the change would touch.
4. Never ask what the project or the conversation already answers, and never reopen a decision the user or an accepted ADR already made. Raise a conflict with an ADR as a conflict, citing it.

## 2. Interview and record

Work the `grilling` rounds. As each round lands:

- Challenge and sharpen terms against the glossary, as the `domain-modeling` skill describes.
- Write each resolved term to the configured glossary when it settles.
- Offer an ADR only when a decision meets all three `domain-modeling` criteria. Write it when the user accepts.

Running this skill authorizes glossary and ADR writes at the configured paths. It does not authorize commits, product code, or tracker writes.

## 3. Optional builder check

When the settled understanding will be handed on to be built (to the `to-spec` skill or to another builder), and a fresh reader would add value, run one builder check on the close. Follow [references/builder-check.md](references/builder-check.md). A subagent start counts against the run's shared budget; without a subagent or budget, read the close as that builder yourself.

## 4. Close

Post the `grilling` close, then list every glossary and ADR change with its path. Name the `to-spec` skill as the next step when the result is a build.

Done when the user confirms the close and every resolved term and accepted ADR is written at its configured path.

## Out of scope

- A gate that blocks all building until a design document is approved.
- A second spec or plan document; the `to-spec` skill writes the spec.
- A browser companion or local server.

## Provenance

Adapted upstream files, their hashes, and the local changes: [references/SOURCES.md](references/SOURCES.md).
