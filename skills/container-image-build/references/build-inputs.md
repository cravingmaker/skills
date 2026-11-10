# Build inputs

Use this reference for private dependencies, caches and native build compatibility.

Keep the repository's package manager and lockfile format. Discover its frozen or locked install command from the installed tool and project policy; a successful install that rewrites the lockfile fails this contract. Separate build dependencies from the final runtime graph.

Resolve base digests with a registry-aware tool such as `docker buildx imagetools inspect` or `crane digest`, after checking installed help. Record the platform when resolving a manifest from a multi-platform index. Resolve image/tool identities live; these instructions supply no remembered versions or hashes.

Include external images used by `COPY --from` and the Dockerfile frontend in the build-input inventory. A cache-mounted output directory is not retained in the build layer; copy the finished artifact outside that mount in the same build step.

| Runtime | Check before copying into the runtime stage |
| --- | --- |
| Node | Preserve the package manager version and production dependency graph; native addons need a compatible Node ABI and libc. |
| Python | A copied virtual environment must still resolve its interpreter at the expected path; match the Python base and native libraries. |
| Go | Verify whether cgo is in use before choosing a static runtime base; test the declared architecture. |
| Rust | Inspect the final binary's linked libraries before selecting a static or `cc` runtime image. |

A secret mount keeps the input out of image metadata only if the build command does not copy or log it. Check package-manager configuration, downloaded URLs and exported caches for credentials. Keep authenticated and untrusted cache writers apart. Inspect history and final filesystem contents privately; publish a count or finding, never raw history or secret values.

Use an inert credential canary only in an owned disposable fixture. Search all retained layers and exported build outputs for that canary; deleting a file in a later layer does not remove earlier bytes. Keep this credential test separate from a scanner's vulnerability report.

Test native modules against the runtime libc and architecture. A cross-platform build under emulation establishes build progress, not native startup performance or host compatibility. Exercise a native target where required and name emulation in the record.

Sources to check at use time: [Docker build practices](https://docs.docker.com/build/building/best-practices/), [BuildKit secrets](https://docs.docker.com/build/building/secrets/) and [Build checks](https://docs.docker.com/build/checks/).
