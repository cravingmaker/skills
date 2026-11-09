# Fault tests

Read this when proving a retry policy, bulkhead, cancellation path, or shutdown deadline.

| Fixture | Assertion |
| --- | --- |
| Instant retryable failure | Total attempts include the first call and stop at both attempt and token limits |
| Permanent or unsafe failure | No automatic retry; an uncertain external write enters reconciliation |
| Slow connection and body | Connection setup and response reading both consume the same remaining budget |
| Nested SDK retries | Captured downstream count matches the declared amplification; another retry owner fails the policy |
| Full-jitter extremes | Inject random values at both endpoints and a fake clock; no chosen delay exceeds its cap |
| Retry-After | Delta, date, invalid, past, and beyond-deadline cases produce the documented next action |
| Cancellation | Caller abort reaches the real transport; remote postconditions reveal whether a write still happened |
| Saturation | The active count and queue length never exceed their limits; rejected work starts no dependency call |
| Permit cleanup | Failure and cancellation release capacity; healthy calls succeed after the fault clears |
| Dependency outage | Liveness stays healthy; readiness follows the declared serving contract |
| SIGTERM while busy | Readiness fails, new work stops, accepted work drains within the deadline, and pools close last |
| SIGTERM past deadline | Remaining work follows the documented cancellation or durable recovery path; process exit is bounded |

Use synchronization barriers for process tests, not a sleep that merely hopes a request has started. Do not fake the transport when claiming a socket, connection pool, or response body is cancelled. Keep retry arithmetic separate from the application's scheduling tests. The calculator assumes each nested child's whole retry sequence fits within its parent's per-attempt timeout. Its output is an upper bound, not measured latency.

Sources: [Amazon Builders' Library](https://aws.amazon.com/builders-library/timeouts-retries-and-backoff-with-jitter/), [Google SRE on cascading failures](https://sre.google/sre-book/addressing-cascading-failures/), and [gRPC deadlines](https://grpc.io/docs/guides/deadlines/). Verify retry defaults, timeout coverage, cancellation APIs, and shutdown APIs against the installed client's and runtime's official documentation at use time.
