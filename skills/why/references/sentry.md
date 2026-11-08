# Error history

Read this when a specific exception, guard, retry, or corrective path needs historical context. Sentry is an example; use supported error-history reads in the actual environment.

Identify the relevant organization, project, and environment from available metadata without dumping configuration. Search real exception classes, symbols, error strings, and target file paths.

For relevant issues, inspect first/last-seen times, affected releases, event counts and sampling, then a representative event. Check whether its stack and relevant breadcrumbs actually pass through the target. Compare releases with the change timeline.

Return issue ID and URL, project, period, releases, compact counts, a minimal relevant stack excerpt, and any author or resolution notes. Preserve evidence limits such as retention, sparse sampling, and inaccessible events.

AI-generated root-cause summaries are hypotheses. Original events, traces, and attributable notes are the primary evidence. A post-change drop in errors alone does not prove either intent or causal success.
