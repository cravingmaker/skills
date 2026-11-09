---
name: to-questionnaire
description: Turn a decision the user cannot fully answer into a local Markdown questionnaire for one recipient to fill in, aimed at the gap between what they know and what the user needs. Use when the user invokes to-questionnaire or asks for a questionnaire to send someone.
license: MIT
metadata:
  source: "https://github.com/mattpocock/skills/blob/49dd158d1076134a641b33efb035946536778336/skills/productivity/to-questionnaire/SKILL.md"
  source-revision: 49dd158d1076134a641b33efb035946536778336
  source-license: MIT, see LICENSE-mattpocock
  source-files: "skills/productivity/to-questionnaire/SKILL.md"
  local-changes: "Reuses an already supplied recipient, purpose, decision facts, and known gaps instead of an unconditional interview; asks only what still changes the questionnaire, in one message; the output is a local draft that is never sent or published."
---

# To questionnaire

Turn something the user cannot answer alone into a **questionnaire**: a Markdown document they hand to one person to fill in, or fill in together in a meeting. The recipient holds knowledge the user lacks; the questionnaire draws it out.

**Ask about the send, not the subject.** The user can always say who it goes to and what they need back. The questions in the document then target the **gap** between what the recipient knows and what the user needs.

## 1. Collect what is already known

From the request, the conversation, and any files the user pointed at, take:

- **Recipient:** role, expertise, and relationship to the user. This fixes the tone and how much context the document carries.
- **Purpose:** the decision riding on the answers, and where the answers will go.
- **Needs:** the specific decisions or facts the user must walk away able to make or know.
- **Known facts:** what the user already knows, so the document does not ask it.

## 2. Ask only what is missing

If any of recipient, purpose, or needs is missing or too vague to aim questions at, ask for exactly those, in one message. Skip this step when everything is supplied. Never ask the user about the subject itself; that is the recipient's part.

## 3. Write the draft

Draft questions aimed at the gap, following the template below. Write it to the path the user named, or to `to-questionnaire-<slug>.md` in the current directory (slug from the topic), and report the path.

Writing the draft sends nothing. Do not email it, post it, or publish it as a shared document unless the user asks for that as a separate step.

Done when the file exists, every need from step 1 is covered by a question, and no question asks for a fact the user already has.

## Document structure

Frame it as a **discovery questionnaire**: the user lacks context, the recipient holds it. Order questions most important first, since an async reply may come in one pass, and group them under `##` theme headings once there are more than a handful.

```markdown
# <Questionnaire title>

**Purpose:** why this questionnaire exists and the decision riding on it.

**From:** <the user>, **To:** <the recipient>, **How your answers will be used:** <where they go>

## Context

One paragraph orienting a recipient who wasn't in the user's head. Enough to answer well, not a page.

## How to answer

Deadline and rough effort. Partial answers and "I don't know" are useful: flag anything you're unsure of rather than skipping it.

## <Theme heading>

### What load is the system expected to handle at launch?

_Why this matters: it decides whether we provision for burst traffic now or defer it._

>

## Anything else?

A closing catch-all: anything we didn't ask that we should know?
```

Each question is one idea, never compound, with an answer stub (`>`) directly beneath it. Add a one-line _why this matters_ only where the question could be misread or invite a throwaway answer.

## Provenance

Adapted upstream files, their hashes, and the local changes: [references/SOURCES.md](references/SOURCES.md).
