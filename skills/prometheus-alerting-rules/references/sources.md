# Sources

Read this when checking deployed-tool syntax or signal semantics; resolve the target's actual versions and use their matching documentation. These links support original instructions; no third-party text, rule configuration or code is retained. Checked on 2026-11-10; this date is a drafting receipt, not a promise of current feature support.

| Primary source | Use |
| --- | --- |
| [Prometheus rule tests](https://prometheus.io/docs/prometheus/latest/configuration/unit_testing_rules/) | Native synthetic series, missing/stale markers and expected alerts/expressions |
| [PromQL functions](https://prometheus.io/docs/prometheus/latest/querying/functions/) | Counter resets, rates, absence and histogram behavior |
| [Histograms and summaries](https://prometheus.io/docs/practices/histograms/) | Aggregate bucket semantics and quantile limits |
| [Alertmanager configuration](https://prometheus.io/docs/alerting/latest/configuration/) | Route inheritance, matchers, inhibition and receiver configuration |
| [Alertmanager repository](https://github.com/prometheus/alertmanager) | Installed-version amtool route verification and release checksums |
| [pint annotation checks](https://cloudflare.github.io/pint/checks/alerts/annotation.html) and [label checks](https://cloudflare.github.io/pint/checks/rule/label.html) | Native YAML policy; the starter was checked with pint 0.89.4 on 2026-11-10; verify installed syntax |
| [PostgreSQL statistics](https://www.postgresql.org/docs/current/monitoring-stats.html) | Use installed-major definitions for units, visibility, snapshots and resets |
| [Neon documentation](https://neon.com/docs/) | Verify supported collectors, metrics and suspend/restart behavior live |
