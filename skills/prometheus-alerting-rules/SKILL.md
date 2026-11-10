---
name: prometheus-alerting-rules
description: Write or repair Prometheus recording rules, alerts and Alertmanager routes when an alert is noisy, never fires or misses recovery. Test rate and histogram math, missing data and routing; use the PostgreSQL signal adapter for database collector semantics.
license: MIT
metadata:
  verified: "2026-11"
---

# Prometheus alerting rules

Deliver versioned rules, routing and synthetic evidence for an explicit signal contract.

## Bind the signal

Inspect the deployed Prometheus, Alertmanager, exporter and rule-generator versions, scrape/evaluation intervals, existing CI and configuration ownership before editing. Use the project's pinned native tools; resolve missing versions from official releases and verify downloaded checksums. Read [references/sources.md](references/sources.md) when checking current syntax, native histogram support, matcher behavior or lint-tool configuration.

Record the eligible population, unit, aggregation dimensions, expected metric type, owner, response, runbook, and what zero, absence and delayed data mean. Compare [assets/alert-contract.md](assets/alert-contract.md) with the project's contract before adapting it; it is a review outline, never a blind overwrite. Read [references/postgres-signals.md](references/postgres-signals.md) when collecting or alerting on PostgreSQL health, including the folded postgres-monitoring and postgres-observability jobs.

Use the `slo-error-budgets` skill, when installed, for SLI eligibility, target approval and budget policy. Use the `opentelemetry-instrumentation` skill, when installed, when application counters or trace instrumentation must change. Read a named skill's `SKILL.md` before relying on it; if an optional skill is unavailable, state the missing method and its effect on the claim. This skill owns rule semantics and routing; incident coordination, host-check installation and deployment readiness remain their existing owners.

Done when every alert has an observable trigger, accountable receiver and recovery condition, and every recording rule has a unit and stable dimensions.

## Implement the contract

- Apply `rate` or `increase` to each counter before aggregating; summing counters first hides independent resets.
- Align numerator and denominator by population, time window and labels; keep a missing error series distinct from a measured zero unless the exporter contract guarantees that equivalence.
- For classic histograms, aggregate bucket rates while retaining `le` before quantile calculation; use threshold bucket fractions for a latency SLI. Verify native histogram semantics against the deployed version. Never average instance percentiles.
- Keep bounded service, environment and route dimensions. Remove user IDs, raw URLs, query text, credentials and other unbounded or private labels before export.
- Page for urgent actionable symptoms; put causes and nonurgent risk into tickets unless the owner establishes an immediate response need. Give every alert `severity`, a routing owner label and `runbook_url`.
- Choose `for:` and recovery behavior from scrape delay, detection budget and flapping evidence. Include pending, firing and resolved assertions; a long hold can hide a short burn.
- Keep a receiving default route. Test specific routes, fallback and `continue` fan-out. Scope inhibition with identity labels that exist on both alerts so missing labels cannot suppress unrelated services.

Done when expressions, holds and labels implement the recorded signal contract without silently treating missing telemetry as health.

## Prove the rules

Use the repository's real render path first when a generator or operator CRD owns the rules; validate the rendered output consumed by Prometheus. Run the installed tools' help before relying on version-sensitive flags:

```sh
promtool check rules path/to/rendered-rules.yml
promtool check config path/to/prometheus.yml
promtool test rules path/to/rule-tests.yml
amtool check-config path/to/alertmanager.yml
amtool config routes test --config.file=path/to/alertmanager.yml --verify.receivers=expected-receiver service=example severity=page
```

Compare [assets/pint.hcl](assets/pint.hcl) with the project's existing policy when enforcing runbook, severity and owner labels. The starter was checked with its recorded pint version; verify the installed schema before use. Run the project's pinned pint with `pint -n --offline -c path/to/pint.hcl lint path/to/rendered-rules.yml`, or use the existing equivalent gate. Where that policy is absent, check every alert's rendered labels and annotations in native tests and the review inventory; a syntax pass does not enforce them. Keep native diagnostics in a protected local report when expressions or configuration contain private values. Let pint and promtool parse YAML; the skill ships no YAML reader. Maintain an explicit alert inventory with at least one firing and one quiet case per alert, and reject stale test names: an unknown alert with an empty expectation can pass vacuously. Native syntax and label checks alone do not prove coverage.

Build fixtures for healthy, threshold boundary, pending, sustained failure, recovery, missing/stale series, independent counter resets, sparse events and telemetry failure. For histograms add unequal instance traffic and a known threshold fraction; for routing add a receiver mismatch that must fail. Make one relevant broken expression fail the same behavioral test, then restore it and repeat the pass. Offline route tests establish receiver selection only; inhibition, silence timing, grouping and actual delivery require an authorized isolated Alertmanager with an inert local receiver, followed by the scoped notification path if requested. Keep collector replay separate from expression tests; synthetic metrics cannot prove SQL privileges or actual collection.

Prepare exact config changes and evidence before a reload or notification test. Production reloads, external notifications, traffic changes and credential rotation require explicit authorization for that scope; existing authorization persists. Immediately before a mutation verify account, project, region, cluster and receiver identities, or state which are inapplicable for a local target. An automated rehearsal must name an explicitly disposable target and refuse any other destination.

Done when native tests pass for the intended states and routing, the wrong-behavior test fails, and every unavailable collector, inhibition or delivery check is named separately. Return rule/config hashes, tool versions, selected tests, receiver expectations, actual notification evidence if run, and remaining limits.
