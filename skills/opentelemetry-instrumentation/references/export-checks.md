# Export checks

Read this when preparing the policy or interpreting the export checker. The input is OTLP JSON or newline-delimited OTLP JSON objects with `resourceSpans`, `resourceLogs`, or `resourceMetrics`. Human-readable debug exporter text and binary protobuf are different formats; configure or convert explicitly rather than silently skipping them.

Use the installed collector's file exporter documentation for its supported encoding. The checker accepts integer OTLP enum values and hexadecimal trace/span IDs; it normalizes ID case. It reads the usual scope containers, not legacy instrumentation-library containers. An unsupported shape fails instead of producing an empty successful scan.

## Policy

Compare `assets/telemetry-policy.json` with the application's actual instrumentation. Keep each expected span and log event name explicit. Each span rule lists required attributes. Each metric rule lists finite permitted values for every point attribute and a maximum series count for the synthetic fixture. Each log rule lists required attributes and value coverage, such as both authorization outcomes. Queue edges specify source name, destination name, attributes that must match, and `parent` or `link`.

A log rule requires span context by default. Set `require_span_context: false` only for an event whose contract permits logs outside an active span, such as startup. Such logs may omit both IDs; supplied IDs are still validated, and a trace-only log must resolve to an exported trace. Keep the default for request events that must detect lost correlation. The [log data model](https://opentelemetry.io/docs/specs/otel/logs/data-model/#trace-context-fields) makes both context fields optional.

For logs, the checker maps native `eventName` into its policy's `event.name` field and also accepts that attribute from older instrumentation. If both are present, they must agree. Use the selected SDK's emitted form; the [OpenTelemetry log data model](https://opentelemetry.io/docs/specs/otel/logs/data-model/) defines the native field.

Every target span must have its declared relation to an exported source. Match a safe event identity across a queue edge so a link to the wrong existing producer also fails; use an empty match list only when the declared relation needs no identity match. Ordinary parents and trace-correlated logs must resolve inside the capture. Run this check on a complete unsampled fixture; sampled or filtered production traces can legitimately lack ancestors. Multiple synthetic journeys test whether links accidentally connect unrelated work.

The checker scans nested output for forbidden attribute keys, configured synthetic canaries, and a small set of credential-shaped values. Findings contain code and location, never offending values or raw payloads. This is a redaction regression check, not a complete secret or personal-data detector. Add a safe canary for every sensitive input branch and inspect the intended minimization policy.

Metric allowlists and series limits prove the bounded fixture contract. They do not predict production cardinality from unseen values, resource multiplication, or multiple instances. Inspect production dimensions and resource counts with the operations owner before claiming a storage bound.

## Evidence

Keep the capture command, code revision, installed SDK and collector versions, enabled instrumentation, sampling mode, and policy with the result. Test actual SDK-to-collector output; generated fixture JSON proves the checker, not the SDK wiring. The offline tests in `tests/opentelemetry-instrumentation/` cover the checker with synthetic values.

Sources: [OTLP encoding](https://opentelemetry.io/docs/specs/otlp/), [HTTP spans](https://opentelemetry.io/docs/specs/semconv/http/http-spans/), [messaging conventions](https://opentelemetry.io/docs/specs/semconv/messaging/), and [context propagation](https://opentelemetry.io/docs/concepts/context-propagation/). Resolve the selected semantic-convention version and conditional attributes at use time.
