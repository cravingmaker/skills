# Evidence matrix

Read the branch that matches the observed signal. Commands use the already confirmed explicit context and namespace; captures stay private.

| Signal | Next discriminating evidence | Do not infer |
| --- | --- | --- |
| Pending with FailedScheduling | Describe the Pod and its assigned constraints; compare requests, allocatable capacity, taints/tolerations, affinity/topology and quota; inspect PVC phase/events where named. | More nodes will fix every scheduling constraint. |
| Waiting with ContainerCreating | Inspect Pod events, volume attachment/binding and node/runtime conditions. | Pending always means insufficient CPU. |
| ImagePullBackOff or ErrImagePull | Inspect the pull error, source digest/platform and registry access path without reading or printing credentials. | The image is missing before distinguishing authorization, TLS and network failure. |
| Configuration or runtime start error | Check referenced ConfigMap/Secret key existence without values; compare image entrypoint, architecture, permissions and node runtime. | Every startup failure is a registry error. |
| CrashLoopBackOff | Compare current/last termination reason, restart count, previous bounded logs and startup/probe events. | Retry backoff is the root cause. |
| Explicit OOMKilled reason | Correlate container limits/usage, node memory pressure, timestamps and runtime/node evidence. | Every memory problem is fixed by raising a limit. |
| Exit 137 without OOMKilled | Check termination reason, kill/timeout evidence, eviction, node/runtime events and memory evidence. | SIGKILL establishes an OOM. |
| Probe failure | Identify probe type, endpoint, port, timeout and timing; reproduce the endpoint's contract through an authorized test path. | A transient dependency failure warrants liveness restarts. |
| ProgressDeadlineExceeded | Inspect the Deployment condition, replica counts, ReplicaSets, new Pods, capacity and delivery-controller state. | The Deployment controller automatically rolls back. |
| No ready Service path | Compare selector to Pod labels, EndpointSlice service labels/ready conditions and Service target ports. | Label-selected Pods guarantee an endpoint or a working network path. |
| DNS failure | Check service/namespace spelling, available endpoints and resolver configuration before an authorized DNS probe; inspect the target CNI and policy facts. | A client timeout proves a DNS defect. |
| Mount, sandbox or eviction event | Correlate the current Pod UID with PVC/provisioner/attachment, node pressure, runtime and CNI evidence. | Restarting the application repairs node or storage faults. |

A bare `Failed` condition, no Pod status or an empty resource list leaves missing evidence. Keep an old warning event distinct from current state. Select events with the current Pod UID; same-name events from an older Pod do not establish the new Pod's cause. Event retention and metrics availability vary, so record the capture time and missing interval.

The EndpointSlice API treats omitted or null `ready` as true; false is explicit unready evidence. `publishNotReadyAddresses` and terminating-endpoint handling can change routing, so observed API readiness still needs an application-path check. Verify the target's [EndpointSlice API](https://kubernetes.io/docs/reference/kubernetes-api/discovery/endpoint-slice-v1/) before interpreting those fields.

Sources to check at use time: [Debug Pods](https://kubernetes.io/docs/tasks/debug/debug-application/debug-pods/), [Pod lifecycle](https://kubernetes.io/docs/concepts/workloads/pods/pod-lifecycle/), [Debug Services](https://kubernetes.io/docs/tasks/debug/debug-application/debug-service/) and [Deployment conditions](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/).
