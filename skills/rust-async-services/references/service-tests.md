# Service tests

Read this when writing the async-behavior tests for an Axum service. Drive the real `Router` in process with `tower::ServiceExt::oneshot`, or a real listener on port 0 when the test needs a connection to drop. Use paused time for timer-only cases; real sockets need barriers and a bounded real-time watchdog. Each test must fail when its protection is removed; check that once.

| Test | Setup | Assert |
| --- | --- | --- |
| Middleware order | A handler that sleeps past the timeout layer. | The response has the documented timeout status and problem body; the tracing layer recorded the request (a test subscriber or exporter captured the span); authentication ran before the handler and after tracing. |
| Rejection mapping | Send malformed JSON and a body with an unknown field. | Both responses use the problem-details shape and content type; no default plain-text rejection leaks through. |
| Concurrency limit | Hold N requests open at the limit, send one more. | The extra request gets the overload status at once, not after a queue wait. |
| Client disconnect | Open a real connection, send a request whose handler pauses at a barrier between two writes, then drop the connection and release the barrier. | Record whether this stack actually drops the handler; an independent observer sees both writes or neither, and durable recovery settles uncertain effects. |
| `select!` cancellation | Race the operation against a shutdown or timeout branch that wins. | No message, byte, or permit is lost; the next iteration resumes the same work. |
| Blocking bound | Hold closure A at a barrier, cancel its awaiter, then submit closure B with one permit available in total. | B waits until A releases the permit held inside its closure; cleanup releases every barrier. |
| Shutdown drain | Hold one request open, trigger the shutdown signal, then release the request. | The held request completes; a new connection is refused; the serve future returns before the drain deadline; background tasks observed the cancellation token. |
| Shutdown deadline | Hold a request open past the drain deadline. | Shutdown returns at the deadline and logs the abandoned request. |

## Test seams

- Build the app with a function such as `app(state) -> Router`, so tests construct it with fakes.
- Pass the shutdown future in, so a test triggers it with a `oneshot` sender or a cancellation token instead of a real signal.
- Use real PostgreSQL for the disconnect test; a mock cannot show rollback on drop. Read the `integration-test-harness` skill when installed for the database fixture.
