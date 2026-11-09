# Vitest and MSW adapters

Read this when a test uses Vitest, request interception or virtual time.

## Runner selection

Read the installed Vitest version and configuration before selecting projects, environments, fixtures or browser providers. Use existing locked versions; check current official migration notes when an upgrade is in scope. Bind the actual command and project filters to the result report, and prove every intended case ran. Keep assertions and promises awaited or returned so a test cannot finish before the failing operation.

Run the project's typecheck command separately from runtime tests. Check the installed runner's explicit typecheck configuration; green runtime cases alone do not establish type correctness.

Use per-test fixtures for stateful resources and reset handlers, timers, spies and globals during cleanup. Check isolation with parallel and shuffled execution, including a failure that interrupts normal cleanup. If fake timers are used, restore real timers and settle queued tasks before the next case. Keep real network/database readiness on real time; advancing virtual time does not start a real service. Use the runtime's supported clock APIs, including Temporal only when the installed runner/runtime actually supports the required interception.

## Request interception

For MSW, install handlers for the intended boundary and make unexpected requests fail using the installed API. Reset per-test overrides and close the interceptor at the owned fixture's end. Assert externally visible request and response behavior with independently chosen data. Do not let a production schema builder generate both the expected payload and the observed payload.

An intercepted response can test application decoding and handling of a provider contract. It does not establish real provider authentication, retries, network timing or database transaction semantics. Retain a real authorized sandbox or transport test where the claim requires it. Use synthetic authorization values, and prove that recorded failures redact them.

## Browser and coverage scope

If a claim needs a browser implementation of a web API, use the configured real browser provider and retain its result identity. A simulated DOM environment is a separate scope. Coverage is a floor for inspecting missing cases; a high percentage does not prove the oracle is independent or the boundary is real. For a meaningful regression, change the behavior under test and show its assertion fails, then restore it.
