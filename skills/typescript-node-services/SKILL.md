---
name: typescript-node-services
description: Build or repair a Node TypeScript service so its deployed entry matches what was checked. Use for a new server, emitted ESM import errors, invalid startup configuration, event-loop stalls, or cancellation and lifecycle bugs. Browser bundles and tooling upgrades are separate jobs.
license: MIT
compatibility: Python 3.12 or later and a POSIX host for the optional built-entry smoke helper; the caller supplies the deployment Node executable.
---

# TypeScript Node services

Prove the service's checked source becomes an artifact that imports or starts on its actual deployment runtime.

## Bind source to deployment

Read package scripts, lockfile, package `type` and `exports`, compiler configuration, runtime image, and deployed entry. Use the project's package manager and locked compiler/linter versions. For native Node module resolution, align `module` and `moduleResolution` with Node-aware modes such as `nodenext`. Use bundler resolution only when that bundler builds the deployed server. Check emitted import extensions and package exports; TypeScript path aliases alone do not teach Node to resolve them. Do not convert an existing CommonJS service to ESM without a task reason and consumer checks.

Compare [assets/tsconfig.server.json](assets/tsconfig.server.json) and [assets/eslint.server.js](assets/eslint.server.js) with the repository; never overwrite its configuration blindly. Set strict checks explicitly, including indexed access, exact optional properties, override, and module syntax where supported. Read the installed [TypeScript options](https://www.typescriptlang.org/tsconfig/) and [typescript-eslint support](https://typescript-eslint.io/users/dependency-versions/) before changing flags or presets. Read the `toolchain-upgrade` skill when installed for compiler or lint version changes. Read the `project-guardrails` skill when installed for general check and CI setup.

Run type checking separately from the test runner and build. Use typed promise checks for floating promises and misused async callbacks. An explicit `void` marks intent but does not handle a rejection; attach error handling or supervise the task. Run existing formatting, type, lint, and build commands independently so each failure remains visible.

## Parse at boundaries

Parse request data, environment variables, queue payloads, stored versioned JSON, and dependency responses into named values. Choose size and representation limits before parsing large bodies. Read [references/boundary-parsing.md](references/boundary-parsing.md) when selecting unknown-key, coercion, or precision behavior. Keep authorization separate from shape validation. Model expected domain failures explicitly and map them to public errors at one boundary.

Parse configuration before listening or claiming work. On missing or invalid configuration, exit with a diagnostic naming the key and expected shape, never the value. Test a missing key and a syntactically valid but invalid value.

When native type stripping is part of deployment, verify its exact runtime support and permitted syntax against [Node's TypeScript documentation](https://nodejs.org/api/typescript.html). Use the installed compiler's erasable-syntax check where available. Native stripping does not perform type checking or apply tsconfig path mappings. Read [references/bun-deno.md](references/bun-deno.md) only when the actual target is Bun or Deno.

## Own time, work, and lifecycle

Pass a request or job `AbortSignal` through each dependency layer and combine it with a finite operation deadline using supported runtime APIs. Check cancellation during connection setup and body consumption. Bound fan-out, queue depth, body/decompression sizes, regular-expression work, and active dependency calls. Profile CPU-heavy parsing or computation and move it off the event loop when evidence supports that change. Worker threads also need bounded admission and shutdown.

Keep startup, resource acquisition, serving, and teardown explicit. A lifecycle function should open and close the same resources in tests and deployment. Supervise required async work; use a durable job for work that must survive process loss. Read the `service-resilience` skill when installed for retry budgets, overload, and drain deadlines. Read the `async-messaging` skill when installed for durable work.

## Test the artifact

Copy the service into an explicitly disposable test directory with synthetic configuration. Run `python3 <skill-dir>/scripts/smoke-built-entry.py --help` for the bounded build/import/start/reject interface. Supply the actual deployment Node executable and its expected exact version from the deployment record. The helper runs an explicit build argv without a shell, checks an emitted JavaScript entry, and either imports it to completion or starts it until an application readiness file appears. In start mode it sends SIGTERM and requires a clean bounded exit. Child output stays private; results are JSON on stdout and safe diagnostics on stderr. Exits: 0 pass, 1 finding, 2 invalid input.

Use import mode for importable modules and start mode for executable services. The readiness file is a fixture adapter written only after the service is ready; an early marker cannot prove listening. Test actual readiness and accepted-work draining through the project's service tests as well. The helper requires a POSIX host and Python, not a package install or an assumed build script.

Use reject mode with `--expect-key KEY` for missing and invalid startup configuration. It requires a nonzero application exit and that key in the diagnostic. Add `--forbid SYNTHETIC_CANARY` to reject a known fake secret leak; never pass real credentials as arguments. Raw diagnostics are bounded and withheld, so this mode proves the canary check rather than merely hiding output.

Done when separate types and typed lint pass, invalid configuration fails before admission, and the emitted artifact starts or imports on the recorded runtime. Include cancellation, event-loop limits, lifecycle evidence, exact commands, and unrun deployment paths in the result.
