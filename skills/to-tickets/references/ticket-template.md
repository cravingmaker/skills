# Ticket template

Read this before filing tickets. The local form is parsed by a program, so its field lines are exact.

## Contents

- Local ticket template
- Field rules
- Remote issue template
- Worked example

## Local ticket template

```markdown
# NN: <Ticket title>

**What to build:** the end-to-end behavior this ticket makes work, from the user's perspective, not a layer-by-layer implementation list.

**Spec:** <approved spec path or link>, stories <n, n>

**Blocked by:** <NN, NN> or None

**Status:** ready-for-agent

**Proof:** <surface to drive or source to open> → <result to observe>

- [ ] Acceptance criterion 1
- [ ] Acceptance criterion 2
```

## Field rules

- **Heading:** `# NN: Title`, where `NN` is the file's number. Titles are unique within the feature.
- **Blocked by:** ticket numbers separated by commas (`01, 03`), or `None`. Nothing else: no titles, no "and", no space-only separators, no ticket's own number.
- **Status:** `ready-for-agent` for work an agent can take, `ready-for-human` for work that needs a person. Use the role names; the setup's label mapping applies on remote trackers.
- **Proof:** one line naming the real surface or source and the observable result. "Tests pass" is not a proof of user-visible behavior.
- **Acceptance:** one `- [ ]` checkbox per independently checkable criterion, before any `## Comments` heading. Checkboxes under `## Comments` do not count.
- **Comments:** conversation goes at the bottom under `## Comments`.
- Leave out file paths and code snippets; they go stale. Exception: a prototype snippet that encodes a decision more precisely than prose (a state machine, a reducer, a schema, a type shape), trimmed to the decision and marked as from a prototype.

## Remote issue template

```markdown
## Parent

A reference to the parent issue, if the source was an issue; otherwise omit this section.

## What to build

The end-to-end behavior this ticket makes work, from the user's perspective.

## Proof

<surface to drive or source to open> → <result to observe>

## Acceptance criteria

- [ ] Criterion 1
- [ ] Criterion 2

## Blocked by

#<n>, #<n>, or None. Omit this section when blockers were set as native links.
```

Status on a remote tracker is the label the setup maps to the role.

## Worked example

Three tickets for a saved-searches spec at `docs/specs/saved-searches.md`. A fixture test imports exactly these blocks, so keep each one a valid ticket file.

<!-- ticket-file: 01-save-a-search.md -->
```markdown
# 01: Save a search

**What to build:** a signed-in shopper saves the current search with a name and sees it confirmed.

**Spec:** docs/specs/saved-searches.md, stories 1, 2

**Blocked by:** None

**Status:** ready-for-agent

**Proof:** in the web app as the seeded shopper, search "lamp", save it as "Lamps" → the toast "Saved Lamps" appears and reloading the page keeps it in the saved list

- [ ] Saving stores the query and filters under the given name
- [ ] Saving with an empty name shows "Name required" and stores nothing
```

<!-- ticket-file: 02-list-saved-searches.md -->
```markdown
# 02: List saved searches

**What to build:** a shopper sees their saved searches, newest first, on the account page.

**Spec:** docs/specs/saved-searches.md, story 3

**Blocked by:** 01

**Status:** ready-for-agent

**Proof:** open the account page as the seeded shopper with two saved searches → both names appear, newest first

- [ ] The list shows every saved search for the signed-in shopper only
- [ ] An empty list shows "No saved searches yet"
```

<!-- ticket-file: 03-rerun-a-saved-search.md -->
```markdown
# 03: Rerun a saved search

**What to build:** a shopper opens a saved search from the list and gets its results.

**Spec:** docs/specs/saved-searches.md, story 4

**Blocked by:** 01, 02

**Status:** ready-for-agent

**Proof:** click "Lamps" in the saved list → the results page shows the same products as a fresh "lamp" search

- [ ] Rerunning applies the saved query and filters
- [ ] A saved search whose filter no longer exists runs without it and says so
```
