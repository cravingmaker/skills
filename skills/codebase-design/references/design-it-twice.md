# Design it twice

Read this when comparing alternative interfaces for a chosen candidate. Adapted from Matt Pocock's codebase-design/DESIGN-IT-TWICE.md, based on Ousterhout's "Design It Twice": your first idea is unlikely to be the best. The `architect` skill runs the comparison and decides whether independent agents are worth their cost; this file holds the method it applies.

## 1. Frame the problem space

Before producing any design, write a short explanation of the problem space for the chosen candidate:

- The constraints any new interface must satisfy, including callers you cannot break and trust boundaries it crosses
- The dependencies it relies on, and which category each falls into (see [deepening.md](deepening.md))
- A rough illustrative code sketch to ground the constraints: not a proposal, just a way to make the constraints concrete

Share it with the user when they are present; they read and think while the designs are produced.

## 2. Produce distinct designs

Produce at least two, usually three, **radically different** interfaces, each under a different constraint:

- "Minimize the interface: aim for 1–3 entry points max. Maximise leverage per entry point."
- "Maximise flexibility: support many use cases and extension."
- "Optimise for the most common caller: make the default case trivial."
- "Design around ports and adapters for cross-seam dependencies" (if applicable).

Each design uses the skill's vocabulary and the project's domain vocabulary, and states:

1. Interface (types, methods, params, plus invariants, ordering, error modes)
2. Usage example showing how callers use it
3. What the implementation hides behind the seam
4. Dependency strategy and adapters (see [deepening.md](deepening.md))
5. Trade-offs: where leverage is high, where it's thin

Whole-shape alternatives, not point fixes inside one shape. When designs are written one after another by the same agent, they are not independent; say so.

## 3. Present and compare

Present designs one at a time so the reader can absorb each, then compare them in prose by **depth** (leverage at the interface), **locality** (where change concentrates), and **seam placement**, plus compatibility cost for existing callers.

After comparing, give your recommendation: which design is strongest and why. If elements from different designs combine well, propose a hybrid. Be opinionated: the reader wants a strong read, not a menu.
