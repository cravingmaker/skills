---
name: logical-data-modeling
description: Define entities, identity, cardinality, grain and lifecycle when source systems or consumers disagree about what records mean. Use for a cross-store logical model, reused identifiers or ambiguous relationships; deliver the model and a source-to-physical crosswalk.
license: MIT
---

# Logical data modeling

Preserve what a record means before choosing how to store it. Deliver a logical model, a source-to-physical crosswalk and counterexamples that distinguish a faithful mapping from a plausible lossy one.

## Establish the meaning

1. Read source definitions, actual example records, existing keys and the consumer questions that the model must answer. Give each question a stable ID, consumer and input/output grain, and link each entity to the questions it serves.
2. Name the entity, one-row grain, identifier issuer and scope, valid period, recorded corrections, and creation/retirement behavior for each record family.
3. Separate a stable entity from its names, source codes and versions. Cite the issuer documentation or observed source records, with the observation date, for key stability and reuse rules. Keep an unverified rule in the owned unresolved questions.
4. State cardinality and optionality in both directions. Name the evidence for a one-to-one claim, the unresolved cases and the consumer behavior when a link is absent or ambiguous.
5. Preserve source claims and rejected alternatives. A missing code, unresolved identity or late correction remains distinguishable from zero, a new entity or overwritten history.

Done when each consumer question has a declared input grain, output grain, identity rule and handling of unresolved meaning. Use the `domain-modeling` skill, when installed, for vocabulary or domain ADR edits; read its `SKILL.md` before use. This job supplies logical identity and relationships rather than a replacement glossary.

## Check references before physical design

Use the project's model format when it already has equivalent checks. Otherwise compare the starter in [assets/model-example.json](assets/model-example.json) with the project and adapt it; read it when a machine-readable model is needed. Read [references/model-format.md](references/model-format.md) when preparing JSON for the reference checker.

```sh
python3 scripts/check-model.py path/to/model.json
```

The Python 3.12+ helper reads one JSON file, checks stable IDs and references, and prints a JSON summary. It exits 0 for consistent references, 1 for findings, and 2 for usage or unreadable input; diagnostics go to stderr. It has no database, network or write path. A pass with unresolved questions is incomplete semantic evidence; report the unresolved count and owners.

- Every key and relationship resolves to declared fields and an entity.
- Every entity has a mapped destination or an explicit unbuilt/unresolved reason.
- Each source mapping retains its issuer, version and correction rule in `identity_rule`, and declares its destination grain. Compare source and destination grain explicitly before collapsing revisions or relationships.
- A physical constraint or join must refer back to the supplied logical rule instead of silently changing it.

Done when reference checks pass and the crosswalk names how every entity reaches a source and physical destination, including gaps.

## Try to disprove the model

Read [references/counterexamples.md](references/counterexamples.md) when proving identity or relationship semantics. Run independent consumer questions over identifier reuse, ambiguous links, missing codes, late corrections and a join that could multiply a measure. Use hand-calculated expected rows, keys and quantities from source facts, independent of the proposed transformation. Keep unresolved records in the reconciliation totals. A diagram, schema-valid JSON or matching record count cannot establish semantic correctness.

Done when the source-to-consumer results preserve the declared identity and grain, each lossy alternative fails its counterexample, and unresolved choices remain explicit. Read [assets/counterexamples.sql](assets/counterexamples.sql) when running the offline SQL example; it illustrates these oracles rather than validating the user's model.

## Deliver and route

Return the model, crosswalk, answered questions, exact query results and unresolved decisions with owners. If physical PostgreSQL constraints are needed, use the `postgres-schema-design` skill when installed, reading it first, and carry the same counterexamples into database tests. For analytical marts, historical as-of policy, cross-source reconciliation or contract publication, hand over the model and unanswered questions to that job's owner; keep those separate deliverables.

## Sources

Read the [data modeling overview](https://www.ibm.com/think/topics/data-modeling) when distinguishing conceptual, logical and physical artifacts. Verify platform-specific key or temporal behavior against the selected engine's official documentation at use time; the logical model makes no version-support claim.
