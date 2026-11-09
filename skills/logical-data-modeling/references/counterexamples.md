# Counterexamples

Read this when a logical identity or relationship rule needs falsifiable evidence. Build expected results from source facts before implementing the mapping.

| Case | Source facts | Required observation | Lossy alternative to reject |
| --- | --- | --- | --- |
| Identifier reuse | Issuer A uses code X for entity alpha in days 1–9 and beta in days 10–19; issuer B also uses X. | A trade at day 3 links to alpha; day 12 links to beta; B never matches A. | Grouping by code alone or applying today's identity to all history. |
| Ambiguous link | Source record Q has two candidate entities and no accepted link. | Q remains unresolved with both candidates retained. | Selecting the first candidate or creating two resolved facts. |
| Missing code | A fact with quantity 7 has no recognized code. | The fact and quantity 7 remain in reconciliation; its identity is unresolved. | An inner join silently discarding it. |
| Late correction | A source first reports quantity 10, then corrects it to 12 with a later recording time. | The earlier knowledge query returns 10 and the later query returns 12; both source claims remain. | Replacing the original or ordering by event time alone. |
| Fan-out | One order has lines 5 and 7 and two tags. | Its total is 12; attaching tags preserves the measure's grain. | Summing a raw line-to-tag join and obtaining 24. |

[The worked query](../assets/counterexamples.sql) computes these cases from small CTE relations without touching a database table. It runs in SQLite for the package's offline fixture tests; use equivalent native queries for the selected store and actual model. The expected values live in the test, independently of the query expressions. The tests also run deliberately lossy query variants and require different results.

Keep valid time (when a fact applies) separate from recorded time (when a claim became known). Choosing a historical policy or resolving source identity disputes is further work; record the question and owner instead of silently selecting a winner. The PostgreSQL physical mapping must carry these same cases into real constraint and consumer-query tests.
