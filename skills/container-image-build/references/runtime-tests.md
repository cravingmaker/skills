# Runtime tests

Use this reference before exercising a newly built image.

Record the disposable Docker context, exact image ID/digest, container label/name and cleanup ownership. Test with no host-sensitive bind mounts, no real credentials and no Docker socket. Declare writable tmpfs or volume paths; a root filesystem marked read-only can still contain writable mounts.

Use the production entrypoint and numeric user. Observe the effective UID and filesystem behavior through an existing app diagnostic or an isolated test entrypoint; minimal images may contain no shell, `id` or `curl`. Adding a shell to production merely to run a probe changes the artifact under test.

Exercise a real request or batch result and independently verify its output. Test TLS roots, DNS and native dependencies on each supported platform. Measure startup and readiness against the declared bound.

Send SIGTERM to the production process path in the disposable container. Observe request draining, clean exit within the configured stop timeout and child cleanup. Record the elapsed time and exit status; a forced SIGKILL after timeout fails shutdown even if the container stops. Use an init process when its child-reaping or forwarding behavior is needed, then test that path too.

Check the configured stop signal before using `docker stop` as the SIGTERM test; the image or runtime can override its default. Exit 137 alone does not prove a timeout or OOM: correlate the signal, elapsed time and runtime events.

Run a negative fixture that violates the chosen contract. Keep the expected rejection independent of a test script's own success message. Clean up only the recorded disposable container and its owned storage; never prune a shared daemon.

Sources to check at use time: [Docker run reference](https://docs.docker.com/engine/containers/run/) and [Dockerfile reference](https://docs.docker.com/reference/dockerfile/).
