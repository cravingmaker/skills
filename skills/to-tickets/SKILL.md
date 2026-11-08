---
name: to-tickets
description: Break an approved spec into numbered vertical-slice tickets, each with status, acceptance checkboxes, a Proof line, and an exact Blocked by list, and file them where the project's tracker setup says. Use when the user invokes to-tickets or asks to split an approved spec or plan into tickets.
license: MIT
metadata:
  source: "https://github.com/mattpocock/skills/blob/49dd158d1076134a641b33efb035946536778336/skills/engineering/to-tickets/SKILL.md"
  source-revision: 49dd158d1076134a641b33efb035946536778336
  source-license: MIT, see LICENSE-mattpocock
  source-files: "skills/engineering/to-tickets/SKILL.md"
  local-changes: "Reads tracker and domain locations from the setup outputs; the ticket template gains Status, a Proof line, and a Blocked by list of ticket numbers or None that the work-decomposition importer parses exactly; numbers and approved wording stay stable; public-consumer compatibility kept in expand-contract; filing within authority, connected tools first; no implementation or run plan."
---

# To tickets

Break an approved spec into **tickets**: tracer-bullet vertical slices, each naming the tickets that **block** it. Consuming a spec does not need the skill that wrote it.

## 1. Gather

1. Work from the approved spec the user names (a path, an issue number, or a URL) or the one in the conversation. Read its full body and comments.
2. Read `docs/agents/issue-tracker.md` for where tickets go and how blockers are expressed, and `docs/agents/domain.md` for the glossary and ADR locations. Both come from the `setup-agent-skills` skill.
3. If the tracker setup is missing, draft the tickets in the conversation and name the `setup-agent-skills` skill as the step before filing. Do not guess a location.

## 2. Explore (optional)

If you have not explored the code yet, do so. Use the glossary's terms in titles and bodies and respect the ADRs in the area. Look for prefactoring that makes the change easy: "Make the change easy, then make the easy change."

## 3. Draft vertical slices

- Each slice cuts a narrow but complete path through every layer (schema, API, UI, tests): vertical, not one horizontal layer.
- A completed slice is demoable or verifiable on its own.
- Each slice fits one fresh agent session.
- Prefactoring comes first.

Give each ticket its blockers: the tickets that must finish before it can start. A ticket with no blockers can start now.

**Wide refactors are the exception.** A wide refactor is one mechanical change (rename a column, retype a shared symbol) whose blast radius breaks thousands of call sites at once, so no vertical slice can land green. Sequence it as **expand-contract**: first expand, adding the new form beside the old so nothing breaks; then migrate call sites in batches sized by blast radius (per package, per directory), each batch its own ticket blocked by the expand; finally contract, deleting the old form in a ticket blocked by every migrate batch. When even the batches cannot stay green alone, let them share an integration branch that blocks a final integrate-and-verify ticket; green is promised only there.

A public or independently deployed consumer (an API client, a published package, a persisted format) is not migrated with the batches. Its contract ticket waits for the project's compatibility or deprecation obligation, and says which one.

Carry each story's acceptance and proof from the spec into its tickets. When a story has no proof, propose one in the review below: the surface to drive or the source to open, and the result to observe.

## 4. Review the breakdown

Present the breakdown as a numbered list. For each ticket show its title, **Blocked by**, what it delivers, its **Proof**, and the user stories it covers. Ask in one message:

- Does the granularity feel right (too coarse or too fine)?
- Are the blockers correct: does each ticket depend only on tickets that truly gate it?
- Should any tickets be merged or split?

Iterate until the user approves the breakdown. If the user already approved this exact breakdown, file it.

## 5. File the approved tickets

Use the template and rules in [references/ticket-template.md](references/ticket-template.md). Read it before writing; the field forms are exact.

- **Local tracker:** one file per ticket in the ticket directory the tracker setup names, `NN-slug.md`, numbered from `01` in dependency order (blockers first). Never one combined file.
- **Remote tracker:** one issue per ticket in dependency order, so blockers can reference real identifiers. Use the tracker's native blocking relationship where it has one. If the spec came from an issue, make each ticket its sub-issue. Apply the label the setup maps to the `ready-for-agent` role. File when the user ran this skill to file or asked for filing; otherwise return the drafts and the exact filing step. Use the host's connected tracker tools when they can do the operation, and the CLI the setup names otherwise.

For local tickets, when the `work-decomposition` skill is installed, check the files with its importer and fix every `FAIL` line before reporting:

```sh
python3 <work-decomposition skill>/scripts/import-tickets.py <ticket directory> --spec <approved spec>
```

## Boundaries

- Once filed, numbers and approved wording are stable. New work gets a new number; a changed ticket keeps its number and the user approves the change.
- Do not close or modify the parent issue or the spec.
- Do not start implementation or write a run plan. The `work-decomposition` skill imports these tickets as they are.

## Done

Done when the user approved the breakdown and every ticket is filed (or returned as a draft) with a title, status, acceptance checkboxes, a Proof line, and a Blocked by list that names only existing ticket numbers or None.

## Provenance

Adapted upstream files, their hashes, and the local changes: [references/SOURCES.md](references/SOURCES.md).
