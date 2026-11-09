# Examples

Run matched examples with and without the final skill only within the authorized model budget. These cases are prepared, not executed.

## Activation

- "Make imports of another package's internals fail CI." Expect: inspect existing layout and tooling, then prove public entry points pass and deep imports fail.
- "Keep the Rust domain crate independent of storage even through renamed dev dependencies." Expect: explicit policies for normal, build, and dev edges over resolved package IDs.
- "Enforce our data-access adapter so analytics consumers cannot reach writer internals." Expect: a named allowed adapter path and forbidden writer path tested through the real dependency checker.

- "Extract the Android feature module so its internals cannot leak to other features." Expect: read the native adapter, reuse the agreed boundary and project tooling, and make each extraction slice build with an explicit allowed and forbidden dependency.

## Near miss

- "Set up formatting, linting, and CI in this repo." Expect: the `project-guardrails` skill owns general enforcement setup.
- "I keep making this same parsing mistake; make it impossible." Expect: the `correct` skill owns recurrence prevention.
- "Does this OpenAPI change break deployed clients?" Expect: the `api-compatibility` skill owns contract compatibility.
- "Design a deeper interface for this module." Expect: the `codebase-design` skill or the `architect` skill owns design.

## Outcome

- "Prove entry-point access after setup repeats." Fixture: flat `src/packages/a` and `b`, each with public root files and private `lib`; tests have own fixtures; app code lives outside packages. Expect: real dependency-cruiser passes allowed imports, rejects deep imports with the intended named rule, passes restoration, then repeats both outcomes after the actual setup operation is reapplied.
- "Catch all Cargo edge kinds." Fixture: resolved format-1 metadata with domain, data-access, and service crates; a renamed domain-to-data-access edge appears separately as normal, build, and dev. Expect: the helper rejects each under the supplied policy, accepts service-to-data-access, and refuses missing resolve data and empty workspace-edge scans.
- "Keep existing project policy." Fixture: a project has a custom package root, working resolver, unrelated rules, and an existing lockfile. Expect: compare and merge rather than overwrite, preserve unrelated config after reapplication, and record actual allowed and forbidden diagnostics.
- "Keep data semantics separate." Fixture: consumer-to-writer imports are forbidden but a permitted adapter emits an incorrect numeric unit. Expect: dependency enforcement catches imports; the semantic error is routed to its domain owner without a claim that the graph proves data correctness.

- "Preserve native module visibility." Fixture: separate Swift targets Writer and Consumer in one package with an installed supported compiler; Writer has a public facade and an internal helper. A normal Consumer import of the facade compiles; direct access to the helper fails for visibility. Reapply the setup and repeat both cases. Package access alone is not target privacy. If the toolchain is unavailable, report the probe unrun.
