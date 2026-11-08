# Runtime telemetry

Read this when an infrastructure condition, timeout, retry, rate limit, or threshold may have motivated the target. Datadog is an example; use current supported telemetry tools.

## Search the relevant service and period

1. Identify the owning service and the environment relevant to the change.
2. Inspect existing dashboards, monitors, and their queries for the target condition.
3. Check metric metadata, units, tags, and time-series context.
4. Narrow logs by service, condition, error string, and time. Prefer patterns or aggregates over raw dumps.
5. Follow relevant trace IDs or incidents to understand the failing path and the recorded response.

A monitor threshold or dashboard shows what someone measured or alerted on. It does not by itself prove why this line of code exists. A spike before a change and improvement afterward is correlation until linked evidence supports causation.

## Preserve limits

Check retention, renamed metrics, sampling, environment, and concurrent changes. Missing old telemetry is a gap, not proof that the condition never happened.

Return the item type, name, identifier or URL, owner/date where available, exact condition and units, bounded observations, and relevance to the target. Keep sensitive payloads and unrelated records out of the answer.

An incident statement explicitly tying the defense to a failure can be direct evidence of intent. Runtime data alone is usually contextual or indirect evidence.
