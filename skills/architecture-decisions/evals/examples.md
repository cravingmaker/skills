# Examples

Run matched examples with and without the final skill only within the coordinator's authorized model budget. These cases are prepared, not executed.

## Activation

- "Audit our accepted ADRs against main; decisions should be superseded, not rewritten." Expect: resolve the configured ADR directory, compare historical reasoning, and report reciprocal-link defects without rewriting records.
- "Compare these two datastores before we commit; exact decimals and recovery after a worker crash decide it." Expect: declare comparable logical inputs and disqualifying precision, concurrency, recovery, and operating cases before trials.
- "Does this data mesh proposal make sense for our ownership model?" Expect: inspect actual domain accountability and compare a simpler platform before recommending the organizational choice.

- "Do we need Iceberg, or are immutable Parquet manifests enough for our nightly exports?" Expect: read the analytical-table adapter, declare the required concurrency, snapshot, engine, and recovery cases, and compare the simplest viable option.

## Near miss

- "Write the already-agreed tenancy decision in our ADR directory." Expect: the `domain-modeling` skill owns the authorized write; no new comparison workflow.
- "Sketch two interfaces for this parser module." Expect: the `architect` skill owns interface alternatives.
- "Review the current service architecture for recovery risks." Expect: the `architecture-review` skill owns system assessment.
- "Make UI-to-database imports fail CI." Expect: the `architecture-fitness-functions` skill owns enforcement.

## Outcome

- "Catch accepted reasoning edits while permitting a valid supersession." Fixture: a Git repository with accepted `docs/adr/0001-store.md` committed at BASE; change its decision paragraph. Expect: helper exits 1. Restore the paragraph, change only status and a successor link, and add `0002-store.md` with the reciprocal predecessor link. The successor is accepted only with user sign-off. Expect: exits 0 against BASE with `--signed-off 2`; without that acknowledgement, new acceptance fails.
- "Keep our short paragraph ADRs." Fixture: `0001-store.md` contains a heading and a paragraph, without lifecycle or template sections. Expect: default audit passes and reports status `recorded`; editing its historical paragraph under `--base` fails. No rewrite or required section is invented.
- "Reject a faster candidate that corrupts precision." Fixture: both candidates receive the same ordered rows containing the string decimal `9007199254740993.01`, null, and explicit units; an independent oracle compares exact values after restart. Candidate A rounds the decimal. Expect: A is disqualified even if throughput is higher; hashes, failure schedule, warm/cold state, and gaps are recorded.
- "Keep acceptance with the owner." Fixture: a one-way datastore choice whose trials pass but with no user sign-off. Expect: evidence and a recommendation are returned; any authorized ADR draft is proposed and no migration runs.

- "Leave a proposed replacement pending." Fixture: accepted `0001-store.md` and proposed `0002-next.md` with `Supersedes: ADR-0001`; the current decision has no successor yet. Expect: the audit passes. Turning 0002 accepted under a trusted base needs sign-off and reciprocal supersession; the agent does not make either change without authority.
- "Compare table semantics before speed." Fixture: two logical writers append disjoint IDs from one fixed dataset; a reader pins a publication manifest or table snapshot while writes continue. An independent expected ID set detects lost updates and mixed snapshots after restart. Test every required engine on the same logical results and recorded warm/cold conditions; unsupported required behavior disqualifies a candidate.
