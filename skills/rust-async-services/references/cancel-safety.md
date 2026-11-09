# Cancellation safety

Read this when work can lose a `select!` branch, time out, disconnect, or stop during shutdown. Check each chosen primitive against the installed [Tokio select documentation](https://docs.rs/tokio/latest/tokio/macro.select.html), not a remembered global list.

Cancellation safety depends on the exact future and how it is recreated. In a loop, ask whether dropping the pending operation and rebuilding it loses bytes, queue position, a permit, or application progress. A cancel-safe receive does not make the business effect after receiving transactional. Distinguish data loss from losing fairness in a wait queue.

| Boundary | Required check |
| --- | --- |
| Read or write loop | Persist partial progress outside a discarded future or use a documented cancel-safe operation |
| Lock or semaphore admission | Check whether recreation loses queue position and whether permits survive the real operation |
| Received message | Keep ownership until commit/acknowledgement, or restore it through durable retry |
| Database transaction | Observe rollback or commit from a separate connection after cancellation |
| Remote write | A dropped future does not prove the provider stopped; verify the key or reconcile |
| Spawned async task | Dropping a handle may leave work running; assign a supervisor and completion policy |
| Blocking closure | Once started it may continue after abort; keep the permit inside it and bound drain behavior |
| Client disconnect | Drive the real HTTP stack through disconnect at a barrier and observe handler/task/resource behavior |

Do not detach must-complete business work merely to avoid request cancellation. Use a durable handoff if completion must survive a process exit. For streaming, test cancellation after partial output and inspect leaked connections and resource counts.

Use barriers or notifications to stop at the critical boundary. A useful bounded-blocking test holds a closure at a barrier, cancels its awaiter, and tries to admit another closure. The second closure must wait until the first releases its permit. Release every test barrier in cleanup so a failed assertion cannot hang the suite.

Sources: [Tokio shared state](https://tokio.rs/tokio/tutorial/shared-state), [spawn_blocking](https://docs.rs/tokio/latest/tokio/task/fn.spawn_blocking.html), [JoinSet](https://docs.rs/tokio/latest/tokio/task/struct.JoinSet.html), and [Axum errors](https://docs.rs/axum/latest/axum/error_handling/index.html). Verify selected versions and server disconnect semantics at use time.
