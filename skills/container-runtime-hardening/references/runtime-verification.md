# Runtime verification

Use this reference before changing a daemon or testing runtime restrictions.

Create a named disposable target within task authority, carrying an ownership label and an exact cleanup list. Confirm the daemon context and host immediately before creating or changing anything. Use inert fixture data, no real host secrets and no real control socket. Never test isolation by attempting an escape on a shared host.

Exercise the app's real user path with its intended UID and writable mounts. Read effective identity, capability masks, `NoNewPrivs` and seccomp state through a supported app/test interface; an inspect flag records requested configuration, not every kernel outcome. Custom profiles need their own content review and rejection test.

For a denied check, attempt a harmless write to an otherwise writable file in the disposable container's read-only root. It must fail because of the mount, not a missing command. Check a deliberately absent fake control-socket path or a fixture permission boundary; never mount a real Docker socket to prove a bad mount is dangerous. If capability enforcement is in scope, choose a harmless fixture operation whose denied error has an independent oracle on the target kernel.

Prove useful work still succeeds with network and resource bounds. Observe restart/recovery without broadening privileges. For rootless or user namespace changes, rehearse storage UID mapping and restore access in the disposable environment before any authorized host migration.

Check intended published-port reachability from an authorized client outside the host. Engine-managed firewall rules can differ from the host firewall front end; reading its rules alone does not establish exposure.

Separate Linux kernel enforcement from a macOS/Windows client or VM claim. Keep the Engine version, kernel/VM identity, custom profile digest and tested image ID in the evidence. Check current limitations in the official runtime documentation.
