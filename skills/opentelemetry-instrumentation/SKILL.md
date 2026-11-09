---
name: opentelemetry-instrumentation
description: "Add or repair telemetry in application code: service spans, correlated JSON logs, bounded metric labels, queue context, and security events. Use for missing traces, broken parentage, secret-bearing output, or diagnostic gaps. Collector pipelines, dashboards, and alert rules are separate jobs."
license: MIT
compatibility: Python 3.12 or later for the read-only export checker.
---

# OpenTelemetry instrumentation

Instrument the questions an operator must answer, then inspect a synthetic journey from application source to collector output.

## Choose signals and verify support

Name the diagnostic question, operation, expected span or event, metric, and failure case. Cover inbound HTTP, outbound calls, database acquisition and execution, publication, queue waiting, and worker execution where present. Measure rate, errors, and duration, plus in-flight work and pool or queue saturation when they answer the question. Keep business completion distinct from transport acceptance.

Read current [language and signal status](https://opentelemetry.io/docs/languages/) and the installed SDK and instrumentation documentation. Record SDK, semantic-convention, and exporter versions in the project's evidence. Verify initialization order and Node ESM loader support before importing instrumented libraries. Use the repository's existing instrumentation rather than double-instrumenting calls.

Flush and shut down telemetry providers after accepted work drains and before process exit. Verify startup and final-request signals on the export; initialization and flush calls alone do not prove they arrived.

## Keep identity useful and bounded

Set service identity and release attributes on resources. Use route templates for HTTP server span names: `{method} {http.route}` when the framework has a matched route. Map an unknown method according to the selected conventions. An unmatched route needs a bounded fallback; a raw path never substitutes for an unavailable template. Check HTTP error/status behavior against the selected semantic conventions, including client cancellation.

Use finite metric attribute sets. User IDs, request IDs, message IDs, full URLs, SQL text, and free-form error messages do not belong in metric dimensions. Redact credentials, cookies, sensitive bodies, query values, and personal data before export. Test resource attributes, span events, links, logs, and exemplars as well as ordinary span attributes.

Emit structured JSON logs with stable event name, outcome, service identity, and trace/span IDs where a span exists. Use pseudonymous scoped identifiers only when the event contract requires them. Read [references/security-event-contracts.md](references/security-event-contracts.md) when a feature or control needs security telemetry. Sampling of diagnostic traces is not an audit retention policy.

## Carry context across real boundaries

Inject and extract the selected propagation format through outbound clients and message metadata. Treat incoming context and baggage as untrusted data: validate size and syntax, constrain propagated baggage, and keep secrets out. Use a parent or span link according to the actual relation; batch or fan-out consumption can require links rather than one invented parent. Keep event identity for deduplication separate from trace identity. Test two overlapping journeys to expose context leakage between requests.

Read [references/export-checks.md](references/export-checks.md) when collecting or checking a synthetic export. Compare [assets/telemetry-policy.json](assets/telemetry-policy.json) with the service's intended signal contract, then run:

```sh
python3 <skill-dir>/scripts/check-otlp-export.py --policy path/to/policy.json path/to/export.jsonl
```

Use an owned local collector with an installed, supported file exporter. Capture an unsampled complete synthetic journey in OTLP JSON, including spans, logs, and metrics. The checker verifies expected signal presence, allowlisted names and metric values, required attributes, correlation, declared queue edges, redaction canaries, and fixture series counts. Its policy is the application's bounded fixture contract, not a universal implementation of every semantic convention. Review conditionally required attributes against the live conventions.

Compare [assets/collector-file.yaml](assets/collector-file.yaml) only when a local collector fixture is missing; verify its components against the installed distribution before running it. The checker emits JSON counts and codes on stdout, safe diagnostics on stderr, and exits 0 pass, 1 findings, 2 invalid input.

Collector routing, batching, sampling pipelines, backends, dashboards, and alerts belong to operations owners. Hand over the emitted signal contract and source-to-collector evidence without naming an unshipped capability.

## Prove the observed journey

Exercise success, dependency failure, cancellation, overload, and queue redelivery where applicable. For security events, exercise allow, deny, and event absence. Remove a required signal, insert a synthetic secret, add an unbounded label, and break a queue edge; the check must reject each mutation. Run the unmodified fixture again and retain the same successful result. Use synthetic payloads on owned targets; never capture production credentials to test redaction.

Done when the emitted journey answers the stated diagnostic questions, context relationships resolve, required security events survive the export path, and privacy/cardinality mutations fail. Report the versions, capture command, checker policy, results, and the signal paths or production properties that remain untested.
