# Events and caches

Read this when changing event filters or cache behavior, or mapping a non-GitHub pipeline.

A required workflow skipped by a path or branch filter can leave a required context pending.
Prefer an always-reported gate whose job logic decides whether work is needed; verify its treatment of skipped, cancelled and failed dependencies.
Manual and reusable entry points need explicit input validation and the same destination protections as automated release jobs.

Cache keys describe OS, architecture, toolchain, lockfile and configuration that affect validity.
Prefer download caches validated by lockfile integrity; a restored executable is an untrusted input.
Check setup actions for implicit caches, broad restore keys and cache-save behavior.
A cold-cache run must still succeed.
Publication and release jobs restore no caches; transfer exact verified artifacts from build jobs instead.

For GitLab, apply the same source/identity/secret/artifact matrix to job ID tokens, includes and protected environments using current GitLab docs.
For Jenkins, inspect controller/agent authority, plugin maintenance and credential boundaries using its current security handbook.
These comparisons transfer the trust model and do not validate another CI system's syntax.
