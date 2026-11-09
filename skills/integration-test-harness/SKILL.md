---
name: integration-test-harness
description: Build or audit isolated tests when real database, cache, broker, storage or native runtime semantics matter. Use for commits, provider transports, Vitest/MSW integration or reviewed legacy fixtures; prove capability readiness, independent oracles, selected execution and interruption cleanup.
---

# Integration test harness

Exercise the real boundary behind the claim, with an independent oracle and fixtures that the run owns and cleans up.

This skill supplies dependency and runtime test methods consumed by a project's verification driver. It does not create another planning or verification controller. Use the `tdd` skill when the task needs the general failing-test, implementation and refactor loop. Use the `create-verification-skill` skill when asked to package a missing repeatable project driver, and the `project-guardrails` skill when the gap is CI enforcement. Read any named skill before relying on it.

## Bind the claim to the real capability

State the behavior and the boundary it depends on: database constraints, commit visibility, isolation, provider transport, filesystem persistence, native clock or framework lifecycle. Inventory the project's runner, locked dependencies, service setup and existing fixtures before adding tooling. List which claims a fake can support and which require the real dependency. A mocked repository or SQLite substitute cannot establish PostgreSQL semantics. A container proves its configured PostgreSQL behavior, not a provider's HTTP or pooler path.

For Redis, probe the expiry or script behavior being claimed; for a broker, publish and consume through the required acknowledgement path; for storage, exercise the relevant persistence or upload operation. A generic ping cannot replace that capability.

Match relevant versions, extensions, collation, timezone, permissions and driver settings to the deployment. Verify readiness through an actual connection and the required capability, such as a constraint violation, a supported extension query or a persistence round trip. A listening port or healthy container alone is not that proof. Treat missing local tools as an explicit unavailable check; a required CI integration lane must fail rather than turn an unavailable dependency into a green skip.

Read [references/postgres-fixtures.md](references/postgres-fixtures.md) when the claim depends on PostgreSQL, migrations or commit visibility. Read [references/native-framework-tests.md](references/native-framework-tests.md) when Swift, Kotlin, a clock, a store or a platform framework supplies the behavior. Read [references/vitest-and-msw.md](references/vitest-and-msw.md) when Vitest, fake timers or request interception form the adapter. Read [references/legacy-characterization.md](references/legacy-characterization.md) when pinning reviewed current behavior before a refactor. Read [references/sources.md](references/sources.md) before relying on version-specific runner, container or platform behavior.

Done when every claim maps to an actual capability probe and its relevant environment settings.

## Own and isolate the fixtures

Use an explicit disposable target and synthetic data, scoped by run, worker and test. Verify the destination identity before any write; an ambient URL or a database name containing "test" does not establish authority. Keep credentials out of printed commands, connection errors, captures and test artifacts. Destructive operations on existing data require explicit user confirmation. Production branches can contain private data; use schema-only or synthetic fixtures.

Use the runner's resource fixture or existing container/database factory so setup failure still registers cleanup. Clean up open transactions, checked-out clients, timers, sockets, processes and only the run's created resources. Exercise success, assertion failure, setup failure and interruption. After a hard kill that bypasses hooks, an owner-scoped reaper must find resources by run identity; record what requires that reaper. Do not remove a shared database or another run's resources to make a suite pass.

Done when parallel and shuffled runs cannot see each other's state and an interrupted run leaves no unowned resource.

## Build a falsifiable oracle

Write expected rows, bytes, state transitions or error classes independently of the production calculation. Use small hand-derived examples where each relevant null, precision, ordering or cross-tenant case changes the expected result. Commit writes that the claim says are durable, then observe them through a separate connection or newly opened store. A rollback-per-test wrapper can hide commit, after-commit callbacks, deferred constraints and multi-connection behavior.

For a regression, run the broken implementation or remove the actual enforcement and show that the relevant assertion fails. Restore it and rerun the same scenario. A fixture that merely causes an unrelated syntax or setup error does not demonstrate sensitivity. Keep business oracle logic out of a shared helper that calls the same production function under test.

Use the `postgres-concurrency-control` skill for a two-connection race, the `postgres-connection-pooling` skill for a transport contract, and the `postgres-query-performance` skill for plan evidence. If the proof depends on external effects, test the durable boundary and its recovery path with an authorized sandbox or a contract-faithful controlled service.

Done when a meaningful wrong behavior fails, the repaired behavior passes, and the durable result has an independent observation.

## Execute and verify selection

Run the actual focused command from a fresh fixture, then the justified parallel or shuffled cases. Bind results to the source revision or content hash, build, runner/runtime versions, selected tests, target capability and fixture seed. Capture the process exit and report selection; an empty suite, all-skipped run or stale result file cannot pass. Use a fresh output directory so yesterday's report cannot survive a failed runner invocation.

When the runner produces JUnit XML, use [scripts/check-results.py](scripts/check-results.py) with an independently declared expected selection. For native result bundles or another report format, use the runner's supported exporter or validate its native result; retain the raw result and document any conversion. Do not fabricate XML to turn an unavailable runtime into evidence.

```sh
python3 scripts/check-results.py results.xml --expected-file expected-cases.json
```

Read [references/result-contract.md](references/result-contract.md) when choosing IDs, combining reports or interpreting failures. The helper needs Python 3.12+ and the standard library, and reads explicit local files only. It emits JSON counts on stdout and diagnostics on stderr; exits are 0 passing nonempty selection, 1 failed or incomplete results, 2 malformed input or usage. `--help` exits 0 without inspecting files or writing anything. It checks results and selection, not whether the assertions establish the claimed behavior.

Done when the fresh runner exit succeeds, every expected case passes, interruption cleanup is checked, and the retained evidence identifies what actually ran.

## Return the result

Report the changed claim, real boundary, independent oracle, wrong-behavior failure, repaired result, target capability and cleanup evidence. Name the executed command and nonempty selection, and label local, CI, provider and native-device results separately. List unavailable checks without converting them into passes; paired skill adoption runs are separate from product test results.
