# Examples

Run each prompt with and without this skill. Record the observed behavior against the expectation.

## Activation

- "This OrderService has twelve public methods and every caller strings four of them together. How should its interface look?" Expect: the skill loads; the answer judges depth at the interface, applies the deletion test and proposes a smaller interface that hides the sequencing.
- "Where should the seam go so we can test the pricing logic without the payment gateway?" Expect: classifies the dependency (true external), proposes an injected port with production and test adapters, and tests through the module's interface.
- "Our codebase calls these things services. Can you use your module vocabulary to review this one?" Expect: keeps the repository's word "service" in the write-up while reasoning with module, interface and seam.

## Near miss

- "Design the overall system for a multi-region chat service with queues and databases." Expect: the skill does not load; this is system design (the engineering system-design skill or ordinary reasoning).
- "Sketch the types and signatures for the new export feature before we code it." Expect: the `architect` skill handles the design artifact; this skill is read only as its vocabulary.
- "Add a GLOSSARY.md entry for 'Settlement'." Expect: domain glossary work, not this skill.

## Outcome

- A deepening proposal keeps a single-adapter seam that marks a real trust boundary instead of removing it to satisfy the two-adapter heuristic.
- A recommendation that shrinks code never drops a defensive check at a trust boundary, a compatibility path for public consumers, numeric precision or unknown fields.
- A change to an interface with independently deployed consumers proposes expand, migrate, then contract; controlled callers are migrated in the same change.
