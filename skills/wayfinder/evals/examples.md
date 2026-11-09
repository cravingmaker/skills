# Examples

Run each prompt with and without this skill. Install `research`, `prototype`, `grilling`, and `domain-modeling` in both arms. Use two fixtures: one with a GitHub tracker setup that has a "Wayfinding operations" section, and one with no setup. Record the observed behavior against the expectation.

## Activation

- "wayfinder: we want to move the whole product from REST to an event-driven backend, and I don't know where to start." Expect: the destination named first by interview, then a map with Destination, Notes, Not yet specified, and decision tickets with types and blockers, written as local files.
- "wayfinder: work the next ticket on .scratch/event-backend/map.md." Expect: the first frontier ticket claimed before any work, resolved by its type, recorded on the ticket and in Decisions so far; only one non-research ticket per session.
- "wayfinder: chart this on our GitHub tracker; you can create the issues." Expect: the map and tickets created on the configured tracker through its wayfinding operations.

## Near miss

- "Rename the `users` table column `name` to `full_name`." Expect: the change or a ticket breakdown; no map.
- "Break the approved migration spec into tickets." Expect: the `to-tickets` skill, with build tickets, not decision tickets.
- "Grill me on whether to use Kafka." Expect: the `grilling` skill alone; no map.

## Outcome

- Without publishing authority, the map is local files even when a remote tracker is configured; with authority, the configured tracker's operations are used.
- With no setup, the map is charted locally and the missing setup is stated; there is no contradiction between "run setup" and "use local".
- Decision tickets carry no build label, and the map hands a build off to the `to-spec` and `to-tickets` skills.
- No branch, push, or pull request is created, and no fixed token-size session limit or compulsory parallel research appears.
- Subagent starts for research stay within the declared budget, and settled ADRs or decisions are not ticketed again.
