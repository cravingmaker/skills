---
name: grilling
description: Interview the user about a plan, design, or decision in numbered rounds with recommended answers until every consequential choice is settled. Use when the user asks to be grilled, to stress-test a plan, or to settle open design decisions before building.
license: MIT
metadata:
  source: "https://github.com/mattpocock/skills/blob/49dd158d1076134a641b33efb035946536778336/skills/productivity/grilling/SKILL.md"
  source-revision: 49dd158d1076134a641b33efb035946536778336
  source-license: MIT, see LICENSE-mattpocock
  source-files: "skills/productivity/grilling/SKILL.md"
  local-changes: "Facts are looked up before asking and supplied answers are reused; only unresolved consequential choices are asked; sub-agent fact finding is optional and budgeted; added a checkable close, a no-doc default mode, and a stop rule; dropped repeat interviews."
---

# Grilling

Interview the user until you share an understanding of the plan, then stop. Map the plan as a **design tree**: every decision branches into the decisions that hang off it.

## Before the first round

1. **Look before asking.** Read the conversation, the files and docs the user pointed at, and the code they touch. Finding facts is your job; deciding is the user's.
2. **Reuse what is settled.** A choice the user already made, in this conversation or in the project's docs and decisions, is settled. Do not ask it again; list it as settled in the close.
3. **Keep only consequential choices.** A choice is consequential when two reasonable answers lead to different results and a wrong guess is costly to undo. State a reversible, low-stakes choice as an assumption in one line instead of asking it.

## Rounds

Work the tree in **rounds**. The **frontier** is every open decision whose prerequisites are settled: the questions you can ask now without guessing at answers you have not heard. Ask the whole frontier in one round. Number each question and give your recommended answer. Then wait for the answers.

Format a round like this:

```
❓ **Q1** - **<question title>**: <question body, might be multiple paragraphs, including multiple choices>

➡️ <your recommended answer>

---

❓ **Q2** - **<question title>**: <question body, might be multiple paragraphs, including multiple choices>

➡️ <your recommended answer>
```

Word each question so "yes" accepts your recommended answer. Ask for a missing fact only the user holds plainly, without a recommendation.

Each round of answers reshapes the tree: settled decisions push the frontier outward. Recompute the frontier and ask the next round. A question whose answer depends on another question still open in this round belongs to a later round. Before sending, check each question and recommendation for a condition supplied by an open answer; defer that branch instead of asking it in the same round.

When a frontier question needs a fact from the environment, look it up yourself; never ask the user for something you could find. A running lookup is an unsettled prerequisite, so only the questions downstream of it wait; ask the rest now. Do the lookup inline by default. Start a subagent only when the search is large and independent, and count the start against the run's shared budget when one exists.

## Close

Stop when the frontier is empty or every remaining question would not change the result. Then post the close:

- **Settled:** each decision, numbered, in one line, marked as the user's answer or as your stated assumption.
- **Deferred:** anything the user chose to leave open, with who decides it.
- **Next step:** what the settled plan feeds, such as the `to-spec` skill or direct work.

For an explicit interview, finish when the user confirms the close and wait for that confirmation before acting on its plan. For embedded use, return when the specific consequential gap is resolved; continue within the caller's existing authority without another whole-plan confirmation.

## Scope

- **Explicit interview.** When the user asked to be grilled, this skill's round format governs the conversation and you wait for each round's answers.
- **Embedded use.** When another skill uses grilling to fill a real gap, ask only the questions that gap needs, then return to that skill.
- **No-doc mode** (the default, and what the `grill-me` entry selects). Write no project files; the result lives in the conversation. Glossary and ADR updates belong to the `grill-with-docs` flow or an explicit instruction.
- **Resume, don't restart.** When a session is interrupted, pick up from the open frontier. A repeat interview over settled decisions wastes the user's time.

## Failure modes to check

- Asking the user something the repo, the docs, or the conversation already answers.
- Bundling a question that depends on an open answer into the same round.
- A recommendation that is not a real answer ("it depends").
- Answering a decision for the user and treating it as settled.
- Continuing past the point where remaining answers no longer change the plan.

## Provenance

Adapted upstream files, their hashes, and the local changes: [references/SOURCES.md](references/SOURCES.md).
