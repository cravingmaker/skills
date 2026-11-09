---
name: architecture-fitness-functions
description: Enforce architectural dependency rules with checks that reject forbidden imports or crate edges and accept allowed ones after repeated setup. Use for layer direction, public entry points, cycles, crate layering, or public-API growth. General CI setup stays with project-guardrails.
license: MIT
metadata:
  verified: "2026-11"
  source: "https://github.com/mattpocock/skills/blob/49dd158d1076134a641b33efb035946536778336/skills/in-progress/setup-ts-deep-modules/SKILL.md"
  source-revision: "49dd158d1076134a641b33efb035946536778336"
  source-files: "skills/in-progress/setup-ts-deep-modules/SKILL.md"
  local-changes: "Made setup an optional discovered-layout adapter; retained public-entry, fixture-privacy, and cycle rules; added unresolved imports and package-root escaping; removed automatic installs and example commits; added Rust and data-boundary methods and repeated-setup proof."
---

# Architecture fitness functions

Make a named architectural dependency rule fail in the build. Start with unreachable illegal states, then use static graph checks and executable counterexamples. Read [per-file provenance](references/SOURCES.md) when checking the retained TypeScript adapter.

This capability owns architectural imports, crate layers, and public-surface rules. General formatter, lint, hooks, and CI policy use the `project-guardrails` skill. A repeated mistake uses the `correct` skill; wire compatibility uses the `api-compatibility` skill. For a module seam, use the `codebase-design` skill. Read a routed skill before using it; none is required to run this helper.

## Select enforcement

1. Name the invariant, affected roots, allowed and forbidden edges, and motivating decision or defect. State how type-only, runtime, build, dev, generated, and platform-specific edges count.
2. Inspect layout, exports, privacy, graph tools, package manager, lockfile, and the normal check command. Prefer an existing sufficient checker. Change tooling only within the authorized task.
3. Make internals inaccessible where the runtime or compiler supports it. Use package exports and explicit entry points for Node, and private modules or scoped Rust visibility. Relative source paths can bypass package exports; inspect the actual import route.
4. Add the smallest static rule for the remaining graph. Treat empty scans, unresolved imports, and unclassified files as missing coverage. Read [tool selection and proof](references/tool-selection.md) for versions, baselines, and public API growth.

Done when the rule has an owner and a command whose scan includes a real relevant edge.

## Use the relevant adapter

For flat TypeScript packages with public root files and private subfolders, read [the TypeScript adapter](references/typescript-boundaries.md). Compare [the dependency-cruiser starter](assets/dependency-cruiser.cjs) with the existing config; merge scoped rules rather than overwriting it. Preserve multiple public entry points and the project's layout. This optional adapter also checks tests through public entry points, fixture privacy, unresolved imports, and cycles. It does not require reorganizing a project.

For Rust workspace layers, read [the Cargo policy](references/cargo-boundaries.md). Generate resolved metadata with installed Cargo, then run `python3 scripts/check-cargo-boundaries.py METADATA.json POLICY.json`. Compare [the policy example](assets/cargo-policy.json) with actual crate names. The stdlib helper separates normal, build, and dev edges, including renamed and target-specific dependencies, and rejects incomplete or empty graph inputs.

For native module extraction or dependency rules, read [native module boundaries](references/native-module-boundaries.md). Use the agreed graph, compiler visibility, and incremental build evidence; platform syntax does not create a new design workflow.

For data-interface or writer-component rules, read [data interface boundaries](references/data-interface-boundaries.md). Name the data-access adapter and prove consumers cannot import writer internals. Semantic data quality, privacy behavior, and governance drift remain with their domain owners.

## Prove the rule and setup

For dependency-cruiser, generate a fresh JSON report and run `python3 scripts/check-import-scan.py GRAPH.json --require-root ROOT` for each intended root. Preserve both the checker exit status and the helper exit status in CI. The helper rejects empty or wrongly scoped scans, including an absent or incompatible parser; it cannot prove report freshness or complete parser support.

1. Run an allowed edge through the real configured checker and require success.
2. Add a forbidden edge in an owned disposable fixture and require the intended rule and failing exit. The dependency must resolve; syntax or missing-file errors do not prove the boundary.
3. Restore the allowed edge and require success.
4. Reapply the actual setup or merge operation. Check that it preserves unrelated config and does not duplicate or weaken rules. Rerun forbidden and allowed cases. Running the same check twice does not prove setup survives reapplication.
5. Wire the proven command into normal local and CI checks within current authority. If CI changes are outside scope, hand over the exact command and mark wiring pending.

For legacy violations, baseline exact edges with a reason, owner, and removal trigger. Fail on new edges and remove stale exceptions; a directory-wide ignore cannot serve as a ratchet.

Verify tool versions, Node support, resolver behavior, rule names, and cargo-deny semantics against the installed release and official docs at use time. The starter's recorded version is a tested example, not an instruction to upgrade. Read [version evidence](references/version-evidence.md) when checking the example.

Done when forbidden edges fail, allowed edges pass after actual setup reapplication, empty or unresolved scans cannot pass, and the normal check path runs the rule or has an explicit pending handoff. Report commands, diagnostics, roots, target/feature scope, exceptions, and local versus CI evidence.
