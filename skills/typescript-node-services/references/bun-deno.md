# Bun and Deno targets

Read this only when the deployment runtime is Bun or Deno. This is a target-verification branch, not a claim that either runtime behaves identically to Node.

Read the repository's lockfile, runtime configuration, deployment image, and entry command. Check the installed runtime's official documentation for TypeScript handling, module resolution, Node API compatibility, permissions, environment loading, test behavior, and cancellation/shutdown APIs. Use [Bun documentation](https://bun.sh/docs) or [Deno documentation](https://docs.deno.com/runtime/) for the actual target.

Run the separate compiler check even when the runtime executes TypeScript. Test the packaged or emitted deployment entry with that runtime, including invalid configuration, import resolution, dependency compatibility, real I/O cancellation, and termination. Retain the project's selected package manager and lockfile unless changing them is authorized. The Node smoke helper deliberately invokes Node; create or use the project's target-specific smoke test for a Bun or Deno deployment.

If the service must support several runtimes, list the supported targets and run the same observable contract on each. A passing unit suite on one runtime is not evidence for another.

Replacing a deployed runtime is a hard-to-reverse choice. Use the `architecture-decisions` skill when installed to compare options, keep any ADR proposed, and obtain user sign-off before adopting the replacement.
