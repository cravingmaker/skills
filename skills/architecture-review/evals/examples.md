# Examples

Run matched examples with and without the final skill only within the authorized model budget. These cases are prepared, not executed.

## Activation

- "Review the architecture before we extract billing into a service." Expect: prioritize concrete scenarios, generate dependency evidence, and trace a transaction and recovery journey.
- "Audit ownership and replay in this source-to-warehouse pipeline." Expect: trace actual writers, physical-to-semantic mappings, durable acknowledgement, and reconciliation.
- "Is this architecture proposal internally consistent?" Expect: one contradiction and trade-off pass; runtime uncertainties become bounded probes.

## Near miss

- "Review this pull request diff." Expect: the `change-review` skill owns diff review.
- "Design two interfaces for this cache." Expect: the `architect` skill owns a new interface shape.
- "Find codebase modules that would benefit from deeper interfaces." Expect: the `improve-codebase-architecture` skill owns the requested candidate report.
- "Audit accepted ADR immutability and compare two store options." Expect: the `architecture-decisions` skill owns those checks.
- "Enforce the service layer direction." Expect: the `architecture-fitness-functions` skill owns dependency enforcement.

## Outcome

- "Support the recovery finding." Fixture: an API commits an order, publishes directly to a broker, then responds; a fault hook can crash between commit and publication. Expect: report the exact source path and scenario, distinguish code inspection from an executed fault test, and propose the smallest repair or probe.
- "Do not turn churn into severity." Fixture: Git history changes a generated file more than transaction code, but the latter has an evidenced lost-acknowledgement path. Expect: churn remains an inspection aid; findings follow quality-scenario evidence, with generated/excluded roots and history limits stated.
- "Resolve real data mappings." Fixture: the register calls a field gross revenue, a transform subtracts tax, and the consumer labels it gross. Expect: cite the transform and consumer mapping, name the semantic uncertainty and owner, and avoid claiming the register enforces semantics.
- "Handle unavailable execution honestly." Fixture: source and manifests are available, production and CI traces are not. Expect: trace the critical journey from source, give bounded runtime probes and unrun checks, and make no capacity or restore guarantee.
