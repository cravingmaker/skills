# Examples

These cases are prepared for paired runs with and without the skill; no model runs are claimed.

## Activation

- "Act as a devops-engineer and get this failed CI check diagnosed." Expect: read the router and fix-ci body, bind current-head failure evidence and preserve task authority.
- "Equip this agent as a DevOps engineer for a release that includes a PostgreSQL major upgrade." Expect: read postgres-version-upgrades plus relevant release and rollback methods; do not substitute a schema migration.
- "Act as a DevOps engineer to make our service observable and recoverable." Expect: route instrumentation conditionally to backend, then objectives, alert rules and runbooks.

## Near miss

- "Write a portable shell script." Expect: shell-scripting directly; no role-router activation.
- "Use the engineering plugin deploy-checklist for launch approval." Expect: the requested engineering:deploy-checklist entry; no role invocation.
- "Use the engineering plugin incident-response for incident command." Expect: the requested engineering:incident-response entry; no role invocation.
- "What does a DevOps engineer do?" Expect: explanation, not equipping a role or starting tools.

## Outcome

- "Route CI aliases without a duplicate package." Fixture: catalog contains fix-ci with searchable aliases ci-failure-triage and ci-failure-diagnosis. Expect: router requires fix-ci, reads it for red CI and creates no ci-failure-triage folder.
- "Stop the unavailable flow precisely." Fixture: remove one required method such as kubernetes-workloads from the installed role inventory and ask for that job. Expect: name the missing method and stop that flow rather than inventing a third-party replacement.
- "Return evidence after an authorized change." Fixture: workflow/image/manifest/plan change has a source revision, explicit target and candidate digest; one relevant hosted check cannot run. Expect: static outputs, negative fixture, effects, undo limitations, authority and the exact unrun check are reported separately.

- "Keep folded jobs searchable." Fixture: the catalog maps shell-script-testing to shell-scripting and postgres-incident-triage to runbook-authoring. Expect: those references load for their bounded jobs, with no duplicate folder or required edge; live incident coordination remains with the incident lead.
