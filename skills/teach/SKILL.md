---
name: teach
description: Teach a concept or subsystem through what, how, and why. Use for a requested deep explanation or saved lessons. For an explicitly selected learning or spaced-repetition workflow, use that workflow directly without loading this skill.
license: MIT
metadata:
  requires: "clear-communication how why"
  source: "https://github.com/cursor/plugins/blob/6b0300214a09fd6029cfb7077043125758cd1fd2/pstack/skills/teach/SKILL.md"
  source-revision: "6b0300214a09fd6029cfb7077043125758cd1fd2"
  source-files: "pstack/skills/teach/SKILL.md"
  local-changes: "Kept grounded layered explanation; made investigation inline-capable and quizzes learner-controlled; restricted Matt's durable workspace and formats to explicit requests."
---

# Teach

Explain what a thing is, how it works, and why it is built that way, in one plain account at the learner's pace. Default to explanation in the conversation. An ordinary explanation creates no course, lessons, progress records, or workspace files.

Resolve and read the `clear-communication` skill (required), the `how` skill, and the `why` skill from the installed inventory before relying on them. If one is missing, name the prerequisite and stop this flow. These are reusable methods, rather than three mandatory agent launches.

## Ground the explanation

1. **Choose the understanding.** Infer why the learner is asking and what they already know from the conversation. Reuse that context rather than quizzing it out of them. Ask only if a missing fact changes the explanation's scope or level. Done when the account has a small, relevant learning goal.
2. **Trace how.** Use the `how` skill to follow the actual mechanism at the depth the question needs. Start from supplied artifacts, code, or high-trust topic sources. Prefer a concrete execution or worked example over a catalog of functions. Done when the explanation's factual path has source anchors and any unavailable steps are marked.
3. **Establish why.** Use the `why` skill for the relevant rationale, alternatives, and constraints. Keep the investigation narrow unless history is the question. Reuse already established evidence and state the skipped or unavailable sources. Preserve distinctions between documented intent, supported inference, and unknown rationale when rewording for teaching.

Apply these methods inline unless delegation is useful and already permitted by the active host and run budget. Match the investigation to the question; a small mechanism need not trigger a broad historical sweep.

## Explain in layers

Start with a plain definition and tie it to the case in front of the learner. Give the smallest complete answer first, then build only the layers the question needs: mechanism, rationale, example, and consequential edge cases. Walk through what happens as the person uses the thing when that makes the mechanism clear. Keep one name per concept and preserve source values, uncertainty, identifiers, and quotations.

Use a diagram, real artifact, or small example when it explains more clearly than prose. Build a complex picture in useful stages; a simple point needs no figure. Choose the supported medium for the idea without a diagram quota, generated-image requirement, or new app launch. Explain the mechanism directly and leave space for the learner's next question. In a one-shot request, deliver the requested depth in one self-contained answer.

The learner controls quizzes and practice. Honor a request for questions or exercises and an agreed learning plan; honor a preference to skip them just as directly. Without that choice, explain without a compulsory quiz, teach-back, or pacing ceremony. An answer that repeats your wording does not establish durable understanding.

## Explicit durable workspace mode

Enter this mode only when the user asks to save a learning workspace, curriculum, lessons, or progress across sessions. Read [references/workspace-mode.md](references/workspace-mode.md) before writing its MISSION, RESOURCES, lessons, learning records, or learner glossary. Use the user's chosen destination and existing conventions; create only the artifacts the agreed learning task needs. Keep learner terminology separate from the project's authoritative semantic glossary.

## Done

Return the explanation itself, with the main point first, source-backed mechanisms, calibrated rationale, and visible limits. Success means the learner has an accurate account at the requested depth; do not claim they mastered or retained it without evidence. For requested workspace mode, also return the saved artifact paths and the next agreed learning step. Source files and adaptations: [references/SOURCES.md](references/SOURCES.md).
