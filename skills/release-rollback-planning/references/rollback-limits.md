# Rollback limits

Read this while filling `irreversible_effects` and the schema state. Each row is a question to answer for the release; any "yes" goes into the plan with its handling.

## What a rollback does not undo

| Question | Typical handling |
| --- | --- |
| Does the candidate write data in a new shape or a new column? | Keep the old code able to read it (expand first); never drop or rewrite until the next release |
| Does it delete, rewrite or backfill rows? | Treat as irreversible; restore from backup loses writes made since, so it is a recovery, not a rollback |
| Does it contract the schema (drop, rename, tighten a constraint)? | Prove whether old code uses the removed contract; if incompatible, use a compatible roll forward or defer contraction |
| Does it send emails, push notifications, SMS or webhooks? | Cannot be recalled; prepare support or compensating messages |
| Does it call external services with side effects (payments, provisioning)? | Reconcile with the provider; idempotency keys keep retries safe |
| Does it publish to a queue or topic other services consume? | Old consumers must accept the new messages, or the producer change waits |
| Does it change a cache, session or token format? | Old code must read the new format, or caches are flushed as part of rollback |
| Does it ship a client build (mobile, desktop, CDN assets)? | Installed clients stay; the server must keep serving them |
| Does it change DNS, certificates or load balancer routes? | Propagation and TTLs delay the undo; measure them in the drill |
| Does it rotate credentials or change permissions? | The previous version may no longer authenticate; verify a supported current credential delivery path; never restore a revoked credential |
| Does it change feature flags or remote config? | Record the previous flag state as part of the config to restore |

## Schema phases

Expand, migrate, contract: add the new structure while the old code still works (expand), move data and switch readers (migrate), then remove the old structure in a later release (contract). Rollback stays available through expand and migrate only while the previous code still runs on the schema. Use the `postgres-migrations` skill, when installed, to sequence the phases and prove mixed-version compatibility; this plan only records which phase the release leaves the database in.

## Delivery mechanisms

- **Push (CI deploys, `kubectl`, `helm`).** A rollback command redeploys the previous digest. Confirm the previous release record still exists (for example `helm history`, `kubectl rollout history`) and that it references the digest, not a mutable tag.
- **GitOps (Argo CD, Flux).** The controller reconciles the cluster to Git. Rolling back in the cluster while auto-sync is on gets reverted; revert in Git, or suspend reconciliation first and restore it afterward. Check the controller's current documentation for its rollback command and its auto-sync interaction.
- **Progressive delivery (canary, blue-green).** Aborting the rollout is the rollback; the drill must exercise the abort, not only a full redeploy.

## Measuring the drill

Time from the first rollback command to the previous version serving user traffic, including controller sync, image pulls on cold nodes, cache warm-up and DNS. Record the slowest component. A drill on an empty staging cluster underestimates production; say so when traffic, data volume or node count differ.

## Primary references

At use time check the deployed controller's official rollback and synchronization documentation, including [Argo CD automated sync](https://argo-cd.readthedocs.io/en/stable/user-guide/auto_sync/), and the installed PostgreSQL major's [transaction](https://www.postgresql.org/docs/current/tutorial-transactions.html) and [sequence](https://www.postgresql.org/docs/current/functions-sequence.html) behavior. [Google SRE release engineering](https://sre.google/sre-book/release-engineering/) and [canarying releases](https://sre.google/workbook/canarying-releases/) are method references; this text is original.
