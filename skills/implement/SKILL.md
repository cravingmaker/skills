---
name: implement
description: Build one approved piece of work from its spec or ticket, prove the result, and self-review it. Use when the user asks to implement a ticket, a spec slice or an agreed change, or when a coordinator briefs a worker to build one ticket.
license: MIT
metadata:
  requires: "tdd change-review"
  source: "https://github.com/mattpocock/skills/blob/49dd158d1076134a641b33efb035946536778336/skills/engineering/implement/SKILL.md"
  source-files: "skills/engineering/implement/SKILL.md"
  source-revision: 49dd158d1076134a641b33efb035946536778336
  local-changes: "Kept ticket lookup, tdd at agreed seams, regular checks and a closing review; merged pstack's feature and refactoring playbooks, the deslop cleanup and Superpowers' executing-plans rulings and completion contract; a leaf self-reviews and returns evidence while the coordinator owns independent review; commits stay within current authority; no second controller."
---

# Implement

Implement the one piece of work described in the spec, ticket or agreed change. **One slice, proved, reviewed.** A leaf worker returns evidence to its coordinator; it does not start other agents.

## Steps

1. **Identify the work.** If given a ticket reference, fetch it from the configured tracker and state its title before starting; if the reference is ambiguous, ask. Read the spec or ticket's acceptance checks, Proof line and agreed test seams. Reuse decisions already approved there; do not interview the user again or redesign the slice. Done when you can name the outcome, the Proof and the files you expect to touch.

2. **Ground and pre-flight.** Read the code the change touches, the project's domain glossary and the decision records in that area; the `how` skill helps on an unfamiliar subsystem. Check the work for contradictions with the spec, with earlier tickets' interfaces and with itself. Rule on each with the spec as the binding authority, record `Ruling: <what> — <why> — <cost if wrong>` (in the run record when one exists, otherwise in your report), and continue. Done when every conflict you found has a ruling.

3. **Build.** Choose the branch that fits:
   - **Behavior change or bug.** Use the `tdd` skill where the change has a meaningful seam; a trivial, reversible change needs no new test. Build narrow vertical slices with the data shape chosen first (the `codebase-design` skill).
   - **Refactoring.** Pin the behavior contract first with a characterization test, snapshot or equivalence check; type checks and lint are not a pin. Move in small behavior-preserving steps, each keeping the pin green. Update controlled callers in the same change; keep compatibility, or expand then contract, for public or independently deployed consumers. If the cleanup reveals a missing feature or a real bug, split it out.

   Preserve exact values, numeric precision, unknown fields, legal notices, rationale comments, defensive checks at real trust boundaries and others' work. Spot-check every rename against the actual files; renames miss usages in strings and docs. Done when the slice's acceptance checks are met in the code.

4. **Check as you go.** Run type checks and single test files regularly, and the project's relevant full suite once at the end. Read every output. A failure you did not cause still goes in the report by name. Done when the final suite run and the Proof both have a command and an observed result.

5. **Clean the diff.** Compare your change with its base and remove clutter you introduced: comments that restate the code or break local style, defensive checks or try/catch that are abnormal for a trusted internal path, casts that only silence the type checker, needless nesting, and patterns inconsistent with the surrounding code. Keep behavior unchanged, edit only your own lines, and rerun the checks after cleanup; revert any edit whose check fails. Done when the diff contains only what the slice needs.

6. **Review.** Self-review the diff with the `change-review` skill's rubric against the spec or ticket: missing, extra or misunderstood requirements, then quality, each with file:line. Fix what you find. As a leaf worker, stop there and return the evidence; the coordinator decides on and starts any independent review. Run alone at the top level, you may reserve one independent reviewer when the risk warrants it and it is authorized; label an inline review as yours, never as independent. Done when your own review is clean or every remaining finding is listed.

7. **Commit and report.** Commit to the current branch when committing is within the task's authority; push, open PRs or update the tracker only when that is authorized too. Report result first (COMPLETE, PARTIAL or BLOCKED), then the Proof with its command and observed result, the suite result, files and commits, rulings, review findings left open and anything unresolved.

## Stops

Four things stop you: an irreversible or destructive operation, a security-sensitive action, a side effect outside your task's authority (a merge, a push to a shared branch, a publish), and work so contradictory that every path forward is a guess. Report BLOCKED with what you tried and what you need. Decide everything else, record the ruling, and keep going.

Done when the slice's Proof passes with observed evidence, the relevant suite ran, the diff is clean, your review is recorded, and nothing outside the slice changed.

## Provenance

Adapted from Matt Pocock's implement skill, with material from pstack's feature and refactoring playbooks, the deslop skill (Cursor team kit, via the pstack-claude port) and Superpowers' executing-plans skill. See [references/SOURCES.md](references/SOURCES.md) and the `LICENSE-*` files.
