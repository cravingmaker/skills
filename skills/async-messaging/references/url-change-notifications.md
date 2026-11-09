# URL change notifications

Read this when a committed public URL addition, update, or deletion must notify a search service. Use an outbox adapter with durable receipts; this reference adds no second scheduler or queue.

## Contract

Verify supported endpoints, ownership-key hosting and scope, request schema, batch limits, response meaning, and retry guidance against the [official IndexNow documentation](https://www.indexnow.org/documentation) at use time. Read the target provider's own documentation when its contract differs. Keep protocol limits in validated configuration rather than copying remembered numbers.

Enqueue from the authoritative content transaction or its durable change record. Include canonical URL, site scope, change identity, operation, content revision, and destination. Deduplicate a repeated change for one destination, while preserving a later real revision and a deletion. An unchanged re-save emits no new notification. Do not manufacture change times or notify URLs outside the owned, authorized site scope.

Build batches from eligible records within the verified host and ownership scope. Record destination, batch identity, scoped event IDs, attempt, response classification, and next action. Keep keys, private URLs, and bodies out of logs; use minimized receipt fields. The ownership file is intentionally public according to the protocol; it is not an application credential.

On a lost acknowledgement, resend with stable change identity and record that duplicate submission is possible. Retry eligible transient failures within the parent's time and attempt bounds; respect current server retry guidance. Permanent ownership or payload rejection stops that batch for repair. An accepted submission records notification receipt only. Index eligibility, crawling, and index inclusion remain separate observations.

## Named adapter fixtures

Use `assets/url-notification-cases.json` as the case inventory. Build the owned example URLs on a fake transport; do not contact a search provider from fixture tests. Combine it with the parent crash, duplicate, final-attempt, and stale-lease schedules.

- **Real changes.** Add, update, and delete revisions each create a durable notification; an unchanged save creates none.
- **Destination scope.** A repeated event for one destination deduplicates; another destination receives its own receipt.
- **Uncertain delivery.** The receiver records acceptance then drops the response; resumption retains identity and bounds attempts.
- **Permanent failure.** An ownership or payload rejection stays inspectable and does not advance to accepted.
- **Acceptance meaning.** A successful receipt leaves index status unknown.

Done when the tests compare committed change IDs with notification IDs and receipts, prove bounded recovery, and keep notification receipt separate from indexing.
