# Alert contract

Compare this outline with the project's existing format and adapt only the fields the work needs. All thresholds and hold durations come from the owner and measured traffic; example tests are synthetic, never a production policy.

| Field | Recorded decision or evidence |
| --- | --- |
| Signal and population | Metric/exporter source, type, eligibility, unit, cluster/database/service scope |
| Identity | Stable bounded labels, expected-target source, owner and fallback receiver |
| Expression | Recording dependencies, numerator/denominator alignment, aggregation order |
| Timing | Scrape/evaluation intervals, detection budget, hold and recovery behavior |
| Missing data | Zero, NULL, stale, denied collection, target removal and telemetry outage |
| Response | Severity, urgency, action, runbook_url and recovery condition |
| Routing | Positive/negative label sets, default receiver, fan-out and inhibition identity |
| Evidence | Rendered hashes, native tool versions, selected cases, collector/delivery scope |

Require a runbook URL and routing owner on every alert, including telemetry-failure alerts. Keep private connection/configuration data outside the review artifact.
