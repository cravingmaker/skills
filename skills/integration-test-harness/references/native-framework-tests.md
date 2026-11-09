# Native framework tests

Read this when Swift or Kotlin behavior depends on a platform runtime, time or persistence.

## Preserve the runtime semantics

Use Swift Testing or XCTest and the Android test runner already used by the project. Choose the test runtime from the claimed capability: plain logic, real filesystem/store, framework runtime, simulator or device. An in-memory repository cannot prove that a native persistent store survives reopening. An in-memory Room, Core Data or SwiftData store can exercise the real framework for claims that do not require disk persistence or migration; declare that narrower capability. A plain JVM test cannot establish behavior that belongs to an Android system service. Inspect the installed SDK and runner documentation before choosing a framework API or test target.

## Time and scheduling

Inject a controllable clock or scheduler at the boundary the application already exposes. Await the observable event or drain the framework's supported scheduler; an arbitrary sleep proves no causal ordering. Test a deadline boundary just before and after expiry with independent expected results. Verify task cancellation releases observers, callbacks, work and open stores. Virtual time proves the scheduled logic; retain a real-runtime test when the claim concerns an actual timer or process boundary.

## Stores and framework fixtures

Allocate a new store URL, directory, database or sandbox identity per run/worker/test. Seed synthetic records, save through the real framework, release the writer, reopen independently and assert manually specified values. Test migration from a checked-in small old fixture and verify the new persisted state after reopen. Use platform cleanup hooks plus an owned-resource recovery path after a killed process.

Examples of meaningful failures are a dropped save, a removed transaction, a wrong timezone boundary or a discarded cancellation signal. A test of a fake store's own methods is evidence about that fake only. Retain the exact selected target, build identity, SDK/runtime, device or simulator, native result bundle and test counts. Use native report exporters for selection checks; validate that skipped or unselected tests are visible.

## Boundary

This adapter covers behavior and native-framework integration. Whole-app gesture journeys, install/upgrade flows and device-level lifecycle automation belong to the mobile journey test owner. The same independent oracle, nonempty selection and cleanup contract applies when that owner consumes this method.
