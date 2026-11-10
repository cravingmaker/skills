# Execution and storage

Use this reference before a Compose lifecycle command or cleanup.

Record the exact Docker context, file set, env-file sources, profiles and project name. Carry them unchanged through validation, startup and cleanup. Confirm context/host, project and storage again immediately before mutation. A fixed `container_name`, external network, explicit shared volume name or host bind can collide across project names; remove that coupling from disposable fixtures.

Inspect top-level volume declarations and resolved engine volume labels privately. Confirm which physical volumes the selected services will mount. A top-level `name` or `external` volume may outlive the project; neither is a disposable-cleanup grant. Record existing data and its recovery owner before single-host changes.

Use `up --wait` only with a tested healthcheck or an independent application probe for each required service. Bound the wait and record the failing condition. Dependency restart propagation options do not replace retry logic or independently prove recovery from a crash.

Check the health command in the pinned image, including its exit behavior. For the official PostgreSQL image, a TCP readiness check avoids accepting the socket-only temporary initialization server; verify that behavior in the image's [entrypoint source](https://github.com/docker-library/postgres/blob/master/docker-entrypoint.sh). `pg_isready` alone does not prove the application's credentials, schema or queries work. Escape container-side variables as `$$` in Compose commands, and test the actual application capability after startup.

Use a unique fixture record as the persistence oracle. Create it only in an authorized disposable service, restart the dependency, verify reconnect, then stop/start the environment and read the record back. A volume existing after restart does not prove the data contract.

Default cleanup stops/removes only the recorded disposable project's containers and networks. Use `down -v` only when every selected volume is explicitly owned by this disposable run and the task authorizes its removal. Refuse volume removal if identity or ownership is uncertain. Never use global container, system or volume prune as project cleanup. Cleanup failure remains a reported resource with an owner.

A single-host deployment needs tested backups and a restore procedure from its storage/database owner. Restart policies improve process recovery; they do not provide host redundancy.

Sources to check at use time: [Compose volumes](https://docs.docker.com/reference/compose-file/volumes/), [Compose secrets](https://docs.docker.com/compose/how-tos/use-secrets/) and [Compose down](https://docs.docker.com/reference/cli/docker/compose/down/).
