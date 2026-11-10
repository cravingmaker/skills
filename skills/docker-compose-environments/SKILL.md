---
name: docker-compose-environments
description: Build or fix a Docker Compose environment for local development, CI integration tests or a single-host deployment. Use for startup ordering, healthchecks, profiles, watch rules, ports, persistent volumes or service secrets. Multi-host topology is a separate architecture decision.
license: MIT
compatibility: Python 3.12+ for the read-only normalized-JSON checker; the repository's pinned Docker Compose plugin for rendering and execution.
---

# Docker Compose environments

Deliver a Compose model with explicit readiness, exposure and storage identities, then test the application and its recovery without touching unrelated data.

## Identify the environment

Read every Compose file/override, profile, env-file source, existing check command and application retry contract. Record the Docker context/host, intended purpose, selected services/profiles, project name and persistent volume identities. Choose one explicit project name for each disposable run; a project name alone does not isolate external volumes or host binds.

Check installed Compose help and official [Compose model](https://docs.docker.com/compose/intro/compose-application-model/), [service reference](https://docs.docker.com/reference/compose-file/services/), [startup ordering](https://docs.docker.com/compose/how-tos/startup-order/) and [config command](https://docs.docker.com/reference/cli/docker/compose/config/) at use time. Verify support for `develop.watch`, profiles and the flags the task needs. Omit the obsolete top-level `version` key in authored files; normalized output may have already removed it.

## Build the model

1. Give long-running stateful services a healthcheck that establishes their usable protocol state. Make consumers use `depends_on` with `service_healthy` for those services. Use `service_completed_successfully` for a finite initialization job only when completion is the contract. Keep application retry/reconnect behavior because startup ordering does not ensure continued availability.
2. Scope profiles to optional services and `develop.watch` to development paths. A watch sync must exclude secrets and dependency trees; a runtime-image rebuild and a sync are different updates.
3. Bind development/CI published ports to a loopback address. For a single-host deployment, declare every public service and verify external reachability against that decision. Internal service traffic uses service DNS/container ports, not the host-published port.
4. Use named persistent volumes with deliberate physical identities. Classify each mount as owned disposable, external persistent or host bind. Grant file-based secrets only to their consumers; Compose secrets do not encrypt the source file. Keep credentials outside literal environment values and committed env files.
5. Preserve service users and narrow mounts. A single-host deployment needs digest-pinned images, measured resource bounds, restart/log settings and a recovery/backup owner; CI usually needs no published ports when its runner shares the service network. Moving to Kubernetes remains a separate architecture decision.

## Validate without exposing configuration

Render each shipped combination with `docker compose ... config --quiet` first. Use the same `-f`, project, profile and env options for every later command. Do not use `--no-consistency` to clear a failure.

Pipe normalized output directly to the helper in a private terminal with shell tracing off:

```sh
docker compose -p "$project" -f compose.yaml config --format json |
  python3 <skill>/scripts/check-compose.py - --expected-project "$project" --stateful db
```

Repeat `--stateful` for each stateful service that needs retained data; the script does not guess statefulness from image names. Declare a public service with `--public-service NAME` only after its exposure is agreed. The helper checks normalized shapes, declared stateful readiness/storage, dependency conditions, loopback exposure, volume identities and common credential-valued environment names. It emits indexes/counts and fixed findings, never effective values. Exits are 0 pass, 1 findings and 2 usage/input errors. This heuristic is not a complete secret scan or source-YAML validator, and an observed mount does not prove the data directory uses it.

Treat the full rendered config and interpolation environment as secret-bearing. Do not print either into logs, PRs or reports. If persistence is needed, use a restricted temporary file outside tracked paths and remove it after inspection. Rendering validates a model; it does not contact services or prove readiness.

## Exercise and recover

Read [references/execution-and-storage.md](references/execution-and-storage.md) before any `up`, restart, `down` or volume action. Confirm the Docker context/host, project and mount ownership immediately before mutation. Production effects and traffic changes need explicit task authority; the shipped checker performs no mutations.

On an authorized disposable target, use `up --wait` with a bounded timeout after checking installed help. Assert the real application path, required port exposure and reconnect after a dependency restart. Verify persistent data survives a restart and a stop/start cycle. Deliberately break a healthcheck and prove the bounded readiness gate fails. Clean up only the target's recorded resources.

## Adjacent jobs

For image production, read the `container-image-build` skill when installed. For daemon/host isolation, read the `container-runtime-hardening` skill when installed. For real dependency test semantics, read the `integration-test-harness` skill when installed. Read the selected skill before relying on it; otherwise name the missing method and pass its evidence to the owner. Database schema, migration and backup correctness remain with their respective owners.

## Done

Return the file/profile set, target/project and reviewed storage identities, sanitized validation results, application/readiness/exposure results, restart/recovery evidence and owned cleanup record. Name persistent resources left intact and every check not run. A successful `up` alone does not establish application readiness.
