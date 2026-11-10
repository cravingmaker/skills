# Examples

These are unrun paired-evaluation cases; offline fixture tests do not establish skill-selection benefit. Keep the catalog unevaluated until matched skill/no-skill runs are recorded.

## Activation

- "Our HTTP alert fires on a quiet service and stays quiet after the exporter disappears; fix its rules." Expect: inspect the signal contract and separate sparse-traffic, measured zero and collection failure before native rule tests.
- "Write recording rules and Alertmanager routing for these database signals, including restart and suspend gaps." Expect: read the PostgreSQL signal adapter, preserve NULL/absence/reset semantics and test rendered rules and receiver selection.
- "This latency rule averages instance p99 values; replace it with a service-level signal and prove the result." Expect: use appropriate bucket or native histogram aggregation and an unequal-traffic counterexample.

## Near miss

- "Set an SLO target and decide how much error budget we may spend before paging." Expect: the `slo-error-budgets` skill owns eligibility, target and policy; rule mechanics load only when requested.
- "Add request counters to our application without changing any alerts." Expect: the `opentelemetry-instrumentation` skill owns application instrumentation.
- "Install host disk checks; no Prometheus rules need changes." Expect: the system-monitoring owner handles host checks without loading rule authoring for incidental monitoring vocabulary.
- "Run deploy-checklist for the release." Expect: the existing deployment-readiness process handles this request without manufacturing alert work.
- "Use incident-response to coordinate this outage and status updates." Expect: the existing incident process owns coordination; rule authoring applies only to a concrete rule defect.

## Outcome

- "Prove reset and weighted aggregation behavior." Fixture: tests/prometheus-alerting-rules/fixtures/rules.json and rule-tests.json, with two counters whose resets differ and two histogram populations weighted 900 to 100 per interval. Expect: native tests pass, the unweighted fraction mutation produces 0.75 instead of the independent 0.55 oracle and is rejected, then restoration passes.
- "Prove database missing-data handling." Fixture: expected target cluster demo, collector_ok measured as zero, absent or stale; replication lag absent for a NULL source versus an explicit zero; archive failure and epoch change; freeze and retained-WAL pressure followed by recovery. Expect: all selected native state assertions pass and actual least-privileged collector replay is named unrun unless separately executed.
- "Prove page and fallback routing." Fixture: alertmanager.json has pager, tickets and fallback receivers with no external integrations. Expect: matching page/ticket labels select their receiver, unknown/missing ownership selects fallback, an incorrect receiver assertion fails, and no delivery or inhibition proof is claimed.
- "Review the completed rule package." Expect: every alert has severity, owner and runbook_url; rendered-rule/config hashes and native versions are retained; unavailable SQL collection, inhibition and external notification checks remain separate.
