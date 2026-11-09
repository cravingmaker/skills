# Security event contracts

Read this when adding a security control or feature whose actions must remain observable. Define the event with the control owner; this reference owns emission requirements, not detection rules or incident response.

For each event, record:

| Field | Decision |
| --- | --- |
| Trigger | Exact allow, deny, administrative change, or failed-control condition |
| Identity | Stable event name and version, service, safe correlation ID, and trace/span IDs where available |
| Actor | A scoped pseudonymous actor and tenant identity, or a documented anonymous/system actor |
| Action and target | The attempted operation and minimized target type/reference |
| Result | Outcome, bounded reason code, and whether the business effect committed |
| Time | Event time and collection time, with the ordering or clock assumptions |
| Access | Readers, writers, and protection against tampering or cross-tenant disclosure |
| Retention | Owner-approved retention, deletion, legal hold, and access requirements |
| Failure | What happens when emission or export fails; required audit durability is explicit |

Reject raw tokens, passwords, session cookies, sensitive request bodies, and unnecessary personal data. Keep attacker-controlled text bounded and safely encoded to prevent log injection. Do not put actor, target, or correlation IDs in metric labels. Separate a diagnostic sampled log from a durable audit requirement. Where business success requires a durable audit record, use a transactional record or outbox and prove the boundary; exporter best effort cannot supply that guarantee. Read the `async-messaging` skill when installed for that durable path.

## Named adapter fixtures

- **access-allow.** A synthetic actor performs an allowed operation; the event identifies action, target type, and allowed outcome without credentials.
- **access-deny.** A different tenant or denied actor attempts the same operation; the denial emits its own bounded reason and no protected payload.
- **event-absence.** Remove the deny event from an otherwise valid capture; the checker fails required outcome coverage.
- **event-redaction.** Place a synthetic credential canary in a nested event attribute or body; the checker fails without printing it.
- **event-export-failure.** Interrupt the collector, then restore it; observe the declared buffering, loss, or durable recovery policy.

Map the application's event fields into the exported log record. The checker accepts native `eventName` or the fixture's `event.name` attribute; when both exist, they must agree. Require allow and deny coverage in the checker policy; a trace's presence alone is insufficient. The export-failure case must exercise the real SDK and collector, not only JSON fixtures.

Sources: [OWASP logging guidance](https://cheatsheetseries.owasp.org/cheatsheets/Logging_Cheat_Sheet.html) and [OpenTelemetry logs](https://opentelemetry.io/docs/concepts/signals/logs/). Paraphrase their guidance; verify applicable organizational and jurisdictional retention rules with the responsible owner.
