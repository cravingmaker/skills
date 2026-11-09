# Examples

Paired model runs are deferred; keep this package unevaluated until the adoption harness records runs with and without it.

## Activation

- "Our CRM and trade feed reuse customer codes differently; define the logical entities and identity crosswalk." Expect: issuer/lifecycle rules, a logical model, unresolved links and independent query fixtures.
- "Review this cross-store data model: does one row mean an order, a line or a revision?" Expect: explicit grain and cardinality in both directions before a physical redesign.
- "A code is reassigned and corrections arrive late; model what consumers should join." Expect: distinct stable entities, source claims and unresolved temporal policy, with expected historical results.

## Near miss

- "Rename the domain glossary term and record its settled definition." Expect: the `domain-modeling` skill, when installed and read; no new logical schema.
- "The logical model is agreed; add PostgreSQL keys and tenant-safe foreign keys." Expect: the `postgres-schema-design` skill, when installed and read.
- "Design a sales mart's dimensions and define its as-of reporting policy." Expect: the analytical/temporal modeling job, using a supplied logical crosswalk; no claim that this capability owns the mart.

## Outcome

- "Check question and mapping coverage." Fixture: remove all `questions`, change an entity's `serves` ID to `missing`, or blank a mapping's `grain` in separate copies of `assets/model-example.json`. The checker rejects each; empty models and duplicate JSON members never pass.
- "Check a dangling mapping." Fixture: copy `assets/model-example.json`, replace one mapping's `entity` with `missing-entity`; `scripts/check-model.py` exits 1 with a field-path finding. The unchanged model exits 0 and reports one unresolved question.
- "Prove identifier reuse and unresolved links." Fixture: run `assets/counterexamples.sql` using SQLite; expected early/later identities are alpha/beta, ambiguous candidate/accepted counts are 2/0, and unresolved quantity is 7. A join without issuer/effective bounds must differ.
- "Prove late corrections and fan-out safety." On the same fixture, quantities before/after correction are 10/12 and the order total is 12. Always choosing the latest claim loses the earlier answer; summing the raw line/tag join produces 24 and fails the oracle.
