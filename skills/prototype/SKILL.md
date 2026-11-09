---
name: prototype
description: "Build a bounded throwaway artifact to answer a design question. Use when the user wants to try a state model, compare interactions, or explore what a UI should look like before building it."
license: MIT
metadata:
  source: "https://github.com/mattpocock/skills/blob/49dd158d1076134a641b33efb035946536778336/skills/engineering/prototype/SKILL.md"
  source-revision: "49dd158d1076134a641b33efb035946536778336"
  source-files: "skills/engineering/prototype/SKILL.md"
  local-changes: "Kept logic/UI branches and realistic consumer scenarios; made experience-first and alternatives optional; bounded effort and proof; removed branch, commit, push, server, and production-promotion mandates."
---

# Prototype

A prototype is **throwaway code that answers a question**. The question decides the artifact and the evidence.

## Frame the decision

Name one decision, the realistic cases it must expose, and the stopping point before building. Use the user's scope and effort limit; for an open request, state a small artifact and a finite exploration budget. Reuse existing decisions and references.

If two readings would produce different artifacts, resolve that ambiguity or state a reversible assumption. Ordinary implementation does not need a prototype.

Pick the branch that answers the question:

- **Logic or state.** Read [the logic method](references/logic.md) when the question concerns data shape, legal actions, transitions, timing, or behavior.
- **UI or interaction.** Read [the UI method](references/ui.md) when the question concerns layout, information order, density, controls, or interaction.
- **Consumer experience.** Read [the decision methods](references/decision-methods.md) when trying alternatives or a consumer journey would distinguish competing ideas. This is optional, including for libraries and internal APIs.

Done when the question and an observation that could change the decision are explicit.

## Build only the experiment

1. Use realistic representative inputs, awkward boundary cases, and the project's domain terms. Preserve supplied values and identifiers; label invented fixtures.
2. Put the artifact in a clearly named prototype location within the authorized write scope. Use a scratch artifact unless the question needs the existing page or module context. Follow existing routes and runners where applicable.
3. Choose the smallest runnable form: a self-contained logic demo, a short script, or a temporary UI rendering path. Keep relevant state visible and scenarios repeatable.
4. Keep state in memory by default. Use stubs for real mutations; use a named scratch store only when persistence is the question and that store is authorized.
5. Skip production abstractions and polish that cannot affect the decision. Retain the checks needed for a valid observation and safe operation. A blanket ban on tests is no substitute for reliable evidence.

If alternatives would settle the question, label and compare them under the same inputs. A single decisive experiment is enough when comparison adds nothing.

## Observe and conclude

Drive the artifact on the surface the decision concerns. For logic, record the actual outputs, transitions, or timing and the exercised inputs. For UI, inspect the rendered alternatives and drive their relevant interactions through supported host preview or browser tools. Use the existing runner only when the artifact requires it.

State which cases were observed and which remain untested. A screenshot alone cannot establish an interaction, and source inspection cannot establish a rendered result. If the necessary surface is unavailable, preserve the artifact and leave the conclusion qualified.

Return the question, artifact path and run instructions, observations, trade-offs, and the supported conclusion. Preserve that conclusion in the requested or established decision artifact; the reply suffices when no durable note was requested. Keep the experiment available for review.

A validated idea can inform a later authorized build. Prototype completion does not authorize production changes, branch creation, commits, pushes, or publication. End at the experiment unless that further work is already in scope.

Done when the bounded artifact answers the decision with appropriate observations, or records the precise unresolved case without claiming success.

## Provenance

Read [the per-file sources](references/SOURCES.md) when checking attribution, original hashes, destinations, and adaptation.
