---
name: architecture-decisions
description: Audit accepted ADRs and test consequential architecture options when recovery, concurrency, precision, or operating constraints decide a hard-to-reverse choice. Use for decision-integrity checks or comparable datastore trials. ADR writing stays with domain-modeling.
---

# Architecture decisions

Protect durable reasoning and produce evidence that can disqualify an option. Keep the project's ADR format and location. The deliverable is an integrity audit or a comparable trial record. Writing or superseding an ADR belongs to the `domain-modeling` skill; ordinary interface alternatives belong to the `architect` skill. Read a selected skill before using it. These are optional routes; integrity audits and domain trials work on their own.

## Audit the existing record

1. Find the configured ADR directory, status convention, acceptance authority, and trusted base revision. Use the existing integrity checker if it covers accepted reasoning and supersession. Otherwise run `python3 scripts/check-adr.py ADR_DIRECTORY --base BASE_REF` from this skill's directory.
2. Check numbered identities, statuses, reciprocal supersession, and changes to recorded reasoning. Read [supported ADR forms](references/adr-integrity.md) when selecting inputs or interpreting a finding. A format the helper cannot represent needs an equivalent native check; preserve the existing records.
3. With `--base`, a new accepted file or a transition to accepted needs `--signed-off NUMBER` for each number, repeated as needed. Supply it only after the user signs off; the flag records acknowledgement, not proof of permission. Agents still draft as proposed. A proposed successor may link the current decision without replacing it; activate reciprocal supersession only when the owner accepts the replacement.
4. Follow each Confirmation to the actual rule, experiment, or observed result. Distinguish planned, configured, locally executed, and deployed evidence. The helper reports the presence of Confirmation; it cannot establish its truth.
5. Report defects with the path, base revision, failed check, and smallest repair. Preserve accepted reasoning and use a new record to change a decision. Let the established authoring method make authorized status and supersession edits.

Done when every record in scope is accounted for, accepted history is intact or a defect is reported, effective supersession resolves both ways, and confirmation claims have evidence or a stated gap.

## Test an option that could change the decision

1. Name the consequential choice and the uncertainty that could overturn it. Reuse supplied invariants, workload, loss tolerance, and recovery objectives. Include the status quo or a focused repair when viable.
2. Declare disqualifying cases and independent expected results before testing candidates. Include recovery after a durable write, concurrent writers, exact precision, and operating limits where they decide the choice. A faster candidate that loses required values fails.
3. Hold logical inputs, result semantics, resource budgets, cache state, concurrency schedule, and failure points comparable. Record differences that prevent a fair comparison. Read [data-store selection](references/data-store-selection.md) for datastore trials. If reporting measured speed or cost advantages, use the `benchmark-checklist` skill when installed.
4. Run bounded trials only on explicitly disposable targets. Record input and result hashes, commands, candidate versions, failures, errors, recovery results, and unrun cases. Stop at the declared budget; inconclusive evidence stays inconclusive.
5. Supply evidence, the accepted disadvantage, reversal cost, and revisit trigger to the decision owner. Use the `domain-modeling` skill when an authorized ADR write is needed. An agent-authored ADR remains `proposed`; one-way choices need user sign-off.

Read [analytical table formats](references/analytical-table-formats.md) when comparing immutable Parquet manifests with DuckLake, Iceberg, or Delta. Read [service boundaries](references/service-boundaries.md) when independent deployment is the disputed benefit. Read [data ownership](references/data-ownership.md) when consistency or write authority is at issue. Read [data mesh applicability](references/data-mesh-applicability.md) only when organizational ownership is part of the choice. Read [ADR failure checks](references/adr-failure-modes.md) when reviewing a record's argument. Use [the trial record](assets/option-trial.md) and [the quality scenario](assets/quality-scenario.md) where the project lacks equivalents. They supply evidence fields, not another ADR template.

Verify runtime support, datastore behavior, service limits, prices, and technology licenses at use time against official vendor documentation for the exact deployed or tested release. Keep credentials and personal data out of evidence; destructive operations require explicit user confirmation.

Done when each viable option has the same declared oracle, observed results or explicit gaps, and a recommendation whose decisive constraint and downside are visible. Trials neither accept an ADR nor authorize a migration.
