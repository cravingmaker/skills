# Reusable workflow contracts

Read this when creating a reusable workflow or composite action.

Choose a composite action for steps sharing the caller job's runner and authority.
Choose a reusable workflow for a job interface with its own runner jobs and explicit inputs, outputs, secrets and permission ceiling.
Neither packaging choice alone establishes an isolation or SLSA level.

Declare input types and defaults, validate an artifact digest and destination, and reject arbitrary command strings in privileged callers.
Pass named secrets rather than broad inheritance when possible.
Check current GitHub rules for nested calls, environment secrets, permissions and supported call-job keys before editing.
Remote reusable calls use a live-resolved full commit SHA; inspect local called workflows at the caller's source SHA.
Preserve the repository's supported caller interface or migrate every caller in the same change.

Test a representative caller, invalid input, a denied authority case and output propagation.
Obtain actual called check names from a hosted run before changing required contexts.
