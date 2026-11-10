# Changelog

Each entry records one merged pull request, newest first. The merged snapshot ends at PR #10 on 2026-11-09.

[PR #11](https://github.com/cravingmaker/skills/pull/11) (backend-engineer) and [PR #12](https://github.com/cravingmaker/skills/pull/12) (devops-engineer) were closed unmerged because their Outcome evals mostly matched the no-skill baseline at high token cost. Their skills are not part of this collection.

[PR #14](https://github.com/cravingmaker/skills/pull/14) removes the planned role entries, role template, and unused Android provider, and maps jobs to shipped skills. It keeps `agent-orchestrator` as the core router. It is open as of 2026-11-10, so it has no merged-PR entry here.

## Contents

- [PR #10: observed cutover and reservations](#pr-10-observed-cutover-and-reservations)
- [PR #9: Claude host evaluations](#pr-9-claude-host-evaluations)
- [PR #8: land the reviewed stack](#pr-8-land-the-reviewed-stack)
- [PR #7: shipping and continuity](#pr-7-shipping-and-continuity)
- [PR #6: design, build, and verification](#pr-6-design-build-and-verification)
- [PR #5: shaping and understanding](#pr-5-shaping-and-understanding)
- [PR #4: adoption tooling](#pr-4-adoption-tooling)
- [PR #3: the orchestrator role](#pr-3-the-orchestrator-role)
- [PR #2: the fleet foundation](#pr-2-the-fleet-foundation)
- [PR #1: the first capabilities and checks](#pr-1-the-first-capabilities-and-checks)

## PR #10: observed cutover and reservations

Merged 2026-11-09. [Release retired-source reservations](https://github.com/cravingmaker/skills/pull/10) after the observed user-host cutover.

The owned core was installed on Claude Code and Codex, repeat installs left it unchanged, and fresh sessions checked discovery and explicit-entry visibility. Matt's collection and its Codex marketplace entry were uninstalled; the other retired collections were already absent. Built-in and unrelated plugin name reservations remain. The recorded Claude interview entry opened its owned no-doc parent.

## PR #9: Claude host evaluations

Merged 2026-11-09. [Record the Claude Code host campaign](https://github.com/cravingmaker/skills/pull/9), extend earlier paired evidence, and complete final-byte follow-ups.

The harness gained effort recording, native slash-command observation, bundled-skill/fork isolation, private Bash temp handling, and visible-body read detection. It kept the listing/cat extension specific to Claude. Focused method changes addressed source-boundary mistakes in retrospectives, failed-probe accounting, narrow trigger descriptions, and overbroad handling of a named proof gap.

All core entries ended evaluated. The PR preserves invalid attempts, host-confounded denials, the one-off hidden-file read, protocol exceptions, and unavailable real surfaces. Evaluation status is coverage plus reviewed behavior, not a claim that every observation passed or that all manual file reads are prevented.

## PR #8: land the reviewed stack

Merged 2026-11-09. [Land the reviewed stack on main](https://github.com/cravingmaker/skills/pull/8).

PRs #2 through #7 had merged into their stacked parent branches rather than main. This PR brought the already reviewed stack tip to main, including the foundation, orchestrator, adoption tooling, core methods, evaluations, and cutover checklist. It did not introduce a new implementation on top of that reviewed content.

## PR #7: shipping and continuity

Merged 2026-11-09 into its stacked parent; landed on main through PR #8. [Adopt the shipping and continuity end of the workflow](https://github.com/cravingmaker/skills/pull/7).

PR drafting, delivery, CI triage, verified feedback, branch updating, takeover, retrospectives, handoffs, teaching, history lookup, and catch-up became owned methods. The shared delivery contract binds checks to the current revision, retains old unresolved reviews, follows repository-required gates, bounds review rounds, and restricts watchers to the root. Prepare-only delivery carries no-merge through helpers.

The final stacked head also contained Codex paired-evaluation follow-ups and native selected-skill activation detection (`2b9dbc1`, tightened by `531a651`). Those changes landed on main through PR #8.

The cutover checklist was added as a plan, not as proof of uninstall. Later PR #10 records the observed cutover.

## PR #6: design, build, and verification

Merged 2026-11-09 into its stacked parent; landed on main through PR #8. [Adopt design, implementation, diagnosis, review, and real-surface verification](https://github.com/cravingmaker/skills/pull/6).

One coordinator owns approved code-ticket execution, including worker/reviewer starts and final integration proof. Design and report-only review stay distinct from authorized repair. Verification-driver authoring has bounded-gap and full-map modes with namespaced names.

The wizard serializer now checks exact parser round trips and refuses unsupported values before writing. Architecture reports escape content and work offline by default, with pinned strict Mermaid only by explicit choice. Paired follow-ups and fixes remained part of the reviewed stack.

## PR #5: shaping and understanding

Merged 2026-11-09 into its stacked parent; landed on main through PR #8. [Adopt the main shaping flow and grounded explanation methods](https://github.com/cravingmaker/skills/pull/5).

Interviews, domain terms, specs, stable vertical tickets, triage, decision maps, questionnaires, project configuration, research, prototypes, prompt refinement, and answer repair became owned packages. The producer/consumer contract carries acceptance, exact source hashes, blockers, and named Proof from spec through tickets into execution and acceptance.

Descriptions and follow-up evaluations narrow accidental activation without reopening settled decisions or adding another planning pipeline.

## PR #4: adoption tooling

Merged 2026-11-09 into its stacked parent; landed on main through PR #8. [Add the tooling needed to own upstream methods](https://github.com/cravingmaker/skills/pull/4).

Invocation preference moved into the catalog. The Claude settings adapter and generated Codex policy implement explicit-only entries without host-specific frontmatter. Optional links became checked prose pointers; required metadata continues to drive installation.

Per-file provenance manifests, legal-file checks, effect-free script help, and reserved built-in names made later adoption reviewable. This PR added tooling rather than the adopted skill corpus.

## PR #3: the orchestrator role

Merged 2026-11-09 into its stacked parent; landed on main through PR #8. [Add the first role router and its coordinating methods](https://github.com/cravingmaker/skills/pull/3).

The role plans justified delegation, gives each task an owner and write boundary, preserves one finite budget, runs bounded evidence-led disagreement, and accepts integrated work by checking it. Standalone briefs and durable records let a successor resume without inventing missing results.

The initial profile was smaller than today's closure. Current generated metadata, not the historical PR's package count, defines installation.

## PR #2: the fleet foundation

Merged 2026-11-09 into its stacked parent; landed on main through PR #8. [Add the catalog, profiles, installer, authoring bar, and paired harness](https://github.com/cravingmaker/skills/pull/2).

The collection separates capability methods from role routers and computes dependency closures from skill metadata. The harness creates matched fresh sessions with candidate/no-candidate discovery, records effective host/model and actual bytes, and retains invalid or hurt results. Initial comparisons already demonstrated that a valid evaluation can contain an inaccurate answer.

## PR #1: the first capabilities and checks

Merged 2026-11-09. [Add the first communication and enforcement capabilities](https://github.com/cravingmaker/skills/pull/1).

The collection began with faithful lean communication, project enforcement, deliberate tooling upgrades, and checks against repeated agent mistakes. It added the standing communication contract, Vale style, pinned reference validation, repository package checks, fixture tests, and CI. Retained pstack material carries its license and source attribution.
