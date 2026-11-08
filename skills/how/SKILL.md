---
name: how
description: "Explain how a concrete subsystem works from its source: entry points, execution flow, data, and ownership. Use for code walkthroughs, onboarding a subsystem, or checking where behavior belongs."
license: MIT
metadata:
  source: "https://github.com/cursor/plugins/blob/6b0300214a09fd6029cfb7077043125758cd1fd2/pstack/skills/how/SKILL.md"
  source-revision: "6b0300214a09fd6029cfb7077043125758cd1fd2"
  source-files: "pstack/skills/how/SKILL.md"
  local-changes: "Kept grounded execution-path explanation and optional explorer/explainer references; removed mandatory fan-out, diagrams, model sheets, and fixed tool maps."
---

# How

Explain the actual execution path well enough for the reader to work in it. Use the codebase's terms and source anchors.

## Trace the smallest useful scope

1. Resolve the target from the request, conversation, and named files. State a reversible interpretation when useful; ask only when the unresolved target would change the answer.
2. Read applicable project instructions, configured domain material, and the source around the real entry point. A symbol name or a generated summary alone does not prove a call path.
3. Follow a representative input through callers, dispatch, state and data transformations, decision points, outputs, and side effects. Include relevant error or asynchronous paths.
4. Name the component responsible at each step and the boundaries where responsibility changes. Follow actual imports, call sites, registration, and configuration rather than inferring a speculative graph.
5. Keep file/symbol/line or revision anchors for the consequential steps. Separate source-established behavior from behavior observed in a run. State gaps when dynamic dispatch, generated code, a dependency, or the runtime cannot be inspected.

A simple question is answered inline. If distinct exploration angles would materially help, the coordinator may reserve scoped independent work within its finite shared start/slot budget and the lower host/user limit. Neither exploration nor explanation requires a child agent.

Read [the explorer prompt](references/explorer-prompt.md) when organizing a scoped trace, inline or delegated. Read [the explainer prompt](references/explainer-prompt.md) when combining several traces or explaining a larger subsystem. The references supply optional structure, not a second controller.

## Explain the mechanism

Lead with the smallest complete explanation. Add only the detail the question needs:

- **Overview.** What this subsystem does and where the flow starts.
- **Key concepts.** The real types and terms needed to follow it.
- **Execution path.** What runs, what data changes, and what happens next.
- **Where things live.** The few files a new contributor should open.
- **Gotchas and limits.** Non-obvious behavior, unresolved branches, and static versus executed evidence.

Use prose with short source snippets when they make the mechanism clearer. A diagram is optional and must be supported by the traced relationships. Do not require every section for a narrow answer.

Use the `why` skill only when historical motivation matters, and the `research` skill only when a separate primary-evidence question needs it, if installed. Read the selected skill before use. Present behavior is not evidence of historical intent.

Investigation stays within read-only authority unless changes were separately authorized. A walkthrough does not start an implementation, PR, or review loop.

Done when the reader can follow a real input from the named entry point to its outcome, locate the responsible code, and distinguish established behavior from unresolved or unobserved paths.

## Provenance

Read [the per-file sources](references/SOURCES.md) when checking attribution, original hashes, destinations, and adaptation.
