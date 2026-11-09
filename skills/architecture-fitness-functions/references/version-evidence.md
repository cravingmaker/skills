# Version evidence

Read this when checking the starter's recorded release or choosing a supported equivalent.

The starter is pinned to releases used for its local fixtures; it makes no claim about the latest release. Recheck the installed runtime, parser support, package release, lockfile, and official rules before using it in a project.

| Item | Recorded input | Primary source | Accessed |
| --- | --- | --- | --- |
| dependency-cruiser starter | 18.7.2 | [Package metadata](https://registry.npmjs.org/dependency-cruiser/18.7.2), [rule reference](https://github.com/sverweij/dependency-cruiser/blob/v18.7.2/doc/rules-reference.md) | 2026-11-10 |
| TypeScript parser for the fixture | 5.9.3; recheck compatibility in a real project | [Package metadata](https://registry.npmjs.org/typescript/5.9.3), [transpiler support](https://github.com/sverweij/dependency-cruiser/blob/v18.7.2/src/meta.cjs) | 2026-11-10 |
| Cargo metadata | Output format 1; opaque package IDs | [Cargo Book](https://doc.rust-lang.org/cargo/commands/cargo-metadata.html) | 2026-11-10 |
| JS Boundaries selection | Check installed rule and selector support | [Dependency rule](https://www.jsboundaries.dev/docs/rules/dependencies/) | 2026-11-10 |
| cargo-deny selection | Check installed bans and wrapper semantics | [Bans configuration](https://embarkstudios.github.io/cargo-deny/checks/bans/cfg.html) | 2026-11-10 |

The live parser check found that the starter's tested dependency-cruiser release does not load a TypeScript parser outside its declared supported range. A CLI success with an empty graph is insufficient. Keep the import-scan helper in the CI command and verify parser compatibility at use time.

These sources supply facts and interfaces; their code and prose are not copied. The separate uppercase SOURCES manifest records retained Matt Pocock material.
