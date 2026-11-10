# Examples

Run matched prompts with and without the final skill before changing evaluation status. These cases are prepared, not model-evaluated.

## Activation

- "Add Postgres to this local Compose setup and make the app wait for it to be usable." Expect a stateful healthcheck, service_healthy dependency, app retry behavior and bounded readiness proof.
- "Our CI Compose tests collide with local containers and delete the wrong volumes; fix the identities and cleanup." Expect explicit project and physical storage ownership before lifecycle commands.
- "Review this single-host Compose deployment's ports, profiles, watch paths and file-based secrets." Expect rendered-variant checks and declared exposure without printing effective configuration.

## Near miss

- "Rewrite the Dockerfile to remove build dependencies." Expect the `container-image-build` skill.
- "Audit rootless Docker, capabilities and seccomp on the host." Expect the `container-runtime-hardening` skill.
- "Design multi-host failover for this service." Expect an architecture decision, not an automatic Compose rewrite.
- "Test PostgreSQL transaction isolation with real concurrent connections." Expect the `integration-test-harness` skill and the database owner; Compose can supply a dependency but does not own the oracle.
- "Run the installed engineering plugin's deploy-checklist for our release." Expect a release checklist without unrelated Compose changes.
- "Run the installed engineering plugin's incident-response for production downtime." Expect incident coordination; do not start or tear down environments merely to follow a checklist.

## Outcome

- "Validate this environment without disclosing resolved values." Fixture: `tests/docker-compose-environments/fixtures/config.json`; project fixture, healthy db, service_healthy consumer, loopback app port and named fixture_data volume. Expect exit 0, stable counts and no configuration dump. Inject API_TOKEN and DATABASE_URL with a synthetic marker; expect exit 1 without either key or value.
- "Reject startup and exposure mistakes." Fixture: remove/disable db healthcheck, change its consumer condition to service_started and remove the port host_ip. Expect stateful readiness/ordering and public-port findings; an agreed explicit public-service declaration clears only that exposure finding.
- "Keep cleanup tied to physical ownership." Fixture: an owned disposable project with one shared external volume and one owned volume. Expect no volume-removal command covering the shared volume; identify both privately and leave uncertain resources intact. An otherwise unique project name must not count as proof that external data is disposable.
- "Reject a stateful service that mounts no persistent storage." Fixture: remove db.volumes from config.json while retaining its unused top-level data volume, then use only a tmpfs mount. Expect stateful-storage in both cases; a reviewed named volume or host bind clears that finding, without claiming the app writes to it.
- "Prove readiness, reconnect and persistence." Fixture: a disposable app and database, a unique record as an independent oracle and a bad healthcheck variant. Expect bounded startup success and bad-healthcheck failure, app reconnect after a dependency restart and exact record readback after stop/start; report any test not run.
