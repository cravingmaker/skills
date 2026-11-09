# Sources

Read this when selecting installed runner APIs, capability checks or report export behavior. Instructions and checker are original; no source code or text is copied.

- [Testcontainers Node wait strategies](https://node.testcontainers.org/features/wait-strategies/): startup signals and explicit readiness conditions.
- [node-postgres transactions](https://node-postgres.com/features/transactions): real commit and client ownership.
- [SQLx test attribute](https://docs.rs/sqlx/latest/sqlx/attr.test.html): database fixtures and failed-test cleanup behavior; use locked-version docs.
- [Vitest test context](https://vitest.dev/guide/test-context.html), [requests](https://vitest.dev/guide/mocking/requests) and [migration guide](https://vitest.dev/guide/migration.html): runner fixtures, interception and version-specific behavior.
- [Vitest type testing](https://vitest.dev/guide/testing-types): explicit compiler checks and their distinction from runtime test execution.
- [MSW documentation](https://mswjs.io/docs/): the installed interception lifecycle and unexpected-request policy.
- [Swift Testing](https://developer.apple.com/documentation/testing) and [XCTest](https://developer.apple.com/documentation/xctest): installed Apple runtime and runner capabilities.
- [Android local tests](https://developer.android.com/training/testing/local-tests) and [instrumented tests](https://developer.android.com/training/testing/instrumented-tests): host versus platform-runtime boundaries.
- [Room database tests](https://developer.android.com/training/data-storage/room/testing-db): real in-memory framework fixtures and separate migration evidence.
- [Kotlin coroutine tests](https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-test/): controlled scheduling and cleanup at the installed library version.
