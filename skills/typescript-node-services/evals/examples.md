# Examples

Run matched final-skill and no-skill cases when authorized. The smoke-helper fixtures use a real local Node runtime, not an assumed deployment image.

## Activation

- "The TypeScript tests pass but our built Node server cannot import its entry." Expect: package type/exports, compiler resolution and emitted imports are checked on the deployment runtime.
- "Build a Node TypeScript service that refuses invalid configuration before listening." Expect: configuration parsing precedes admission and missing/invalid key tests run separately from type checking.
- "Our Node service stalls on fan-out and loses work during cancellation." Expect: bounded admission, actual AbortSignal propagation, and owned lifecycle behavior are tested.

## Near miss

- "Upgrade TypeScript and typescript-eslint." Expect: the `toolchain-upgrade` skill owns compatibility and effective-rule changes.
- "Set up formatting, CI, and pre-commit checks for this repo." Expect: the `project-guardrails` skill owns general enforcement.
- "Build a browser-only React bundle." Expect: a frontend task; Node server runtime settings are not imposed.
- "Design REST endpoints for invoices." Expect: the `api-design` skill owns the operation contract.
- "Build a Tokio service for this API." Expect: the `rust-async-services` skill owns the Rust runtime.

## Outcome

- "Prove the built entry is what runs." Fixture: the offline copy/build/import and start fixtures in `tests/typescript-node-services/test_smoke.py`, then a disposable copy of the real service with the recorded deployment Node executable. Expect: an emitted entry imports or reaches application readiness and exits cleanly on SIGTERM; leaked handles and import errors fail.
- "Refuse an unsafe smoke target." Fixture: omit the disposable flag, pass a git-marked target, give a path outside the copy, or supply a mismatched runtime version. Expect: exit two before the build; no emitted file appears.
- "Prove invalid configuration and promise checks." Fixture: a server that listens only after parsing a required integer key, a missing key, an invalid synthetic value, and an unhandled request promise. Expect: startup failures name the key without its value, the readiness marker stays absent, and the repository's typed lint rejects the unhandled promise independently of tests and build.
- "Check invalid startup output safely." Fixture: one emitted entry exits two and names `FIXTURE_KEY`; another emits `FIXTURE_KEY: SYNTHETIC_ONLY_CANARY`; another accepts configuration and hangs. Expect: reject mode with that key and forbidden canary accepts only the first, times out and cleans up the hanging entry, and prints no child diagnostics.
