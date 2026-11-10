# Probes and shutdown

Use this reference when changing startup, health endpoints or termination.

Write the endpoint contract with the application owner. Readiness removes an instance from eligible traffic while liveness restarts an unhealthy process. A database outage can make readiness fail without making process restart useful. Test that outage and confirm the liveness endpoint still follows its local-process contract.

Measure startup before choosing startup-probe thresholds. A startup probe delays the other probes until it succeeds. Give each check a bounded timeout and measure its cost; identical expensive health queries across many replicas can amplify an outage.

Budget shutdown end to end: endpoint removal/connection propagation, `preStop`, signal handling, draining and child cleanup. The grace timer includes the hook; a long sleep does not extend it. Test real in-flight work and its result through the production entrypoint. Observe whether the process exited cleanly or was killed after grace.

Service readiness, a green rollout status and a passing HTTP probe are different observations. Assert a user path and the workload's independent result before concluding service recovery.

Sources to check at use time: [Probe configuration](https://kubernetes.io/docs/tasks/configure-pod-container/configure-liveness-readiness-startup-probes/) and [Pod lifecycle](https://kubernetes.io/docs/concepts/workloads/pods/pod-lifecycle/).
