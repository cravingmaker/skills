# Explicit learning workspace

Read this only after the user asks for durable lessons, a curriculum, or saved progress. Paths below are relative to the user-selected learning workspace, not this skill folder. Inspect existing files and conventions first, preserve their contents, and create artifacts only as needed.

## Mission and level

Reuse the learner's stated goal, constraints, and prior knowledge. Ask only for a consequential gap before writing a mission. Keep one coherent mission per workspace; discuss a separate location for unrelated topics. Tie lessons to an observable goal rather than a generic wish to understand the topic. Confirm a consequential inferred mission change with the learner; apply an explicit requested change directly.

Use MISSION.md for the goal:

```md
# Mission: {Topic}
## Why
{Concrete real-world outcome.}
## Success looks like
- {Observable ability.}
## Constraints
- {Time, budget, prior knowledge, learning preferences.}
## Out of scope
- {Adjacent topic the learner excludes.}
```

Choose the next tightly scoped lesson from the mission and demonstrated understanding. Keep the challenge within reach while providing a concrete win. Separate immediate fluency from durable retention; exposure alone establishes neither mastery nor long-term storage. When the learner chooses practice, retrieval, spacing, and interleaving can support the agreed plan without becoming mandatory ceremonies.

## Trusted resources

Use RESOURCES.md as a curated set of high-trust primary sources and useful practitioner resources. Annotate each link with its coverage and when to use it; separate knowledge sources from optional communities. Retain a Gaps section for missing or inaccessible evidence and preserve a preference to avoid community suggestions. Remove or mark an off-mission, superseded, or unreliable resource instead of accumulating stale recommendations. Learning explanations still distinguish established facts, source limits, and inference.

```md
# {Topic} resources
## Knowledge
- [{Primary source}]({URL}) — {What it covers; when to use it.}
## Communities
- {Only if useful and wanted; purpose and access limits.}
## Gaps
- {Mission need without a trustworthy source.}
```

## Lessons, references, and reusable assets

When lessons are requested, use sequential `lessons/0001-topic.html` files or the user's established format. Keep each lesson short, readable, tied to one goal, and grounded in the best relevant sources. Link related lessons and compact reference material rather than repeating it. Reuse existing styles, widgets, and assets when they fit; extract shared components when reuse warrants it rather than building a framework first. For HTML, use supported local assets and verify rendering through the requested or existing preview method; state any network dependency. Opening an app or browser follows task authority and host capabilities rather than an automatic CLI launch.

Quizzes, exercises, and feedback follow the learner's explicit preference or agreed plan. When requested, use an informative feedback loop, plausible options without formatting clues, and varied correct-answer positions. Do not force exact answer lengths at the expense of clarity. Keep NOTES.md only when it usefully records stated teaching preferences or working notes within this requested workspace.

## Learning records

Create `learning-records/` lazily and use the next available sequential number, such as `0001-topic.md`. Capture a non-obvious insight, stated prior knowledge and its depth, corrected misconception, or mission shift that changes future teaching. Record evidence of demonstrated understanding separately from self-reported prior knowledge; material merely covered earns no learning claim. Use a short title and one paragraph explaining what is known and why it changes the next lesson. Add evidence, implications, or status only when useful. Keep earlier records and mark a superseding record when understanding changes; avoid a session activity journal.

## Learner vocabulary

Keep a learner glossary under a learning-specific path such as `reference/GLOSSARY.md` unless the workspace already supplies a separate location. It records concepts the learner can use, with short definitions, useful aliases, and explicit ambiguity notes. Reuse its terms consistently and refine definitions as understanding grows. A project semantic glossary remains authoritative for project terms; link to it without overwriting it or declaring learner aliases to be project policy. Avoid duplicating a terse glossary definition as a learning record.

Done when the agreed artifacts support the mission, preserve the learner's preferences, distinguish exposure from evidence, and identify the next agreed lesson without claiming unobserved mastery.
