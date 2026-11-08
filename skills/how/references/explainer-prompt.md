# Scoped explainer prompt

Read this when explaining a larger trace or combining findings. It can be used inline; no separate agent is required.

## Inputs

Question: `{question}`.

Traces and source anchors already gathered, if any: `{findings}`.

Available read surfaces and relevant version: `{context}`.

Read the actual code where a finding is uncertain or contradictory. If there are no findings, trace the mechanism directly. Reuse valid existing work rather than restarting exploration.

## Explain at the needed depth

Lead with what this subsystem does and where the relevant path starts. Add only the sections that help this reader:

- **Overview.** The smallest complete mental model.
- **Key concepts.** Real types, terms, and responsibilities.
- **Execution path.** Trigger, calls, data changes, decision points, outputs, and effects, with precise source anchors.
- **Where things live.** The files someone should open to work here.
- **Gotchas and gaps.** Non-obvious behavior and what could not be established.

Use concrete names: `UserService` calls `AuthClient.refresh()`. A short snippet or optional diagram can help when it clarifies actual traced relationships. Do not make a diagram mandatory.

Reconcile overlapping findings and check conflicting descriptions against source. Preserve unresolved gaps and static-versus-executed limits. Explain how the code works without presenting a plausible rationale as documented intent.
