# Examples

Run matched prompts with and without the final skill before changing evaluation status. These cases are prepared, not model-evaluated.

## Activation

- "Why is this Pod Pending? Start with read-only evidence in the staging namespace." Expect target/UID binding and a probe that separates scheduling, storage and node hypotheses.
- "This container exited 137 and is in CrashLoopBackOff; what should we inspect next?" Expect an unknown SIGKILL cause until OOMKilled or supporting runtime/node evidence appears.
- "Our Deployment is stuck and the Service has no working endpoints; diagnose it without restarting anything." Expect replica/condition, selector and EndpointSlice evidence, with no implied automatic rollback.

## Near miss

- "Write a new Kustomize overlay and tune Pod probes." Expect the `kubernetes-workloads` skill.
- "Fix the application parser crash after the cluster evidence shows a code defect." Expect the `diagnosing-bugs` skill.
- "Fix an image's wrong architecture and missing entrypoint." Expect the `container-image-build` skill once diagnosis has identified the image cause.
- "Design cluster-wide CNI policy or least-privilege RBAC." Expect the cluster/security owner.
- "Rehearse a rollout undo and document what it cannot recover." Expect the `release-rollback-planning` skill.
- "Run the installed engineering plugin's deploy-checklist before launch." Expect a release checklist without a speculative cluster investigation.
- "Run the installed engineering plugin's incident-response; users cannot check out." Expect incident coordination; diagnosis can be an explicitly scoped branch, not a substitute for impact management.

## Outcome

- "Distinguish kill evidence from OOM attribution." Fixture: `tests/kubernetes-troubleshooting/fixtures/snapshot.json`; set one container's lastState.terminated to exitCode 137, reason Error. Expect `exit-137-cause-unknown` and no `oom-reported`; switching reason to OOMKilled must produce `oom-reported`. A running Pod alone must not be declared service health proof.
- "Ignore a stale same-name Pod event." Fixture: the current Pod UID is pod-current; append a FailedScheduling event for the same name with UID pod-old and a secret marker in its message. Expect the event to be counted as ignored and no scheduling signal; changing UID to pod-current produces a resource/taint/PVC hypothesis without echoing the message.
- "Keep selector matching and endpoint readiness separate." Fixture: move the selected Pod to another namespace, then independently set the matching EndpointSlice ready condition false or omit the slice. Expect the appropriate selector/no-ready-endpoint/endpoints-not-observed signals without inventing connectivity evidence. Null or omitted ready follows the API's true interpretation and does not create the no-ready-endpoint signal.
- "Classify observed startup and infrastructure failures without printing event text." Fixture: independently set waiting.reason to CreateContainerConfigError or RunContainerError, then append a current-UID event with FailedMount, FailedCreatePodSandBox or Unhealthy and a synthetic private marker in its message/note. Expect fixed configuration/runtime/mount/sandbox/typed-probe labels, with no marker. Replacing the event's Pod UID with an old UID must ignore it in both core and events.k8s.io shapes.
- "Treat a deployment deadline as detection." Fixture: add a Deployment with Progressing False and ProgressDeadlineExceeded. Expect a replica/Pod/controller probe label, no kubectl undo/delete command and no claim that the platform restored service. An empty List must report missing Pod evidence; malformed JSON exits 2 without input values.
