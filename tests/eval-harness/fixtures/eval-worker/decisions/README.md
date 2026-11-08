# Worker record and notes

For run-record requests, coordinator migration-02 has backend and frontend tasks described in contracts/status.json, one integration owner, two planned worker starts, no retries, one verification reserve, concurrency limit 2. No dispatch has happened and no live worker tools are available. Preserve intents separately from receipts; do not invent receipt/result. Existing notes are inputs, not a completed run.

For an architecture decision record, the accepted cache choice is a process-local TTL cache for the single-instance pilot; rejected Redis because operating overhead exceeds the pilot scope; revisit before three-instance deployment. Meeting note: Ada owns the local cache; Ben owns measuring hit rate; the team deferred multi-instance invalidation until deployment planning. Write a direct summary if only asked to summarize this note.

No commits or pushes are permitted, including in temporary repositories.
