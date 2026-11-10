# Examples

Run matched final-skill and no-skill cases when authorized. Synthetic JSON fixtures prove checker behavior; an actual SDK/collector journey remains separate evidence.

## Activation

- "Our worker trace is detached from the request that published its message." Expect: actual propagation and parent/link semantics are traced across the queue.
- "Add traces, JSON logs, and useful RED metrics to this service." Expect: bounded names and labels answer stated diagnostic questions and a source-to-collector fixture verifies them.
- "This authorization control needs security events without leaking credentials." Expect: the security event reference supplies actor/action/outcome, absence, redaction, access, and retention requirements.

## Near miss

- "Configure collector routing and tail sampling." Expect: a collector pipeline operations job; this skill may supply an emitted signal contract but does not own the pipeline.
- "Build dashboards and Prometheus alert rules." Expect: monitoring consumers own those outputs.
- "Stop a Node request from leaving unhandled background promises." Expect: the `typescript-node-services` skill owns runtime work supervision.
- "Add a timeout to the tax API call." Expect: the `service-resilience` skill owns dependency time and work.
- "Find out why this endpoint is slow." Expect: the `diagnosing-bugs` skill owns diagnosis; existing telemetry is read before a change to instrumentation is proposed.

## Outcome

- "Reject bad telemetry without printing the secret." Fixture: `tests/opentelemetry-instrumentation/fixtures/complete.jsonl` and `assets/telemetry-policy.json`. Mutate a nested log body to the policy canary, add a per-request metric attribute, and replace the route span with a raw path. Expect: each independent mutation fails with a location/code and no canary value in output.
- "Verify queue context and security event absence." Fixture: the same complete unsampled capture with a producer and linked worker on different traces plus allow/deny log events. Expect: the original passes; removing the worker link or deny event fails; parent linkage also passes when the explicit policy and trace relation change together.
- "Accept native log event names." Fixture: move each `event.name` attribute in the complete capture to top-level `eventName`. Expect: the capture passes; a conflicting legacy attribute fails without printing its value.
- "Prove instrumentation reaches a collector." Fixture: an owned local collector with its installed supported file exporter and a synthetic HTTP-to-queue service with two overlapping requests. Expect: actual SDK output has separate request contexts, promised metrics and security events, no canaries, and documented behavior when export is interrupted; hand-authored JSON alone cannot satisfy this outcome.
- "Check a startup log outside a span." Fixture: an OTLP log with service resource and event name but no trace/span IDs, and a log-only policy with `require_span_context: false`. Expect: pass; the same missing context fails when that option is omitted. A supplied malformed ID or unresolved trace still fails.
