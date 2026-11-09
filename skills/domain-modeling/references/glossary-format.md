# Glossary format

Read this when writing the first glossary entry, or when the configured glossary has no format of its own yet. An existing project format wins.

## Structure

```md
# {Context Name}

{One or two sentence description of what this context is and why it exists.}

## Language

**Order**:
{A one or two sentence description of the term}
_Avoid_: Purchase, transaction

**Invoice**:
A request for payment sent to a customer after delivery.
_Avoid_: Bill, payment request
_Source_: [ADR-0004]({ADR directory}/0004-invoice-on-delivery.md)

**Customer**:
A person or organization that places orders.
_Avoid_: Client, buyer, account
```

## Rules

- **Be opinionated.** When several words exist for one concept, pick the best one and list the others under `_Avoid_`.
- **Keep definitions tight.** One or two sentences. Define what the term is, not what it does.
- **Only terms specific to this context.** General programming concepts (timeouts, error types, utility patterns) stay out even when the project uses them a lot. Before adding a term, ask whether it is unique to this context.
- **Link the authority** with an optional `_Source_` line when the definition comes from a decision, a regulation, or a document a reader may need to check.
- **Group terms under subheadings** when natural clusters emerge. A flat list is fine for one cohesive area.

## Single and multiple contexts

The project's domain setup (`docs/agents/domain.md`) says which layout applies and where each file lives.

- **Single context:** one glossary at the configured path.
- **Multiple contexts:** a map file at the configured path lists the contexts, where each glossary lives, and how the contexts relate:

```md
# Glossary Map

## Contexts

- [Ordering]({ordering glossary path}): receives and tracks customer orders
- [Billing]({billing glossary path}): generates invoices and processes payments
- [Fulfillment]({fulfillment glossary path}): manages warehouse picking and shipping

## Relationships

- **Ordering → Fulfillment**: Ordering emits `OrderPlaced` events; Fulfillment consumes them to start picking
- **Fulfillment → Billing**: Fulfillment emits `ShipmentDispatched` events; Billing consumes them to generate invoices
- **Ordering ↔ Billing**: Shared types for `CustomerId` and `Money`
```

Fill each `{path}` with the location the setup records.

When several contexts exist, infer which one the topic belongs to. If it is unclear, ask.
