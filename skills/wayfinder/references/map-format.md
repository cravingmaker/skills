# Map format

Read this before charting a map or adding tickets to one.

## Contents

- Map body
- Ticket body
- Local layout
- Remote trackers

## Map body

The whole map at low resolution, loaded once per session. Open tickets are not listed in it; they are found by querying the map's open children.

```markdown
## Destination

<what reaching the end of this map looks like: the spec, decision, or change this effort is finding its way to. One or two lines; every session orients to it before choosing a ticket.>

## Notes

<domain; skills every session should consult; standing preferences for this effort>

## Decisions so far

<!-- the index: one line per closed ticket, enough to judge relevance, then follow the link for the detail the ticket holds -->

- [<closed ticket title>](link): <one-line gist of the answer>

## Not yet specified

<!-- in-scope fog you can't ticket yet; graduates as the frontier advances -->

## Out of scope

<!-- work ruled beyond the destination; closed, never graduates -->
```

## Ticket body

```markdown
## Question

<the decision or investigation this ticket resolves>
```

The answer is not part of the body; it is recorded on resolution.

## Local layout

Use the layout the tracker setup's "Wayfinding operations" section names. When it names none:

- **Map:** `.scratch/<effort>/map.md`.
- **Ticket:** `.scratch/<effort>/issues/NN-<slug>.md`, numbered from `01`, with the question in the body, a `Type:` line (`research`, `prototype`, `grilling`, or `task`), and a `Status:` line (`open`, `claimed`, or `resolved`).
- **Blocking:** a `Blocked by: NN, NN` line near the top. A ticket is unblocked when every file it lists is `resolved`.
- **Frontier:** the files that are open, unblocked, and unclaimed; the lowest number wins.
- **Claim:** set `Status: claimed` and save before any work.
- **Resolve:** append the answer under an `## Answer` heading, set `Status: resolved`, then add the context pointer to `map.md`.

## Remote trackers

The tracker setup's "Wayfinding operations" section says how this repo expresses each operation. The usual shape:

- **Map:** one issue labelled `wayfinder:map`.
- **Ticket:** a child issue of the map, labelled `wayfinder:<type>`. The `wayfinder:` labels are the only labels a map and its tickets carry.
- **Blocking:** the tracker's native dependency link, because it shows the frontier in the tracker's own interface; a `Blocked by:` line only where native links are unavailable.
- **Claim:** assign the ticket to the person driving the map, as the session's first write.
- **Resolve:** post the answer as a comment, close the issue, then add the context pointer to the map's Decisions so far.
