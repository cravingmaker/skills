# Candidate brief

Read this when asking another agent, or yourself, for one candidate design. Include it in a participant's brief when the `agent-debate` skill runs the alternatives; the brief also carries the task, the Phase A grounding, an isolated place to write, and the output path. Adapted from pstack's architect/references/runner-prompt.md.

You are producing one candidate design. Output a design package: the caller's usage, a type sketch, function signatures, a module map, and a rationale shaped by the architect skill's rationale template.

Apply this discipline; candidates are compared on these points:

- **Caller's usage first.** Write the README-style usage and two or three real call sites before the types, then derive the type sketch from them. The usage is the spec; reconcile the sketch to the usage, not the reverse.
- **Data structures first.** Get the core types right and the code becomes obvious. Trace each dominant access pattern through the proposed structure. If the answer is "we'll add a map, index or cache later", the structure is wrong.
- **Interface depth.** Compare the capability hidden behind the public surface with the size of that surface. Prefer a simple interface that pulls complexity into the callee. Keep transport and wire types off the public interface; parse into domain types behind it.
- **Shared state.** If two actors might both write, ask "what happens?" If the answer isn't "nothing", default to per-actor state with a merge where it is read.
- **Visible structure.** `not implemented` errors for bodies, `// TODO` pseudocode for tricky logic, and doc comments stating intent and invariants. A reader should trace data from input to output by reading types and signatures alone.
- **Invariants in types.** Hard-to-misuse types beat runtime checks, which beat prose comments.
- **Validate at trust boundaries, trust types inside.** Business logic as pure functions; the shell stays thin. Keep the checks that real trust transitions require.
- **One source of truth per invariant.** Derive instead of syncing.
- **Idempotent state transitions** where applicable: ask what happens if the operation runs twice or crashes halfway.
- **Short call chains.** A flow spanning several files is a cue to inspect reader cost. Flatten only when it improves local understanding while preserving ownership, trust boundaries, compatibility and required checks.
- **Compatibility.** State which existing callers change and how; public consumers need an expand-then-contract path.

Produce the best design you can under your lens. Don't hedge toward a safe middle: the differences between candidates are what the comparison uses.
