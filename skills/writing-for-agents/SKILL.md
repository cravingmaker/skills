---
name: writing-for-agents
description: Author or repair agent instruction content, triggers, and completion criteria in SKILL.md, AGENTS.md, CLAUDE.md, or their references. Use only for requested content changes. For finalized instructions, use the selected packager or installer directly without loading this skill.
license: MIT
metadata:
  requires: "clear-communication"
  source: "https://github.com/mattpocock/skills/blob/49dd158d1076134a641b33efb035946536778336/skills/productivity/writing-for-agents/SKILL.md"
  source-revision: "49dd158d1076134a641b33efb035946536778336"
  source-files: "skills/productivity/writing-for-agents/SKILL.md"
  local-changes: "Kept instruction hierarchy and pointer craft; aligned mechanics and paired evals to this repo; merged discovery and recurrence methods; excluded the Anthropic mirror and compulsory model trials."
---

# Writing for agents

Write instructions that change a decision and give the agent a checkable stopping point. The same craft applies to a skill, an AGENTS.md or CLAUDE.md file, and a document reached by a pointer. The goal is a reliable process across runs, with room for the task's actual judgment.

Read the local authoring guide and existing conventions before drafting. Resolve and read the `clear-communication` skill (required) from the installed inventory; if it is missing, name the prerequisite and stop this flow. For a skill in this repository, read [references/skill-mechanics.md](references/skill-mechanics.md) for packaging, invocation, dependencies, provenance, and completion checks. Host setup or packaging by itself is a separate job; instruction craft does not require changing host settings.

## Context pointers

A **context pointer** names material outside the current context and states when to read it. A skill description is one; an AGENTS.md line naming a document is another. Its wording decides whether the agent reaches the material. When necessary guidance goes unread, sharpen the pointer before moving the whole target into always-loaded context.

- Front-load the leading concept that identifies the work.
- Give one trigger per distinct branch; collapse synonyms for the same branch.
- State both what the material does and when it applies, using the user's words.
- Link the target and say "read this when" its branch needs it. A required reference hidden behind an optional-sounding pointer is a real defect.

Descriptions help discovery; they never substitute for reading the skill body. Test ordinary and similar requests as well as explicit names. Quoted commands and incidental name matches should leave unrelated work alone.

## Information hierarchy

Every document spends **context load** on the agent and **cognitive load** on the human who must find it. Always-loaded instructions pay context load every turn; disclosed reference pays only its pointer until needed. Create a separate capability only when independent discovery or reuse earns that cost.

Put material on the rung where it is needed:

1. **Steps:** actions taken in order, ending in completion criteria.
2. **In-file reference:** definitions and rules consulted within the active branch.
3. **Disclosed reference:** detail only some branches need, behind a precise pointer.

Inline what every branch needs and disclose branch-specific detail. Keep a concept's definition, rules, and caveats together so reading one brings its neighbors. Split a long sequence when observed premature completion survives a clearer stopping criterion; a heading alone creates no new context boundary. Use [references/diagrams.md](references/diagrams.md) when a non-obvious choice or loop needs a diagram.

## Completion criteria

Every step ends on a condition the agent can distinguish from unfinished work. "Every changed interface has its affected callers checked" demands more useful legwork than "produce a change list." Name the artifact, observable predicate, evidence, and handling of unavailable proof. Keep a real exhaustive requirement explicit; a sample cannot stand in for full coverage.

Match wording to the demonstrated failure:

| Failure | Useful form |
| --- | --- |
| Wrong output shape | A positive recipe and one complete example |
| Missing required element | A field in the artifact's template |
| Behavior depends on a condition | A branch keyed to an observable predicate |
| Mechanical violation | Structural enforcement or an existing deterministic check |
| Judgment missed despite a clear instruction | Inspect execution evidence before adding prose |

Phrase the target behavior positively. Reserve prohibitions for a hard boundary and pair them with the permitted action. State a real exception as a condition rather than an escape clause attached to every rule.

## Leading words and one source of truth

A **leading word** is a compact concept the agent can reuse, such as checkpoint, evidence, or baseline. Define it clearly and repeat the term rather than its full explanation. Prefer familiar concepts; an invented label spends the words it was meant to save.

Keep each meaning in one authoritative place. Point to other methods instead of copying their procedures. The environment is a source of truth too: discover scripts, config, and layout rather than keeping a second description that drifts. Cache the unwritten convention or costly lookup, with a reason and a freshness boundary.

Delete no-ops, stale guidance, and repeated meanings. A sentence earns its place when it changes behavior relative to the observed default. Use the relevant evaluation evidence to decide; confident prose and shorter output alone prove little.

## Extract working conventions

When asked to capture a user's working style, preserve existing applicable guidance and mine only the authorized project and range. Use supported scoped search and exact evidence pointers, rather than ingesting unrelated transcript history. Separate an explicit preference from an agent interpretation and from a contradicted or one-off signal. Require evidence of recurrence before generalizing an inferred convention; a direct user instruction retains its stated scope. Check whether an existing capability or deterministic mechanism already owns the behavior. Add only the non-default rule that changes future work, without inventing a personal router or extra sections.

## Validate and report

Read [references/evaluation.md](references/evaluation.md) when designing examples, comparing instruction variants, or claiming evaluation. Run deterministic packaging, link, catalog, prose, script, and template checks first. Use the repo's existing harness for matched final-skill and no-skill examples within actual model-run authority and budget. Drafting requires no model call; without recorded pairs, keep status unevaluated and report the unrun checks. Preserve existing material until a justified scoped change replaces it; an untested draft is not a reason to delete work. Do not bootstrap plugins, prescribe models, launch fixed reviewer panels, or publish merely to finish authoring.

Done when the trigger is narrow, the instructions have checkable completion criteria, references and provenance resolve, deterministic checks pass, and evaluation claims match the recorded evidence. Return the changed behavior, validation, and remaining limits. Source files and adaptations: [references/SOURCES.md](references/SOURCES.md). External guidance is link-only: [Anthropic's official skill authoring guidance](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices).
