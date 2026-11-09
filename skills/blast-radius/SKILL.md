---
name: blast-radius
description: Trace what a proposed or actual code change could break beyond its diff, and test the facts its safety depends on. Use for "blast radius," "what could this break," or checking an existing-code assertion before designing against it.
license: MIT
metadata:
  source: "https://github.com/cursor/plugins/blob/6b0300214a09fd6029cfb7077043125758cd1fd2/pstack/skills/blast-radius/SKILL.md"
  source-revision: "6b0300214a09fd6029cfb7077043125758cd1fd2"
  source-files: "pstack/skills/blast-radius/SKILL.md"
  local-changes: "Kept consumer tracing and the proof ladder; added packaged contracts and source fidelity, labeled static/runtime limits, and made explanation and comparison helpers conditional without mandatory fan-out."
---

# Blast radius

Find the downstream breakage a symbol search alone misses, then establish the one or two facts the change's safety depends on. Use this before design when a brief asserts something about existing code; treat the assertion as a hypothesis until the actual consumer census supports it. This is an impact investigation, without automatic product edits or shipping actions.

## Trace the change

1. **Bind.** Record the proposal or diff, base and current artifact identity, intended behavior, and exclusions. Include relevant working changes and source assertions; distinguish facts read from code from assumptions about its consumers.
2. **Find the safety fact.** State the invariant that would clear the main risk, such as "this removes only already-dead cache entries." Name the actual failure if it is false. Completion means a checkable claim, not a list of possible callers.
3. **Follow real consumers.** Read changed exports, declaration files, runtime imports, package entry points, pinned dependency source and local patches. Trace wire formats, schema and database consumers, feature flags, other languages, build artifacts, and independently deployed clients. Check scheduling, retries, microtasks, unmount, and teardown where they affect the invariant.
4. **Check contracts.** Preserve public compatibility and exact source values: order, signs, units, precision, null versus absence, unknown fields, and identifiers. Trace real trust/privilege transitions, including internal ones. A controlled in-repo caller and an independently deployed consumer can need different migration strategies.
5. **Challenge the safety fact.** Use the cheapest decisive proof on the relevant artifact. Prefer a real import, packaged fixture, command, or actual surface over an internal substitute. Keep temporary probes within authorized scratch scope, clean only owned resources, and retain the evidence.

For each material claim, say how far this proof ladder reached:

| Level | What it establishes |
| --- | --- |
| Assumption | A proposition to investigate; no supporting proof yet. |
| Source anchor | Exact `file:line` or pinned dependency source supports the claim. |
| Reasoned/static proof | A complete path or deterministic contradiction establishes a static claim, with assumptions stated. |
| Executed code | A named command/test exercises the actual relevant code on identified inputs; retain actual and expected output. |
| Observed surface | The running packaged, native, UI, CLI, or API surface demonstrates the claimed behavior and side effects. |

A unit import can establish a library claim while leaving package exports or a native/UI journey unverified. A passing unit-test proxy cannot establish the real surface result. Keep each proof's scope explicit instead of requiring runtime evidence for every static fact or presenting static reasoning as an observed run.

## Resolve and report

Separate confirmed risks, cleared risks, and unresolved hypotheses. Each material risk names the causal path, affected consumer, exact source anchor, reachable preconditions, impact, evidence class, and cheapest next check. Do not invent probabilities, callers, or APIs; a scoped search that found no callers establishes only what was searched. An uncommon reachable data-loss, security, or concurrency defect retains its impact-based severity.

Use the `how` skill only when execution-path explanation is needed, the `why` skill only when intent/history matters, or the `agent-debate` skill only for a useful bounded comparison. Read an installed helper before using it; none is a prerequisite or a reason for automatic fan-out. Any independent comparison consumes the existing coordinator's finite shared budget and preserves requested providers and resource ownership.

Return what changed, the key safety fact and its proof level, confirmed risks with evidence, cleared paths, and unresolved limits with the next decisive check. Done when the consequential consumers are accounted for and every safety claim is supported at its stated level or explicitly unproven.

Read [references/SOURCES.md](references/SOURCES.md) when checking provenance and adaptations.
