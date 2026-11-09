# Examples

Run each prompt with and without this skill in a fixture repository with a local tracker in `docs/agents/issue-tracker.md` and an approved spec whose stories carry acceptance and proof. Install `work-decomposition` in both arms. Record the observed behavior against the expectation.

## Activation

- "to-tickets docs/specs/saved-searches.md" Expect: a numbered breakdown for review; after approval, one `NN-slug.md` file per ticket in the configured directory, each with Status, a Proof line, checkboxes, and `Blocked by:` numbers or None.
- "Split the approved export spec into tickets. Renaming the `customer_id` column touches every service." Expect: an expand, migrate batches, and a contract ticket; the contract names the compatibility obligation for external API clients.

## Near miss

- "Write a spec from what we discussed." Expect: the `to-spec` skill; no tickets.
- "Plan how three agents should build these approved tickets." Expect: the `work-decomposition` skill imports the tickets; no new tickets are written.
- "Implement ticket 02." Expect: implementation of that ticket, not a new breakdown.

## Outcome

- The worked example in `references/ticket-template.md` imports with `import-tickets.py --spec`, carrying titles, status, Proof, acceptance, and blockers exactly (`tests/to-tickets/run.sh`).
- Every filed `Blocked by:` line is `None` or comma-separated existing ticket numbers, and `import-tickets.py` reports no `FAIL` lines for the filed directory.
- The parent issue and the spec are unchanged, and no implementation or run plan is started.
- Filing happens only at the destination the tracker setup names; without setup, the tickets come back as drafts.
