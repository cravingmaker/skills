---
name: change-review
description: Review a branch, PR, or working change against repository standards and its agreed spec, reporting the two axes separately. Use for a scoped change review or adversarial probe review; explicit Claude Code built-ins code-review and review keep their own routes.
license: MIT
metadata:
  source: "https://github.com/mattpocock/skills/blob/49dd158d1076134a641b33efb035946536778336/skills/engineering/code-review/SKILL.md"
  source-revision: "49dd158d1076134a641b33efb035946536778336"
  source-files: "skills/engineering/code-review/SKILL.md"
  local-changes: "Renamed the entry; kept separate Standards/Spec axes; added scoped probe and panel modes, caller tracing, impact-based severity and distinct evidence classes; removed fixed fan-out, size vetoes, vote weights and automatic fixes."
---

# Change review

Report whether the agreed change meets **Standards** and **Spec**, keeping each axis's findings and conclusion separate. This pass is report-only: it does not edit product code, apply fixes, commit, push, post, or merge. The host's explicit `code-review` and `review` entries remain distinct; incidental or quoted names do not select this skill.

## Pin the review

1. **Scope.** Resolve the requested base to a full commit SHA and record the comparison semantics: exact commit range or merge-base with the named branch. Reuse an established base; ask only when the choice changes the review. Capture HEAD, status, scope paths, and identities of the reviewed contents. An invalid ref stops the pass; an empty scope returns no changes to review.
2. **Working state.** Include staged, unstaged, and relevant untracked files when the request covers work in progress. A committed three-dot diff alone misses them. Compare the pinned base with the working tree, inspect relevant untracked contents separately, and preserve unrelated work. Do not stash, reset, switch the shared checkout, or silently omit dirty files. A delegated copy must contain the same scoped bytes; record any omissions.
3. **Intent.** Read the supplied spec, approved decisions, linked issue, and PR description using the configured tracker and sufficient connected tools first. Find facts before asking. When no spec exists, say so and report the Spec axis as unavailable; do not invent requirements or demand tracker setup for a local review.
4. **Standards.** Read applicable AGENTS.md, CONTRIBUTING.md, CODING_STANDARDS.md, and scoped conventions. Identify existing check commands and actual results. Tooling handles deterministic rules it enforces; cite its output when relevant and spend judgment on uncovered rules. A configured check that was not run is not a pass.

Done when the base, reviewed artifact, dirty scope, standards sources, spec source or absence, and exclusions are explicit.

## Apply both axes

- **Standards.** Cite a documented rule and the changed behavior that breaches it. Label uncodified design advice as judgment. Use [references/lenses.md](references/lenses.md) when checking structural smells, correctness, security, developer setup, or feature gates. Repository rules override heuristic smells.
- **Spec.** Map acceptance requirements to implemented behavior, missing or partial work, incorrect behavior, and unapproved departures. Cite the requirement. Separate an inferred user expectation from an explicit requirement, and explain its concrete impact; spec silence does not excuse a reachable defect or authorize a new feature demand.
- **Reach.** Read surrounding code and trace changed behavior into affected callers, exported declarations, wire/storage contracts, independently deployed consumers, and real trust transitions, including internal privilege boundaries. A caller outside the diff can expose a defect caused by this change. Keep unrelated pre-existing defects outside the finding count and name excluded concerns where material.
- **Fidelity.** Check exact source values, order, signs, units, numeric precision, null versus absence, unknown fields, identifiers, and public compatibility. Preserve required defensive checks, rationale, and legal comments when proposing a remedy.

Keep the axes separate even when both cite the same root cause; cross-reference their IDs rather than combining their counts or ranking one axis against the other.

## Select the evidence mode

The default is a source-backed review using relevant existing checks. **Probe mode** adds bounded adversarial attempts to break the real change: choose concrete hypotheses, expected results, safe inputs, and a finite attempt/time budget before running. Runtime claims in probe mode need a run against the reviewed code, with the exact command or action, actual and expected result, environment, and evidence location. Recheck a received runtime finding when the relevant surface is available; a failed setup, timeout, or unavailable tool leaves that claim unresolved. Sound deterministic static findings remain valid without a runtime run: show the source chain or deterministic contradiction and label it static. An unexecuted runtime allegation remains a hypothesis, not a verified runtime finding. An internal unit-test proxy does not prove a packaged, native, or UI surface result.

Read [references/reviewer-brief.md](references/reviewer-brief.md) when requesting a reviewer or opening **panel mode**. The coordinator reserves every independent reviewer, replacement, and retry within the existing shared budget: at most eight live subagents or the lower host/user limit, finite total starts, and declared rounds. Use requested providers as requested; report an unavailable member without substitution or invented participation. Independent seats receive the same scope and evidence frame, work read-only, and start no nested reviewers. Inline review is valid when independence is optional; label it honestly. Combine verified evidence within each axis by root cause, retain conflicting evidence and unresolved IDs, and give repeated findings no extra weight. Probe scratch files and disposable fixtures stay outside the product checkout, within current authority, with owned cleanup and retained evidence.

## Report

State the base, HEAD/content identity, scope, mode, checks, and any missing reviewer or evidence first. Then present **Standards** and **Spec** separately, with a conclusion and finding count for each. Each finding has a stable ID, impact-based severity, exact `file:line`, rule or requirement, trigger and affected consumer, evidence class, evidence pointer, and smallest justified remedy. Use **critical/high** for evidenced severe security, data loss, or major functional impact; **medium** for meaningful bounded breakage; **low/advice** for limited impact or design judgment. Rarity alone does not lower a reachable serious defect's severity, and size, complexity, overlap, or reviewer agreement alone does not raise it. List unresolved runtime hypotheses and declined or out-of-scope concerns with reasons; distinguish them from proven findings. Return "no supported findings" when appropriate, with the limits of the pass; review completion grants no fix or shipping authority.

Read [references/SOURCES.md](references/SOURCES.md) when checking provenance, source hashes, and adaptation boundaries.
