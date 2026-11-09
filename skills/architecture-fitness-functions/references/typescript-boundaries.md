# TypeScript boundary adapter

Read this when an existing flat package root treats root files as public entry points.

Pair the real checker JSON output with `scripts/check-import-scan.py`, requiring app and package roots separately. A successful CLI exit with no TypeScript modules can indicate absent or incompatible parser support. Inspect the installed release's supported transpilers; keep pre-compilation and type-edge coverage enabled.

Discover the package root, entry-point convention, colocated tests, resolver, lockfile, and current dependency check. Multiple root files may be public; do not force a single barrel or create a demo package in product code. If the project has another model, retain its convention and implement the corresponding rules with its existing tool.

The adapted dependency-cruiser starter treats any package subfolder as private. Production files may reach their own internals. External code and other packages may reach only public root files. Tests may reach public root files and their own fixtures, but no package internals. Production code cannot import test fixtures. Cycles and unresolved imports fail.

Set `PACKAGES_ROOT` to the inspected root. Merge named rules and relevant resolver options into the current config. The starter pins the release used by its fixture tests; review installed release docs before adopting it. Use the repository's package manager and approved exact version if a new dependency is in scope. Retain aliases and TypeScript compiler options the real project needs.

Run the checker over app code as well as packages so the app-to-internal rule has coverage. Check the reported module and edge counts. Prove app deep imports, cross-package deep imports, test deep imports, fixture privacy, cycles, and unresolved imports separately. Prove multiple public entries, same-package internals, and own test fixtures remain allowed.

Reapply the actual merge or setup operation. Compare the config and rerun allowed and forbidden cases. Do not call two checker runs a setup-reapplication test. The repository fixture restores the starter from its source twice in a disposable project and checks both outcomes after each application. A project-specific merge still needs its own preservation proof.

Use a concise pointer from the project's existing agent instructions to the chosen boundary rule only when instruction edits are authorized. Avoid writing another convention manual when an existing document already owns it.
