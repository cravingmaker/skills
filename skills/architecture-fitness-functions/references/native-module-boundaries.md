# Native module boundaries

Read this when enforcing Android, Kotlin, JVM, or Swift module boundaries or extracting an agreed native module.

## Start with the agreed graph

An extraction needs a reason supported by evidence: ownership, independent tests, a measured build cost, or a dependency other modules must not reach. The `codebase-design` skill owns the module seam when that design is still open. Record the current and intended dependency graph, the public interface, affected consumers, and the temporary compatibility path.

Make extraction incremental. Each slice builds, preserves consumer behavior, enforces its intended graph, and names its rollback or forward repair. Give temporary adapters an owner and removal condition.

## Prefer compiler boundaries

- Gradle `implementation` keeps a dependency off a consumer's compile classpath; `api` exposes it. This is not runtime authorization. Kotlin `internal` limits declarations to their compilation module; inspect friend-module and test configuration before claiming isolation.
- Swift `internal` limits declarations to their module. Separate package targets are modules. `package` shares declarations with modules in the same package; it does not hide them from sibling targets. Use the actual compiler-supported visibility and a normal consumer import to test privacy.
- A forbidden module dependency should be absent from the declared graph, with a check that rejects adding it. Visibility alone does not prevent every unwanted public dependency.

## Use existing architecture checks

Use the repository's ArchUnit, Konsist, Android Lint, detekt, or equivalent rule when it covers the boundary. Verify imported classes or files are non-empty and contain the intended forbidden edge. Inspect the selected Gradle configuration or Swift target graph rather than inferring dependencies from directories. Read installed tool help and official documentation before choosing rule syntax.

## Prove each rule

1. A normal consumer uses the public interface and builds.
2. A disposable consumer reaches the forbidden implementation or adds the forbidden module dependency and fails for the intended rule.
3. Restore the allowed path, reapply the actual setup, and repeat both results. Record clean-build results separately from cached runs.

Keep privileged test imports such as Swift `@testable` separate from ordinary consumer proof. An unavailable native toolchain leaves this probe unrun; a TypeScript graph test cannot establish native visibility.

Primary sources: [Swift access control](https://docs.swift.org/swift-book/documentation/the-swift-programming-language/accesscontrol/), [Swift package targets](https://docs.swift.org/latest/documentation/packagemanagerdocs/introducingpackages/), [Gradle dependency configurations](https://docs.gradle.org/current/userguide/dependency_configurations.html), and [Kotlin visibility](https://kotlinlang.org/docs/visibility-modifiers.html). These interfaces are paraphrased; no source text is copied.
