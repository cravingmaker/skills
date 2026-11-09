---
name: architect
description: Design module interfaces inside one codebase with caller usage, type sketches, alternatives and a chosen rationale. Use for interface design or repeated special cases that suggest a module needs redesign.
license: MIT
metadata:
  requires: "codebase-design"
  source: "https://github.com/cursor/plugins/blob/6b0300214a09fd6029cfb7077043125758cd1fd2/pstack/skills/architect/SKILL.md"
  source-files: "pstack/skills/architect/SKILL.md"
  source-revision: 6b0300214a09fd6029cfb7077043125758cd1fd2
  local-changes: "Kept grounding, usage-first sketches, red-flag screening, interface-depth comparison, rationale and accepted-deviation reconciliation; blind alternatives come from the agent-debate skill instead of a copied arena run; declared design budget; stops at the design artifact unless implementation is authorized; merged exhaust-the-design-space and redesign-from-first-principles; removed model slugs, runner settings, mandatory tournaments and automatic rewrites."
---

# Architect

Sketch types, function signatures, class shapes and module structure with `not implemented` bodies and pseudocode, compare structurally different alternatives, and record the chosen design with its rationale. The **design artifact** is the deliverable; code follows only when implementation is already authorized.

Read the `codebase-design` skill (required) first: it supplies the vocabulary (module, interface, depth, seam, adapter) and the design principles this skill applies.

## Phase A: ground the problem

Build a real model of every system the new code touches. Read the affected code, its callers, the project's domain glossary and decision records; the `how` skill explains an unfamiliar subsystem and the `why` skill recovers the rationale behind an existing shape the design would change. Naming a file isn't grounding. Name the constraints the design must honor: existing types to interoperate with, callers you can't break, invariants, trust boundaries and public compatibility.

Skip Phase A only when the work is greenfield with no surrounding system. Done when every constraint the design must satisfy is written down with its source.

## Phase B: sketch and compare

1. **Declare the design budget.** State how many candidates you will produce and whether they need independent authors, before starting. Record inline candidates as inline work; count starts only for agents actually launched. Two structurally distinct candidates is the default; add a third when the design space has real contenders. Done when the budget is recorded.
2. **Write the caller's usage first.** For each candidate, write the README or quickstart a consumer reads and two or three realistic call sites, then derive the type sketch from them. When usage and types disagree, reconcile the sketch to the usage.
3. **Produce whole-shape alternatives**, not point fixes inside one shape, using the lenses in the `codebase-design` skill's design-it-twice reference. For a consequential choice where independent, blind candidates would improve the decision and the budget allows, use the `agent-debate` skill: it runs blind same-frame alternatives, evidence-led selection and grafting under its shared budget, and its result fills the rationale's synthesis section. Give each participant [references/candidate-brief.md](references/candidate-brief.md) inside its brief. Otherwise write the candidates yourself and label them sequential, not independent.
4. **Screen every candidate** against [references/design-red-flags.md](references/design-red-flags.md). Assume the next contributor is an agent that sees only the files it opened, copies the nearest example, and takes the shortest path that compiles; prefer the design where a change that looks right from one file is right for the whole repo.
5. **Compare on interface depth.** Prefer the design that hides more complexity behind a smaller, simpler public surface without dropping required checks or compatibility. A rich interface can keep call chains short by concentrating capability instead of scattering it across layers.

Done when the chosen design and at least one rejected alternative are recorded, with the comparison behind the choice.

## Phase C: deliver the design

Write the outputs: the caller's usage, then the type sketch (one file with new types and signatures for a small change; a module map plus type definitions for larger work), and the rationale shaped by [references/rationale-template.md](references/rationale-template.md).

Stop here and present the design, unless the request already authorizes implementation. For adversarial pressure on a design artifact, the `agent-debate` skill reviews its trade-offs. When candidate code exists, the `interrogate` skill can probe that code in report-only mode. If the human pushes back on the shape, treat that as Phase A evidence: re-ground and re-run Phase B before writing more code. Done when the design artifact exists and the next implementation step is named.

## Phase D: implement against the sketch (when authorized)

Replace `not implemented` bodies with code and pseudocode with logic, using the `implement` skill. The sketch is the contract. Deviations from it are signal to surface, not friction to absorb silently: if a function needs a parameter the sketch didn't anticipate, ask whether the sketch was wrong, the requirement was missed, or the implementation is overreaching.

Before closing each implementation unit or handing its contract to the next worker, reconcile accepted deviations: once the appropriate owner accepts a change, update the affected usage, outcome contracts, signatures and ownership in the existing design and rationale, and record the acceptance source there. A local deviation that leaves the shared contract intact needs only a recorded reason. Keep unaccepted changes and unresolved disagreements visible, and never edit the design merely to justify what was built.

## Phase E: redesign when the architecture is wrong

If implementation keeps producing friction the sketch can't absorb, don't bolt fixes onto a wrong design. The signal is a *pattern*, not single instances:

- The same shape of workaround appearing repeatedly across unrelated code.
- Multiple unrelated edge cases that all need special-case branches.
- Types that need escape hatches (`any`, casts, optional fields always set in practice) to compile.
- The "we need a lock" reflex when the sketch said the state wasn't shared.
- Callers having to know the abstraction's internal rules to use it.
- Two or more independent Phase D deviations of the same shape.

Use judgment. A few edge cases don't condemn an architecture, and complexity in the data is not complexity in the design.

When the pattern holds, redesign as if the new constraints had been day-one assumptions: re-ground on what's been built, consider removing redundant mechanisms before adding new ones, preserving required behavior, trust boundaries and compatibility even when the sketch must grow, and return to Phase B within the declared budget. Propagate the change through every reference: types, docs, examples and rationale. Present the redesign as a proposal; rewrite built code only within the authorized scope, and deliver it in increments that each keep the contract.

## Provenance

Adapted from pstack's architect skill and its exhaust-the-design-space and redesign-from-first-principles principles, with the pstack-claude port's reconciliation rules. See [references/SOURCES.md](references/SOURCES.md), `LICENSE-pstack` and `LICENSE-pstack-claude`.
