# Result contract

Read this when validating JUnit output or adapting another runner report.

Native status attributes such as `notrun` and `suppressed` count as skipped even without a skipped element. An unknown status requires an explicit adapter normalization and exits 2; the checker does not assume it passed.

Create an expected-case JSON array before running tests, for example `["stock::atomic_increment", "stock::write_skew"]`. Each ID is the exact `classname` plus `::` plus `name` from a JUnit testcase. For a runner without class names, the ID begins with `::`. Use stable unique names including parameter identities; retries or shards need a normalized final report rather than duplicate successful-looking IDs.

Pass every relevant report to `check-results.py` once. It counts testcase elements, rejects duplicate IDs across reports, checks any declared suite counts against actual nested cases, and checks that every expected case passed. Zero cases, all-skipped cases, failures, errors, missing expected cases and duplicate results exit 1. Malformed XML/JSON, DTD/entity declarations, invalid declared counts and an empty expected selection exit 2. Failed or skipped cases outside the expected subset still fail the run; a subset cannot hide a failed suite.

The helper prints counts and stable finding names, never testcase names, failure bodies, system output or raw parser errors. Its input reports can still contain secrets; retain them privately and redact at collection. The expected selection and fresh report locators belong beside the source/build identity and actual runner exit status.

Some node:test name filters report an unselected file as a passing file-level case. The independent expected IDs must name the behavior cases, so that file-level placeholder cannot satisfy the selection.

Use a new report destination per run and fail the shell step if the runner fails before invoking the result checker. A valid old report can pass this parser, so the caller must bind creation to the current run. For a native result bundle, use the platform's supported query/export command and inspect its schema and exit semantics at the installed version. The parser does not judge independent oracles, dependency readiness or cleanup; retain actual runtime evidence for those claims.
