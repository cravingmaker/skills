# Resources and rollout

Use this reference for requests/limits, scaling, rollout capacity or disruption changes.

Compare measured demand, startup peaks, memory working set, CPU throttling and scheduling headroom. Requests affect scheduling and some HPA metrics. A memory limit can cause an OOM; CPU limits can throttle. Decide CPU limits from measurements and platform policy instead of universally adding or removing them. Keep quota, LimitRange defaults, init containers and sidecars in the effective calculation.

Check the selector against Pod-template labels and Service selectors/target ports against the rendered workload. Topology spread requires eligible failure domains and spare capacity. A valid constraint with no feasible placement can strand replacements.

Review rollout surge/unavailability with available capacity and storage attachment constraints. A PDB constrains eligible voluntary evictions; it does not replace Deployment rollout settings or prevent every disruption. A zero-disruption budget can block maintenance. Test an allowed eviction through the eviction API on an authorized disposable target, plus the denied case where availability is insufficient.

`ProgressDeadlineExceeded` is failure detection, not automatic rollback. Preserve a known artifact/config and decide recovery before install. Under GitOps, change desired state or use the owner's authorized suspension/reconciliation procedure so the controller does not undo recovery.

Sources to check at use time: [Resources](https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/), [Disruptions](https://kubernetes.io/docs/concepts/workloads/pods/disruptions/) and [Deployments](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/).
