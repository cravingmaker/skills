// Adapted from Matt Pocock at 49dd158d1076134a641b33efb035946536778336.
// See ../references/SOURCES.md and ../LICENSE-mattpocock.
// Tested example: dependency-cruiser 18.7.2 with TypeScript 5.9.3.
// Compare and merge, never overwrite; use a supported parser, not just a CLI.
// Confirm installed release/runtime support before adopting this adapter.
// Public root files and private subfolders apply only to a flat package root.
const PACKAGES_ROOT = "src/packages";
const R = PACKAGES_ROOT.replace(/[|\\{}()[\]^$+*?.-]/g, "\\$&");
const INTERNALS = "^" + R + "/[^/]+/[^/]+/";

module.exports = {
  forbidden: [
    {
      name: "entrypoint-boundary-from-app",
      comment: "Outside code reaches packages through their public root files.",
      severity: "error",
      from: { pathNot: "^" + R + "/" },
      to: { path: INTERNALS },
    },
    {
      name: "entrypoint-boundary-across-packages",
      comment: "Production code may use its own internals, not another package's.",
      severity: "error",
      from: { path: "^" + R + "/([^/]+)/", pathNot: "^" + R + "/[^/]+/tests/" },
      to: { path: INTERNALS, pathNot: "^" + R + "/$1/" },
    },
    {
      name: "tests-through-entrypoints",
      comment: "Tests use public entry points and their own test fixtures.",
      severity: "error",
      from: { path: "^" + R + "/([^/]+)/tests/" },
      to: { path: INTERNALS, pathNot: "^" + R + "/$1/tests/" },
    },
    {
      name: "tests-folder-is-private",
      comment: "Production code cannot import test fixtures.",
      severity: "error",
      from: { pathNot: "^" + R + "/[^/]+/tests/" },
      to: { path: "^" + R + "/[^/]+/tests/" },
    },
    { name: "no-circular", severity: "error", from: {}, to: { circular: true } },
    { name: "no-unresolved", severity: "error", from: {}, to: { couldNotResolve: true } },
  ],
  options: {
    doNotFollow: { path: "(^|/)node_modules/" },
    tsConfig: { fileName: "tsconfig.json" },
    tsPreCompilationDeps: true,
    enhancedResolveOptions: { extensions: [".ts", ".tsx", ".js", ".jsx", ".json"] },
  },
};
