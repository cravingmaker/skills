# Analytics evidence

Read this when usage, experiments, data shape, billing volume, or the origin of a numeric threshold may explain the design. Databricks is an example; use the actual warehouse's supported read operations.

## Confirm the data before querying

Discover the relevant catalog, schema, tables, columns, and lineage. Company-specific table names and property conventions are not portable defaults. Confirm typed-model definitions, deduplication, refresh lag, and historical schema fit.

Use bounded read-only queries for the relevant period around the change. Prefer existing typed models when they represent that period and question correctly; use raw data only when needed and account for duplicates and refresh lag.

If the tool returns an asynchronous statement identifier, follow its supported result operation rather than executing the same expensive query again.

## Match the question

- **Usage.** Compare relevant event counts around the change, checking instrumentation changes before interpreting a ramp as a launch.
- **Threshold.** Inspect the relevant pre-change distribution, units, and extreme cases. A matching percentile is circumstantial until a decision record connects it to the constant.
- **Experiment.** Confirm flag keys, exposure, outcomes, and any recorded ship decision.
- **Migration or performance.** Use focused query-history and lineage evidence, with known retention and access scope.
- **Billing or volume.** Keep source units, aggregation grain, and the period exact.

An event's presence shows instrumentation, not why the code exists. Correlation with a ship date is context, not proof of causation. Current schemas may differ from those available when the target was written.

Return fully qualified table names, exact bounded query, period, compact numeric summaries with units, and the source locator. Record inaccessible notebooks, retention cliffs, model-creation dates, and unsearched data as limits. Do not dump raw user rows or silently launch a broader analysis.
