# Design principles

Read this when choosing a data model, placing validation, changing an interface that has callers, or simplifying code. Adapted from nine pstack principles: model-the-domain, foundational-thinking, type-system-discipline, boundary-discipline, make-operations-idempotent, migrate-callers-then-delete-legacy-apis, minimize-reader-load, laziness-protocol and subtract-before-you-add. Each is a heuristic; correctness, compatibility, rationale and data fidelity win a conflict.

## Contents

- [Model the domain](#model-the-domain)
- [Data structures first](#data-structures-first)
- [Type discipline](#type-discipline)
- [Trust boundaries](#trust-boundaries)
- [Idempotent operations](#idempotent-operations)
- [Migrating callers](#migrating-callers)
- [Reader load](#reader-load)
- [Laziness and subtraction](#laziness-and-subtraction)

## Model the domain

Encode the real domain in a data structure instead of scattering it across conditionals. A structure that matches the domain makes invalid states unrepresentable and deletes branches. Reach for:

- A state machine instead of scattered booleans, phases or lifecycle checks.
- A typed model instead of loose parameters or repeated shape assumptions.
- A map, registry, lookup table or discriminated union instead of branching spread across files.
- A reducer or command/event model instead of ad hoc state mutations.
- A module organized around one body of domain knowledge instead of a sequence such as load, validate, transform, save. Execution order is not ownership.
- A queue, cache, index, graph, tree or normalized collection where the access pattern calls for it.

Do not force an abstraction. Prefer boring code when the current shape is already clear, local and unlikely to grow. The sign you skipped this is a feature that grows an if/else chain by one more branch, or a second boolean that must stay in sync with the first. This governs how code represents the domain; the project's glossary and decision records (the `domain-modeling` skill) own what the domain terms mean.

## Data structures first

Structural decisions protect option value; code-level decisions protect simplicity. Define core types early, trace every access pattern, and choose structures that match the dominant paths. DRY the structure, not every line: three similar statements still beat a premature abstraction. Before sharing state between actors, ask what happens if another actor modifies it concurrently; if the answer isn't "nothing", isolate it. Each increment should land a coherent abstraction or deepen one, not spread a new capability across callers as special cases. Sequencing the work itself (scaffold first, verifiable units) belongs to planning, not to this skill.

## Type discipline

Make the type checker reject impossible states, mismatched primitives and unhandled variants. Prefer defining errors and special cases out of existence over multiplying handlers.

- **Brand semantic primitives.** `UserId` and `OrderId` are strings underneath but should not be interchangeable; give each its own type (a branded type, a newtype). Validate once at creation.
- **External data is untyped until parsed.** RPC payloads, JSON, IPC messages, CLI args, config, environment variables, database rows: parse them into the typed model where they enter.
- **Derive types from authoritative schemas** (protocol buffers, OpenAPI, GraphQL, migrations) instead of hand-rolling a parallel type.
- **Runtime checks stay honest.** A type assertion or cast is not validation; where the type system cannot prove a property, check it at runtime.

## Trust boundaries

Place validation, narrowing and error handling where data crosses a trust boundary; keep business logic in pure functions behind it.

- **At the boundary** (CLI args, config, network, external APIs, files, environment, and internal privilege transitions): validate, return errors, handle defensively.
- **Inside the trusted region:** typed data and error propagation, without re-validating what the boundary already checked.
- **Across the boundary:** expose domain concepts, not the boundary's private representation; don't re-export transport, storage, framework or wire types through a public interface.

"Internal" does not mean trusted: a request from another internal service, a job payload or a lower-privilege component is still input. Keep defensive checks that the code's security, integrity or legal obligations require, even where they look redundant.

## Idempotent operations

Design operations to converge on the correct state however many times they run and wherever a previous run stopped. Derive each step from the state that exists, not from what the previous run meant to do: read current state, compare with the goal, apply only the difference.

Anything a run leaves behind (a lock, a temporary file, a half-written record, a claimed job) must be recognizable as stale by the next run, by evidence that stays true wherever the run could have stopped. For example, write to a temporary path and rename it into place, or compare artifacts by content rather than creation order. Test: what happens if it runs twice; if the previous run crashed at each point; does re-execution converge? Domain protocols such as payment idempotency keys belong to their specialist role skills.

## Migrating callers

When a new interface replaces an old one:

- **Callers you control** (same repository, deployed together): migrate every caller and delete the old interface in the same change. No compatibility shims or parallel old and new paths. Update tests to assert the new contract, and delete tests that only protect pre-refactor implementation details.
- **Public, published or independently deployed consumers:** keep compatibility. Expand (add the new interface), migrate consumers, then contract (remove the old one) once they have moved, with any deprecation the project's policy requires.

## Reader load

Maintainability is the work a reader must do to understand code, on two axes: **layers to trace** (indirections between a question and its answer) and **state to hold** (hidden or mutable context). Lines of code and complexity scores are proxies.

- Collapse layers that cost more than they save: wrappers with one caller, pass-through layers that repeat the same methods and arguments, speculative indirection.
- Demand interface compression: an interface that hides little makes readers learn both it and the implementation.
- Shrink state scope: returns over mutations, locals over fields, fields over module state, module state over globals. Derive instead of syncing.
- Name an invariant once at the boundary, not in every consumer.
- Keep the project's domain terms and comments that explain why; they lower reader load.

Test: can a new reader answer "where does X come from?" and "what can change X?" quickly? If not, cut layers or cut state.

## Laziness and subtraction

- **Consolidate decisions.** Put a repeated choice behind one source of truth and pass the result along.
- **Make the smallest change that solves the problem.** Fewer lines beat elegant boilerplate, provided behavior, checks and compatibility are kept.
- **Subtract before you add.** Remove dead code, redundant mechanisms and orphan references before building the new shape; design for observed usage rather than speculative cases.
- **What never counts as redundant:** security and integrity checks, compatibility paths for real consumers, rationale and legal comments, and data fidelity (precision, unknown fields, exact values).
