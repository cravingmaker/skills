# Deepening

Read this before proposing a refactor that deepens a cluster of shallow modules. Adapted from Matt Pocock's codebase-design/DEEPENING.md. Assumes the vocabulary in the skill: **module**, **interface**, **seam**, **adapter**.

## Dependency categories

When assessing a candidate for deepening, classify its dependencies. The category determines how the deepened module is tested across its seam.

### 1. In-process

Pure computation, in-memory state, no I/O. Always deepenable: merge the modules and test through the new interface directly. No adapter needed.

### 2. Local-substitutable

Dependencies that have local test stand-ins (PGLite for Postgres, an in-memory filesystem). Deepenable if the stand-in exists. The deepened module is tested with the stand-in running in the test suite. The seam is internal; no port at the module's external interface.

### 3. Remote but owned (ports and adapters)

Your own services across a network (microservices, internal APIs). Define a **port** (interface) at the seam. The deep module owns the logic; the transport is injected as an **adapter**. Tests use an in-memory adapter. Production uses an HTTP, gRPC or queue adapter. The network hop is still a trust boundary: the production adapter parses and validates what arrives.

Recommendation shape: *"Define a port at the seam, implement an HTTP adapter for production and an in-memory adapter for testing, so the logic sits in one deep module even though it's deployed across a network."*

### 4. True external (mock)

Third-party services (Stripe, Twilio, etc.) you don't control. The deepened module takes the external dependency as an injected port; tests provide a mock adapter.

## Seam discipline

- **Adapter count is a heuristic.** Introduce a port when at least two adapters are justified (typically production and test); a single-adapter seam is usually just indirection. Keep or add one when it marks a trust boundary, a process or deployment boundary, or a seam the project's tests already depend on.
- **Internal seams vs external seams.** A deep module can have internal seams (private to its implementation, used by its own tests) as well as the external seam at its interface. Don't expose internal seams through the interface just because tests use them.
- **Callers.** Callers you control migrate in the same change as the new interface. Public, published or independently deployed consumers need compatibility: expand (add the new interface), migrate, then contract (remove the old one) when the consumers have moved.

## Testing strategy: replace, don't layer

- Write new tests at the deepened module's interface. The **interface is the test surface**.
- Tests assert on observable outcomes through the interface, not internal state.
- Tests should survive internal refactors, since they describe behaviour, not implementation. If a test has to change when the implementation changes, it's testing past the interface.
- Old unit tests on the shallow modules become waste once interface tests cover the same behaviour; delete those. Keep any old test that pins behaviour the new tests do not yet cover, and move its case to the interface first.
