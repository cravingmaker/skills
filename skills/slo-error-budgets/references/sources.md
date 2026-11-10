# Sources

Read this when choosing the project's generator or verifying current input/output formats. The instructions and calculator are original; Google SRE material is cited for concepts and is not copied. Primary links checked on 2026-11-10; verify deployed versions at use time.

| Primary source | Use |
| --- | --- |
| [Implementing SLOs](https://sre.google/workbook/implementing-slos/) | Agree user-visible events, ownership and policy |
| [Alerting on SLOs](https://sre.google/workbook/alerting-on-slos/) | Relate permitted spend to burn and confirmation windows; assess sparse services |
| [Prometheus rule tests](https://prometheus.io/docs/prometheus/latest/configuration/unit_testing_rules/) | Verify the rendered alert behavior with independent series |
| [Sloth](https://sloth.dev/) | Check the installed generator's schema and generated rules |
| [Pyrra](https://github.com/prometheus-community/pyrra) | Check the installed generator's schema and rule behavior |
| [OpenSLO](https://openslo.com/) | Check intent schema and the selected adapter's supported version |
