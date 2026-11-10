# Injection, caches and artifacts

Read this when untrusted values reach shell/AI steps or privileged inputs.

For shell fixtures, use a literal value such as `$(touch marker)` in a disposable local directory.
Run the actual step with that value as an environment variable; compare its captured output byte for byte and require that `marker` was not created.
Keep filenames and values as data through every later transformation.
Inspect writes to `$GITHUB_ENV`, `$GITHUB_PATH` and `$GITHUB_OUTPUT` as downstream command and environment inputs.
Use the platform's current multiline encoding for permitted values; raw untrusted newlines must not create extra entries.
Static matching for a removed expression alone does not prove that a downstream script avoids command construction.

An AI instruction to ignore hostile input is advisory text.
Constrain the AI job's token, secrets, checkout credentials, tool access and network reach; send proposed write operations through a trusted maintainer decision.
Review dispatches, generated workflows, PR modifications and artifact handoffs as write paths.
Use inert requests such as creating a synthetic marker in the fixture and assert that the unprivileged job cannot perform the privileged operation.

For cache fixtures, model the low-trust producer and release consumer separately.
A producer allowed to write a key that the privileged job restores is a crossing even when the key includes a lockfile hash.
Inspect broad restore keys, setup actions, post steps, and platform-specific cache-token overrides.
Keep release and publication jobs free of cache restores and verify correctness from a cold cache.

For artifact fixtures, change bytes while keeping the display name constant and require rejection before execution.
Repeat with a different producing repository/workflow/source SHA and an attacker-supplied matching checksum.
The expected digest must arrive through an authenticated trusted path; a checksum beside untrusted bytes cannot supply that trust.
Extract into a fresh directory only after verification; reject path traversal and unsafe links before a privileged consumer accesses files.
