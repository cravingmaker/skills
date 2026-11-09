# Reviewer brief

Use this frame for one independent reviewer or each seat in a report-only panel. Resolve every field from the task and artifact before dispatch; a path is sufficient only when the reviewer can access its exact contents.

```text
Review only. Do not edit product files, the index, HEAD, or branch state; do not commit, push, post, merge, or start reviewers.
Repository/artifact: <absolute locator and content identity>
Pinned base and comparison: <full SHA, semantics, exact diff/status commands>
Scope: <paths, staged/unstaged changes, relevant untracked files and their identities>
Intent and exclusions: <accepted request, preserved constraints, out-of-scope work>
Standards sources: <exact rules and source pointers>
Spec and accepted decisions: <exact source pointers, or no spec available>
Checks already run: <commands, revision, results, pre-existing failures and limits>
Mode: <standard or probe; single reviewer or panel; assigned lens>
Budget and scratch scope: <reserved seat, finite attempts/time, owned disposable location>
Prior findings: <stable IDs, status, evidence and unresolved probes, if any>

Report Standards and Spec separately. Cite each rule/requirement and exact file:line.
Read surrounding code and affected callers, including runtime exports, compatibility and trust transitions.
Grade by impact. Treat smells and size as investigative cues; retain necessary guards and rationale.
For probe mode, run runtime hypotheses against this artifact and return the exact action/command, actual versus expected output, and evidence identity.
Label deterministic source proof static. Keep unrun runtime allegations unresolved.
Return stable IDs, severity, affected consumer, evidence class, smallest remedy, and limitations.
List material concerns set aside and why. No supported findings is a valid result.
```

Freeze the scoped bytes while a reviewer works or bind the report to its earlier snapshot. A later edit invalidates only evidence it affects; recheck those claims against the new identity. For multiple seats, collect independent reports before sharing findings, then reconcile evidence within each axis. Record actual provider/model/effort only when exposed, and keep unavailable or failed seats visible.
