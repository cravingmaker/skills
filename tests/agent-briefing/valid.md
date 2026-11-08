# Worker brief

## Task identity

fixture-run / inspect-contract / revision 1 / coordinator.

## Goal

Determine whether the recorded schema covers the three required errors.

## Context

The accepted requirement is /workspace/spec.md at recorded hash abc.

## Workspace

/workspace/project, base commit recorded in PLAN.md; no uncommitted input is required.

## Scope

Inspect the response schema and error requirements; exclude implementation.

## Constraints

Read /workspace/project/AGENTS.md first; preserve source values.

## Permissions

- Read: /workspace/spec.md and /workspace/project/schema.json.
- Write: Only /workspace/run/raw/inspect-r1.md.
- External actions: None; source inspection requires no external changes.

## Write boundary

Own /workspace/run/raw/inspect-r1.md; repository writes and shared-ledger writes are excluded.

## Role skill

None: this is bounded source comparison, without a role router.

## Capability skills

None: the supplied schema and acceptance command define this bounded inspection.

## Communication

Lead with the result, preserve source facts, use plain words and sufficient detail, inspect before asking, batch consequential questions, state reversible assumptions, and focus on the uncertain part.

## Terminology

An error is one of the three named conditions in the source specification.

## Open decisions

None: the accepted specification fixes the conditions.

## Dependencies

Use the frozen schema at the hash recorded in the plan; no active predecessor remains.

## Acceptance

Each required error has a schema case or an explicit evidence-backed gap.

## Evidence standard

Cite each source location; run the supplied checker if available; distinguish static evidence from executed evidence and hypotheses.

## Return contract

- Result first: COMPLETE, PARTIAL, or BLOCKED and the result.
- Evidence: Source paths and locations with evidence class.
- Artifacts and revisions: Input hashes and report path; skills actually loaded.
- Commands and results: Actual commands and outcomes; omissions with reasons.
- Unresolved claims: Remaining evidence gaps or none.
- Decisions needed: Required owner decision or none.
- Assumptions and surprises: List any assumption, deviation, or none.
- Usage: Measured receipt or unknown.

## Raw report path

/workspace/run/raw/inspect-r1.md

## Budget

Delegation: no
Stop after: One inspection and one check attempt; return unresolved evidence if unavailable.

## Stop conditions

Return a missing prerequisite, revision mismatch, or exhausted allowance; continue only independent authorized inspection.
