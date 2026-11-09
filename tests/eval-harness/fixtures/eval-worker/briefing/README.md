# Migration QA brief context

Task QA-1: prepare (do not dispatch) a fresh QA agent to verify the active->status migration. Contract: contracts/status.json revision status-v2. Read backend/service.py, frontend/client.py, tests/test_contract.py. Source has not yet been migrated. Command ./scripts/validate.sh currently fails; no claim of readiness is authorized. QA reads the whole fixture but may write only reports/qa-migration-r1.md; no other repository edits, no deployment, network, credentials, commits, or delegation. QA is a leaf with one verification pass and must return PARTIAL/BLOCKED for unavailable checks. No role/capability skill beyond the current installed inventory is assumed; report missing required inputs. The coordinator owns all shared logs.

User constraints lost from the old brief: status strings must remain exactly active and paused; a paused account must never show Active; schema edits are forbidden. Open decision: product owner must decide copy for unknown status; do not guess it or add unknown to the schema. For the repair task, update delegation-brief.md using this context. Input hashes can be computed locally. Report needs actual commands, outputs, source/output revisions, loaded skills, assumptions, unresolved claims, decisions, and usage or unknown.

No commits or pushes are permitted, including in temporary repositories.
