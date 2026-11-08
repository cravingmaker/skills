---
name: wayfinder
description: Chart a goal too large and unclear for one agent session as a map of decision tickets, then resolve one consequential decision per session until the way to the destination is clear. Use when the user invokes wayfinder to chart such a map or to work the next ticket on one.
license: MIT
metadata:
  requires: "research prototype grilling domain-modeling"
  source: "https://github.com/mattpocock/skills/blob/49dd158d1076134a641b33efb035946536778336/skills/engineering/wayfinder/SKILL.md"
  source-revision: 49dd158d1076134a641b33efb035946536778336
  source-license: MIT, see LICENSE-mattpocock
  source-files: "skills/engineering/wayfinder/SKILL.md"
  local-changes: "The configured tracker and its wayfinding operations win; local map files are the default until publishing is authorized; removed the fixed 100K-token session size, compulsory parallel research, research branches and pushes, and open-ended scheduling; research, prototype, grilling, and domain-modeling run within current authority and the shared budget, reusing settled facts; map and ticket formats moved to a reference."
---

# Wayfinder

A loose idea has arrived, too big for one agent session and wrapped in fog: the way from here to the **destination** is not visible yet. Wayfinding finds that way instead of charging at the destination. It charts a **map** of **decision tickets** (questions whose answer is a decision, not slices of a build) and resolves them one at a time until the route is clear.

The destination varies: a spec to hand off, a decision to lock before planning, or a change made in place such as a data migration. Naming it is the first act of charting. The map works for any domain: engineering, course content, whatever fits.

## Plan, don't do

Wayfinder plans by default. Each ticket resolves a decision; the map is done when nothing is left to decide before someone does the work. The pull to just do the work usually means you have reached the edge of the map and it is time to hand off: a build goes through the `to-spec` and `to-tickets` skills. An effort can carry execution into the map through its **Notes**; absent that, produce decisions, not deliverables.

Decision tickets never carry a build label such as `ready-for-agent`. They are not delivery tickets.

## Where the map lives

1. Read `docs/agents/issue-tracker.md` and its "Wayfinding operations" section, written by the `setup-agent-skills` skill. When the setup names a tracker and those operations, use them.
2. **Local files are the default** until publishing to a remote tracker is authorized: the user asked to publish the map, or ran this skill on a map that already lives there. Use the local layout the setup names, or the one in [references/map-format.md](references/map-format.md) when it names none.
3. If the setup is missing, chart locally and say so; the `setup-agent-skills` skill can configure a tracker later.
4. On a remote tracker, use the host's connected tools when they can do the operation, and the CLI the setup names otherwise.

## Refer by name

Every map and ticket has a **name**: its title. In everything the human reads, refer to it by name, never by a bare id, number, or slug. The id and link ride inside the name; they never stand in for it.

## The map and its tickets

The map is an **index**, not a store: it lists decisions made and points at the tickets that hold their detail. A decision lives in one place, its ticket. Formats for the map body and tickets: [references/map-format.md](references/map-format.md). Read it before charting.

- Each ticket's body is one question sized to one agent session.
- Each ticket has one type: `research`, `prototype`, `grilling`, or `task`.
- A session **claims** a ticket first, before any work, so concurrent sessions skip it.
- A ticket is **unblocked** when every ticket blocking it is closed. The **frontier** is the open, unblocked, unclaimed tickets.
- Prefer the tracker's native blocking; fall back to a body convention only where it has none.
- Assets made while resolving a ticket are linked from it, not pasted in.

## Ticket types

Every ticket is **HITL** (worked with a human who speaks for themselves) or **AFK** (driven by the agent alone). A HITL ticket resolves only through that live exchange; the agent never answers the human's side.

- **Research** (AFK): surface a fact a decision waits on, from documentation, third-party APIs, or local knowledge outside the working directory. Resolve it with the `research` skill. Record findings on the ticket or in a local file linked from it.
- **Prototype** (HITL): raise the fidelity of the discussion with a cheap, rough artifact to react to (an outline, a stub, UI or logic code), using the `prototype` skill. Link the prototype as an asset. Use when "how should it look" or "how should it behave" is the question.
- **Grilling** (HITL): the default. Run the `grilling` interview with the `domain-modeling` discipline.
- **Task** (HITL or AFK): manual work that must happen before a decision can be made, such as signing up for a service so its API can be judged, or moving data so its shape can be seen. Do it alone only within the user's current authority; otherwise hand the human a precise checklist. The answer records what was done and any facts later tickets depend on (credential locations, URLs, row counts), never the secrets themselves.

## Fog of war and out of scope

The map is deliberately incomplete. Beyond the live tickets lies the **fog**: decisions you can tell are coming but cannot pin down yet. The map's **Not yet specified** section records it. The test is whether you can state the question precisely now, not whether you can answer it:

- **Ticket** when the question is already sharp, even if it is blocked.
- **Not yet specified** when you cannot phrase it that sharply yet. Do not pre-slice fog into ticket-sized pieces.

Work beyond the destination is **out of scope**, not fog: it never graduates. When an existing ticket turns out to sit past the destination, close it and add one line to **Out of scope** with the reason and a link. It stays out of **Decisions so far**, which records the route walked.

## Chart the map

The user brings a loose idea.

1. **Reuse what is settled.** Read the existing ADRs, glossary, specs, and any prior map on the topic. Settled decisions are not ticketed again.
2. **Name the destination** with the `grilling` interview and the `domain-modeling` discipline. The destination fixes the scope, so it is settled first.
3. **Map the frontier.** Grill breadth-first, across the whole space, surfacing the open decisions and first steps. If this surfaces no fog (the whole journey fits one session), you do not need a map: stop and ask the user how to proceed.
4. **Create the map** with Destination and Notes filled in, Decisions so far empty, and the fog sketched into Not yet specified.
5. **Create the tickets you can specify now**, then wire blockers in a second pass, once every ticket has its real id. Write cross-references in that pass with real ids; a placeholder `#<n>` links to an unrelated issue.
6. Stop. Charting is one session's work and resolves no tickets. Research tickets wait for a working session.

## Work through the map

The user brings a map (a path, a URL, or a number), optionally with a ticket.

1. Load the map and only the ticket headers needed to identify the frontier.
2. Choose the ticket the user named, or else the first frontier ticket in order. Save its claim and confirm it before reading resolution sources or investigating the answer. If the claim cannot be saved, stop that ticket's work.
3. Resolve it as its type says. Read the type from the label or `Type:` line, not the body. Fetch related or closed tickets on demand, and read the skills the map's Notes name.
4. Record the resolution: the answer on the ticket, the ticket closed, and a one-line context pointer added to the map's Decisions so far.
5. Add newly surfaced tickets (create, then wire). Graduate fog the answer made specifiable, removing it from Not yet specified. Rule out-of-scope tickets out. Update or delete tickets the decision invalidates.

Resolve one ticket per session. The exception is research tickets: several may be resolved in one session, inline or with subagents when they are independent, and every subagent start counts against the run's shared budget.

Expect other sessions to edit the map concurrently; reload before writing.

## Boundaries

- No branches, pushes, or pull requests for research or decisions.
- No scheduled or recurring sessions; the user starts each session.
- Settled facts and decisions are reused, never re-asked.

## Done

A session is done when its one ticket is resolved, recorded on the ticket and in the map, and the frontier is updated. The map is done when no tickets remain and the way to the destination is clear.

## Provenance

Adapted upstream files, their hashes, and the local changes: [references/SOURCES.md](references/SOURCES.md).
