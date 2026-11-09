---
name: architecture-review
description: Audit a system against prioritized quality scenarios using dependency graphs, churn, and a traced critical journey. Use for architecture reviews or large-refactor risk assessment, including data ownership and recovery. Return evidence-backed findings; ordinary diff review uses change-review.
---

# Architecture review

Find architectural risks that matter to an actual journey and quality requirement. Return evidence-backed findings, sensitivity points, trade-offs, and unresolved probes. The default is report-only. This capability supplies domain evidence; it does not run a generic review loop or choose a new design.

For a diff, use the `change-review` skill. For a named module's interface alternatives, use the `architect` skill. For deepening candidates inside one codebase, use the `improve-codebase-architecture` skill when installed. Read the selected skill before relying on it.

## Establish the review frame

1. Fix the system boundary, inspected revision, users, and authorized reads and probes. Reuse the task's constraints and record unavailable repositories, environments, or history.
2. Read manifests, lockfiles, configured ADRs, ownership, deployment wiring, and relevant incidents. Separate requirements, observations, and assumptions.
3. Prioritize concrete quality scenarios by business importance and uncertainty. Each names a source, stimulus, artifact, operating conditions, response, and measurable result. Read [quality scenarios](references/quality-scenarios.md) when turning a broad goal into a review question. Call this a lightweight scenario review; a table alone does not constitute a full ATAM evaluation.

Done when each important review question has a scenario and a way to obtain evidence.

## Gather evidence before findings

1. Generate a dependency graph with installed project tools. Examples include dependency-cruiser, `cargo metadata --format-version 1 --locked`, `cargo tree -e normal -i CRATE`, or an existing Nx graph. Include composition roots, aliases, generated code, normal/build/dev edges, and the supported target or feature scope. Check syntax against the installed tool's help and official documentation.
2. If history exists, run `python3 scripts/churn-hotspots.py --repo REPOSITORY --since WINDOW`. The read-only helper ranks added-plus-deleted lines multiplied by current file bytes at the inspected revision. Use the ranking to choose inspection candidates; it measures neither complexity nor a defect. Read [evidence limits](references/evidence.md) for history scope and the JSON contract.
3. Trace one critical journey through validation, authority, state transition, transaction, external effect, and response. Include job or event acknowledgement and recovery when crossed. Cite source locations and collect a trace or integration result when execution is authorized. A source trace supports control-flow claims; runtime claims need runtime evidence.
4. For data-heavy systems, follow a real source-to-consumer path and its restore or replay path. Read [data landscape review](references/data-landscape-review.md) for ownership, exact values, and unresolved mappings. A catalog entry, backup setting, or control register alone does not prove enforcement.

Done when graph scope, history scope, and the journey are inspectable, and missing proof is labeled.

## Judge the scenarios

For each important scenario, connect a tactic to its evidence and failure condition. A sensitivity point is a parameter whose change materially affects a scenario. A trade-off point improves one goal while harming another. State affected behavior and conditions instead of unsupported numeric scores.

Keep reproduced defects, conditional risks, optional improvements, and unavailable checks distinct. A plan gets one contradiction and trade-off pass against its stated constraints. Turn runtime uncertainty into a bounded probe with a falsifying result; more review rounds cannot supply runtime evidence. Use [the review report](assets/review-report.md) when the project has no required format. Each finding names severity, scenario, evidence at the inspected revision, consequence, smallest remedy, verification, and owner.

Use the `architecture-decisions` skill when a finding warrants accepted-record checks or comparable option trials. Use the `architecture-fitness-functions` skill when it warrants an import or crate rule. Hand threat depth to the security owner with the exact trust boundary and evidence.

Run load, fault, and security probes only against owned, authorized targets. Diagnostic access does not authorize data changes. Minimize personal data and redact secrets in traces and reports. Verify platform support, limits, and technology licenses live against the exact vendor release before asserting them.

Done when every finding has scenario-specific evidence and a repair or probe, important scenarios have outcomes or explicit gaps, and the next owner can act without reconstructing the review. Report local, CI, and deployed observations separately.
