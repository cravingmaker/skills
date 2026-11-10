---
name: service-resilience
description: Bound dependency time and work in service code. Use when adding an outbound call, fixing retry storms or cascading failure, setting overload behavior, or preventing shutdown from losing work. Covers deadlines, retry ownership, bulkheads, and draining; platform scaling and SLO policy are separate.
license: MIT
compatibility: Python 3.12 or later for the read-only helpers.
---

# Service resilience

Make the service stop waiting and accepting work within a measured budget, then prove recovery under dependency faults.

## Set one budget

Trace the request or job through DNS, connection establishment, TLS, pool acquisition, request execution, and response reading. Set an end-to-end deadline and reserve time for local work and cleanup. Each hop uses remaining time, not a fresh copy of the original deadline. Use monotonic elapsed time locally; translate propagated deadlines with an explicit clock-skew and trust policy. Propagate cancellation into the actual client and check whether a timed-out write can still commit remotely.

Record the dependency, timeout scope, retry owner, eligible failures, maximum attempts including the first, delay cap, and concurrency limit. Include SDK and proxy retries in that inventory. Select timeouts from measured latency and the user-visible budget rather than remembered constants.

Compare [assets/retry-policy.json](assets/retry-policy.json) with the actual path, then run:

```sh
python3 <skill-dir>/scripts/retry-amplification.py path/to/retry-policy.json
```

The helper multiplies nested attempt counts and checks per-hop allocations. Each `max_backoff_ms` bounds one gap between attempts; the calculation includes `(attempts - 1)` such gaps, including a server-directed delay the caller elects to honor. It is not a simulator of parallel calls or a substitute for fault tests.

Use the asset's `layers` for nested retry owners, outermost first. Replace that field with `hops` for sequential dependency operations; their worst-case times and total leaf attempts add. Include caller work in `overhead_ms`. A parallel path needs its own workload model and fault test. The helper prints JSON on stdout and diagnostics on stderr; exits are 0 pass, 1 findings, 2 invalid input.

## Limit retry amplification

Assign retry ownership to one layer. Retry an eligible transient failure only when repeating the effect is safe and time plus retry tokens remain. For an uncertain external write, use the provider's idempotency key or reconciliation. Read the `idempotent-requests` skill when installed for request admission and external effects.

Use capped full-jitter backoff. Honor a valid `Retry-After` only when its delay and the next attempt fit; otherwise surface the documented failure or defer a durable job. Test delay-seconds and HTTP-date forms with a controlled clock, including invalid and past values. Bound retries across traffic with a token or ratio budget as well as per-operation attempt limits. Use the `async-messaging` skill when installed for durable redelivery and queue leases.

## Bound active and queued work

Put finite limits on active calls, queued work, body bytes, response bytes, and fan-out. Use backpressure and release permits on success, error, and cancellation. Reject overload before the queue consumes the deadline; use documented `503` and `Retry-After` behavior for HTTP service overload. Keep rate-limit semantics distinct from capacity rejection. A circuit breaker needs a demonstrated failure mode and tests for open, half-open, and recovered states.

Run `python3 <skill-dir>/scripts/find-unbounded-calls.py` on explicit source files to find calls that deserve inspection. It flags visible fetch calls without a signal, selected client constructors without a visible timeout, axios calls without a timeout or signal, and Promise or Rust iterator fan-out. It is a text heuristic: indirect options, shared clients, dynamic imports, and query wrappers need manual tracing. An empty result does not prove every call is bounded. It prints JSON on stdout, diagnostics on stderr; exits are 0 no candidates, 1 candidates, 2 invalid input. Use existing typed lint and compiler checks before adding another checker.

For Node cancellation and event-loop behavior, read the `typescript-node-services` skill when installed. For Rust task, lock, and blocking-work ownership, read the `rust-async-services` skill when installed. Those capabilities own language-specific configuration.

## Drain within a deadline

On termination, fail readiness, stop admission and queue claims, and drain owned in-flight work. Close idle connections, let accepted work commit or release its claim, then close dependency pools. Bound draining below the platform's termination allowance and define what happens to unfinished durable work. Make shutdown idempotent. Keep liveness independent of dependency health; readiness may reflect inability to serve the promised operation. Platform probe configuration, autoscaling, and SLO policy belong to their operations owners.

## Verify failure and recovery

Read [references/fault-tests.md](references/fault-tests.md) when implementing a dependency or shutdown change. Use fake clocks and deterministic random inputs to assert retry count, delay bounds, remaining deadline, and token exhaustion. Run an actual child service with a controlled slow or failing dependency to check cancellation and socket behavior. Send SIGTERM during accepted work and observe readiness, admission, durable effects, process exit, and recovery after restart. Run faults only on owned, authorized disposable targets and retain no credentials in output.

Done when overload has a finite response, dependency faults cannot exceed the stated work and time limits, and termination preserves the documented work contract. Report static candidates separately from executed faults, plus the observed bounds and any unavailable proof.
