---
name: codebase-design
description: Refine a named module's public interface or test seam in one codebase. Apply depth, deletion-test and adapter-boundary heuristics to its code and callers; provide required shared vocabulary. Broad distributed-system and infrastructure architecture is outside this scope.
license: MIT
metadata:
  source: "https://github.com/mattpocock/skills/blob/49dd158d1076134a641b33efb035946536778336/skills/engineering/codebase-design/SKILL.md"
  source-files: "skills/engineering/codebase-design/SKILL.md"
  source-revision: 49dd158d1076134a641b33efb035946536778336
  local-changes: "Kept the deep-module glossary, deletion test and testability rules; made adapter counts, size and vocabulary heuristics that yield to repository terms, trust boundaries, defensive checks and public compatibility; merged nine pstack design principles; moved alternative-interface exploration to the architect skill; relocated DEEPENING and DESIGN-IT-TWICE into references."
---

# Codebase design

Design **deep modules**: a lot of behaviour behind a small interface, placed at a clean seam, testable through that interface. Use this language and these principles wherever code is being designed or restructured. The aim is leverage for callers, locality for maintainers, and testability for everyone.

Correctness, valid domain and runtime types, real trust boundaries, data fidelity and public compatibility outrank fewer lines or a tidier shape. Every rule below is a heuristic in service of those.

## Glossary

Use these terms for design discussion, consistently. When the repository already has its own names (it calls modules "services", interfaces "APIs"), keep the repository's terms in code and docs and map them to these in your reasoning; don't rename the project to match the glossary.

**Module**: anything with an interface and an implementation. Deliberately scale-agnostic: a function, class, package, or tier-spanning slice.

**Interface**: everything a caller must know to use the module correctly: the type signature, but also invariants, ordering constraints, error modes, required configuration, and performance characteristics. A type signature alone is too narrow.

**Implementation**: what's inside a module, its body of code. Distinct from **Adapter**: a thing can be a small adapter with a large implementation (a Postgres repo) or a large adapter with a small implementation (an in-memory fake). Reach for "adapter" when the seam is the topic; "implementation" otherwise.

**Depth**: leverage at the interface. The amount of behaviour a caller (or test) can exercise per unit of interface they have to learn. A module is **deep** when a large amount of behaviour sits behind a small interface, **shallow** when the interface is nearly as complex as the implementation.

**Seam** _(Michael Feathers)_: a place where you can alter behaviour without editing in that place; the *location* at which a module's interface lives. Where to put the seam is its own design decision, distinct from what goes behind it.

**Trust boundary**: where data or control crosses from a less trusted context into a more trusted one: user input, network and IPC messages, files, config, environment, and internal privilege transitions. A seam may or may not be a trust boundary; "internal" does not mean trusted.

**Adapter**: a concrete thing that satisfies an interface at a seam. Describes *role* (what slot it fills), not substance (what's inside).

**Leverage**: what callers get from depth. More capability per unit of interface they learn. One implementation pays back across N call sites and M tests.

**Locality**: what maintainers get from depth. Change, bugs, knowledge, and verification concentrate in one place rather than spreading across callers. Fix once, fixed everywhere.

## Deep vs shallow

**Deep module** = small interface + lots of implementation:

```
┌─────────────────────┐
│   Small Interface   │  ← Few methods, simple params
├─────────────────────┤
│                     │
│  Deep Implementation│  ← Complex logic hidden
│                     │
└─────────────────────┘
```

**Shallow module** = large interface + little implementation (usually avoid):

```
┌─────────────────────────────────┐
│       Large Interface           │  ← Many methods, complex params
├─────────────────────────────────┤
│  Thin Implementation            │  ← Just passes through
└─────────────────────────────────┘
```

When designing an interface, ask: Can I reduce the number of methods? Simplify the parameters? Hide more complexity inside? A deep module is not a deep call chain: a chain scatters understanding across layers; a deep module concentrates capability behind one interface.

## Principles

- **Depth is a property of the interface, not the implementation.** A deep module can be internally composed of small, mockable, swappable parts; they just aren't part of the interface. A module can have **internal seams** (private to its implementation, used by its own tests) as well as the **external seam** at its interface.
- **The deletion test.** Imagine deleting the module. If complexity vanishes, it was a pass-through. If complexity reappears across N callers, it was earning its keep.
- **The interface is the test surface.** Callers and tests cross the same seam. If you want to test *past* the interface, the module is probably the wrong shape.
- **Count the adapters.** A seam with one adapter is usually just indirection; two (typically production and test) make it real. Keep a single-adapter seam when it marks a real trust boundary, a deployment or process boundary, or a test seam the project already relies on.
- **Data structures first.** Choose the data model and its organizing structure before the logic; trace each dominant access pattern through it.
- **Validate at trust boundaries; trust types inside.** Parse external data into domain types where it enters, keep transport and storage types private, and keep required defensive checks where trust actually changes.

More: [references/principles.md](references/principles.md) holds the full design rules (domain modeling, types, idempotency, migration, reader load, subtraction) — read it when choosing a data model, changing an interface with callers, or simplifying.

## Designing for testability

Good interfaces make testing natural:

1. **Accept dependencies, don't create them.**

   ```typescript
   // Testable
   function processOrder(order, paymentGateway) {}

   // Hard to test
   function processOrder(order) {
     const gateway = new StripeGateway();
   }
   ```

2. **Return results, don't produce side effects.**

   ```typescript
   // Testable
   function calculateDiscount(cart): Discount {}

   // Hard to test
   function applyDiscount(cart): void {
     cart.total -= discount;
   }
   ```

3. **Small surface area.** Fewer methods = fewer tests needed. Fewer params = simpler test setup.

## Relationships

- A **Module** has exactly one **Interface** (the surface it presents to callers and tests).
- **Depth** is a property of a **Module**, measured against its **Interface**.
- A **Seam** is where a **Module**'s **Interface** lives.
- An **Adapter** sits at a **Seam** and satisfies the **Interface**.
- **Depth** produces **Leverage** for callers and **Locality** for maintainers.

## Rejected framings

- **Depth as ratio of implementation-lines to interface-lines** (Ousterhout): rewards padding the implementation. We use depth-as-leverage instead.
- **"Interface" as the TypeScript `interface` keyword or a class's public methods**: too narrow: interface here includes every fact a caller must know.
- **Fewer lines as the goal**: shorter code that drops a check, a compatibility path or precision is not simpler, it is wrong.

## Going deeper

- **Deepening a cluster given its dependencies**: [references/deepening.md](references/deepening.md) covers dependency categories, seam discipline, and replace-don't-layer testing. Read it before proposing a deepening refactor.
- **Exploring alternative interfaces**: [references/design-it-twice.md](references/design-it-twice.md) holds the framing and comparison criteria. The `architect` skill runs the alternatives and owns the design artifact.

## Provenance

Adapted from Matt Pocock's codebase-design skill, with principles from pstack. See [references/SOURCES.md](references/SOURCES.md) and the `LICENSE-*` files.
