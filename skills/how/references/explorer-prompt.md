# Scoped explorer prompt

Read this when organizing an implementation trace, inline or as an optional delegated angle. A coordinator owns any delegated starts and the shared budget.

## Brief

Question: `{question}`.

Assigned angle and boundaries: `{angle}`.

Relevant files, revision, inputs, existing findings, and allowed read surfaces: `{context}`.

Trace this angle without changing files or external state. Use the active host's supported tools. Findings from other angles may be useful pointers but are not proof until checked.

## Return

- **Components.** Real names, file/symbol/line anchors, and each component's responsibility.
- **Flow.** Entry point, calls, inputs, transformations, decisions, output, and side effects.
- **Files read.** Exact files and relevant revision, so another reader can check the trace.
- **Boundaries.** Inputs and outputs where this subsystem meets another owner.
- **Non-obvious behavior.** Surprising cases and the evidence supporting them.
- **Open questions.** Untraced branches, unavailable dependencies or runtime, and what remains uncertain.

Keep source-established behavior distinct from executed observations. Do not infer historical intent from current code. Return evidence within the assigned scope; start no child controller.
