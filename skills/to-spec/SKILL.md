---
name: to-spec
description: Turn an already agreed plan into an engineering spec with numbered user stories, acceptance and proof per story, testing seams, and bound source documents, then file it where the project's tracker setup says. Use when the user invokes to-spec or asks to write up the agreed plan as a spec.
license: MIT
metadata:
  requires: "domain-modeling"
  source: "https://github.com/mattpocock/skills/blob/49dd158d1076134a641b33efb035946536778336/skills/engineering/to-spec/SKILL.md"
  source-revision: 49dd158d1076134a641b33efb035946536778336
  source-license: MIT, see LICENSE-mattpocock
  source-files: "skills/engineering/to-spec/SKILL.md"
  local-changes: "Reads tracker and domain locations from the setup outputs; binds source documents by hash; adds acceptance and real-surface proof to every user story for ticket Proof lines; keeps story numbers stable; publishes only to the configured destination within authority, connected tools first; template moved to a reference."
---

# To spec

Write the spec from what is already agreed. Do not interview the user: synthesize the conversation, the `grilling` close if there is one, and the project's domain documents.

## 1. Read the setup and the agreed understanding

1. Read `docs/agents/issue-tracker.md` for where specs live and how they are filed, and `docs/agents/domain.md` for the glossary and ADR locations. Both come from the `setup-agent-skills` skill.
2. If the tracker setup is missing, write the spec as a draft in the conversation (or at a path the user names) and name the `setup-agent-skills` skill as the step before filing. Do not guess a tracker.
3. Explore the code the spec touches, if you have not already. Use the glossary's terms throughout, as the `domain-modeling` skill keeps them, and respect the ADRs in the area. Flag a contradiction with an ADR rather than overriding it.
4. Preserve the agreed scope exactly. A point that is still genuinely open goes under **Open questions** in the spec, with who decides it; it does not start a new interview.

## 2. Choose the testing seams

Sketch the seams where the feature will be tested. Prefer existing seams to new ones and the highest seam possible; the fewer seams, the better, and one is ideal. If the user already agreed the seams, use them. Otherwise put the proposed seams in the draft and ask the user to confirm them with the draft review, in the same message.

## 3. Write the spec

Use [references/spec-template.md](references/spec-template.md). Read it before writing; it holds the section rules.

- Number user stories from 1. Each story carries its **Acceptance** (observable conditions) and its **Proof**: the surface to drive or the source to open, and the result to observe there. The `to-tickets` skill copies these into each ticket's acceptance checkboxes and `Proof:` line.
- Name the real surface. "Unit tests pass" proves only the unit tests; a UI story is proved in the UI, a CLI story at the command line.
- Bind the sources: list each document the spec relies on (glossary, ADRs, prototype, parent issue) with its path or link and, for files, its SHA-256 (`shasum -a 256 <file>` or `sha256sum <file>`).
- Size detail to the decision. Cover every behavior in scope; leave out what the builder can decide.

## 4. File it

- **Local tracker:** write the spec at the path the tracker setup names.
- **Remote tracker:** file it when the user asked for filing or ran this skill to file the spec; when the user asked for a draft or a review, return the draft and the exact filing step instead. Use the host's connected tracker tools when they can do the operation, and the CLI the setup names otherwise.
- Apply the label the setup maps to the `ready-for-agent` role, when the tracker uses labels.

Once filed, story numbers are stable: new stories get new numbers, and a changed story keeps its number.

## Done

Done when the spec exists at its configured destination (or as a returned draft), every user story has acceptance and a real-surface proof, every source is bound, and no interview or implementation happened.

## Provenance

Adapted upstream files, their hashes, and the local changes: [references/SOURCES.md](references/SOURCES.md).
