# Data interface boundaries

Read this when a dependency rule separates data consumers from a writer component.

Name the authoritative writer and the public data-access adapter. Define the allowed consumer-to-adapter path and the forbidden consumer-to-writer-internals path. Use actual packages, crates, or modules; a catalog's component name alone is not an enforceable boundary.

Include imports, re-exports, generated bindings, tests, and type-only references according to the declared policy. An allowed query adapter can expose read operations without granting write authority. Check direct and transitive imports so a shared helper cannot conceal a forbidden storage dependency.

Create one valid consumer using the adapter and one consumer reaching writer internals. Run both through the actual configured dependency checker after setup and after setup is reapplied. The valid consumer passes and the forbidden path fails its architectural rule. If SQL privileges enforce a separate writer restriction, hand that evidence to the database owner; an import check proves no SQL privilege claim.

Quality assertions, privacy tests, semantic contract validation, and control-register drift stay with their domain owners. This adapter proves dependency direction and public access paths only.
