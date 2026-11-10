# Examples

These are unrun paired-evaluation cases; calculator and native fixtures establish deterministic behavior only. Keep target approval and evaluation status explicit.

## Activation

- "Define an availability SLO for checkout and write the error-budget policy with me." Expect: bind eligible events, source, target/window, exclusions, traffic floor, no-data behavior and owner decisions before approved status.
- "Generate multiwindow burn alerts from this approved event-counter SLO." Expect: derive thresholds from supplied spend fractions and windows, generate native rules and test fast/slow/long-only behavior.
- "Our low-volume endpoint pages after one failure; review the burn-rate policy." Expect: calculate one-event impact at both traffic floors and propose an owner decision that preserves coverage.

## Near miss

- "The approved SLO is unchanged; fix an incorrect PromQL join and Alertmanager route." Expect: the `prometheus-alerting-rules` skill owns expression/routing repair.
- "Instrument a latency histogram in the API." Expect: the `opentelemetry-instrumentation` skill owns telemetry emission; no invented SLO target.
- "Apply retries and a drain deadline to this service." Expect: the `service-resilience` skill owns dependency bounds and shutdown behavior.
- "Build a dashboard for the approved SLO without changing its target or alerts." Expect: the existing dashboard owner handles presentation; no new reliability policy.
- "Run deploy-checklist for tonight's release." Expect: the existing readiness process applies the approved policy, without creating new objectives.
- "Use incident-response to coordinate on-call work." Expect: the existing incident process owns coordination; a budget policy is not incident command.

## Outcome

- "Check the approved burn math." Fixture: target 0.999, objective window 2592000 seconds; policies spend 0.02 over 3600 seconds, 0.05 over 21600 seconds and 0.1 over 259200 seconds with adequate event floors. Expect: burn thresholds 14.4, 6 and 1 and bad-fraction thresholds 0.0144, 0.006 and 0.001; changing the contract changes the calculation without a fixed table.
- "Reject unsafe sparse-window assumptions." Fixture: the first policy above has short_min_events of 1, then 0. Expect: calculator exit 1 with a single-event or empty-floor finding; rule generation emits nothing and exits 1; malformed/nonfinite targets exit 2 without echoing supplied values.
- "Test the generated confirmation behavior." Fixture: use the shipped synthetic contract and rule-tests.json. Bad/eligible counters increase 300/10000 per minute for 60 minutes and then stop adding bad events while eligible traffic continues. Expect: fast burn is absent at 70 minutes; changing the long/short join from and to or fails that same case, and restoring it passes.
- "Prove the slow, missing and reset branches." Fixture: 15 bad out of 10000 eligible per minute for 73 hours; separate zero/no-data/stale/sparse series; and a paired counter reset during a 200/10000-per-minute burn. Expect: slow ticket without either page, no burn alert for undefined reliability, a sustained post-reset burn still detected, and explicit separate telemetry coverage in the artifact.
