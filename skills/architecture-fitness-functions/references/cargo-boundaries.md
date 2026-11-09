# Cargo boundary policy

Read this when enforcing direction between workspace crates.

Generate full resolved metadata using `cargo metadata --format-version 1 --locked`. Use the project's target and feature flags and capture them with the artifact. Avoid `--no-deps`: a missing resolve graph is not a passing scan. If lock generation or dependency fetching is outside scope, use an existing complete captured graph and state its revision and limits.

The policy has two objects. `layers` maps a layer to exact workspace package names. `allow` maps each of `normal`, `build`, and `dev` to permitted destination layers for every source layer. An empty destination list means no workspace dependencies of that kind. Same-layer edges require that layer in the list too. Compare the asset with the real graph; never overwrite policy blindly.

The helper reads resolved dependency IDs rather than manifest aliases. A renamed crate still belongs to its actual package and layer. All reported target-specific edges count; the helper does not evaluate configuration expressions. Run the supported target and feature matrix to establish broader coverage. External dependencies are counted but remain outside this workspace-layer policy. This helper cannot prove a ban on an external crate or on a path through external crates. For such a rule, use an existing graph checker that can express that path and test a real forbidden path plus an allowed one. A clean workspace-layer result proves only its declared scope.

Every workspace member must have a package record, a resolved node, and exactly one layer. Unknown policy names and unclassified new crates fail. Duplicate keys, unknown dependency kinds, absent resolve data, and malformed records fail as invalid inputs. A graph with no workspace edges exits 1 because it cannot demonstrate this policy scans an edge.

Output is JSON with workspace package and edge counts, counts by dependency kind, external edges outside scope, and findings. Exit 0 means the covered edges pass, 1 means findings, and 2 means usage or incomplete inputs. The helper never runs Cargo, accesses a database, or writes a policy.

For schema and flag details, consult the installed release's [Cargo metadata documentation](https://doc.rust-lang.org/cargo/commands/cargo-metadata.html). Keep package IDs opaque; their serialized spelling is not a stable parsing interface.
