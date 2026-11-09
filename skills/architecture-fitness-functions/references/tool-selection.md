# Tool selection and proof

Read this when choosing a boundary checker or making a legacy policy stricter.

| Boundary | Preferred enforcement | Required counterexample |
| --- | --- | --- |
| Package public surface | Explicit exports plus the project's import checker | A real consumer imports a non-exported subpath and fails |
| TypeScript source layers | Existing dependency-cruiser, JS Boundaries, or Nx policy | A resolved forbidden edge fails the intended rule |
| Rust internal surface | Module privacy and scoped visibility | A downstream fixture cannot access an internal symbol |
| Rust workspace direction | Resolved Cargo metadata and an explicit layer policy | A renamed or build/dev dependency cannot bypass the rule |
| Public API growth | Existing public API report or semver checker | An unintended public symbol appears in the diff or exceeds an agreed budget |
| Python data components | Existing import-linter or tach policy | A consumer imports writer internals and fails |
| JVM or Kotlin components | Existing ArchUnit or Konsist tests | A forbidden bytecode dependency fails the selected rule |

Use Nx only when the workspace already uses it. For JS Boundaries, verify classification, unknown-file coverage, rule names, and the installed release's selector schema before editing. For cargo-deny, verify the installed release's `bans` and `wrappers` semantics, including transitive paths. It is not a substitute for an explicit normal/build/dev workspace policy. No universal ESLint or cargo-deny starter is shipped here; use the project's tested native configuration.

Check package-manager and runtime compatibility against official release docs before adding a dependency. Pin any approved addition through the project's lockfile and policy. The method does not authorize an upgrade. Inspect all supported targets and feature sets; a single default metadata graph proves only that configuration.

Legacy baselines identify exact known edges with owners, reasons, and removal triggers. Use the tool's native baseline if it can reject new violations without accepting unrelated drift. Compare the baseline before and after, fail on growth, and remove entries whose violation disappeared. A wholesale regenerated baseline needs explicit review of every added exception.

Prove each changed rule by an allowed edge, a deliberate forbidden edge, restoration, and actual setup reapplication. Save the expected rule identifier and nonzero exit so parse failures cannot masquerade as enforcement. Keep fixtures isolated and clean up only owned temporary files.
