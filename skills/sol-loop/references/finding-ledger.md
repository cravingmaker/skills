# Finding ledger

Keep this information in the existing authoritative run record, not a second log.

| Field | Meaning |
| --- | --- |
| ID | Stable root-cause ID, such as F-001, retained across rounds and wording changes. |
| Axis and severity | Standards or Spec, and actual impact; retain cross-axis references where relevant. |
| Scope identity | Pinned base, reviewed head/content hashes, affected path and caller. |
| Claim and evidence | Trigger, actual versus expected result, source or command, evidence class and artifact locator. |
| State | Open, fixed-awaiting-recheck, resolved, disputed, deferred, or withdrawn. |
| Transition | Round, reason, authority where required, and new evidence. |
| Required probe | Exact pending question/action, owning seat, and why it remains unrun or inconclusive. |

Before assigning a new ID, compare the cause and affected invariant with existing IDs. If two IDs describe one cause, retain one canonical ID and an alias link; their history and budget remain intact. An edited implementation can invalidate a prior resolution without creating a new ID or resetting rounds. Mark a fix resolved only after applicable evidence covers the current artifact; an implemented fix awaiting proof remains pending. Record a scope withdrawal or accepted deferral explicitly; neither is a successful proof or a clean full-scope verdict.

For a panel, retain each seat's actual provider identity, finding evidence, and dissent, including unavailable seats. Keep disagreement visible until evidence resolves it or authorized scope changes it. Scores and agreement counts may describe feedback if actually supplied; they do not close a finding.

On resume, reconcile the stored base/content identities, prior effects, remaining rounds/starts, and active run IDs before launching anything. A missing or stale record is a gap to reconcile, not a fresh budget.
