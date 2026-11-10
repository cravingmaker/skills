# Action references

Read this when auditing or replacing action references.

Use the repository-pinned YAML parser to export every affected workflow and local/composite action document to JSON.
Run actionlint before conversion; preserve mappings and the literal `on` key.
The resolver walks all `uses` entries in each supplied document; include recursively referenced local action documents.
Native analyzers remain responsible for YAML and expression semantics.

`--tags tags.json` is an object mapping each complete remote `uses` value to its intended upstream release tag, extracted from the reviewed pin update or version comment.
For each reference, the script requires a full commit SHA, fetches the tag from the expected repository's Git refs endpoint, follows annotated tag objects and compares the resolved commit exactly.
This establishes current upstream tag membership rather than relying on a commit lookup that might also find fork-network objects.
Verify a displayed version comment agrees with that tag; parser JSON has no comments, so the helper cannot make that comparison for you.
A tag mismatch can mean a moved tag or a stale comment; inspect upstream evidence before changing the pin.

Local `./` actions need source review at the executing SHA.
The helper checks container-action digest syntax only; obtain registry manifest and signature readback separately.
A valid pin fixes bytes and origin evidence; it does not establish that the code is benign.

If the current target supports workflow lockfiles, use its official generator and check mode after verifying availability, format, coverage and transitive dependencies in primary GitHub docs.
The custom resolver implements strict full-SHA policy only; it does not infer lockfile coverage or its schema.
Remote reusable-workflow calls remain full-SHA pinned under this skill's policy.
Never invent a commit, digest, tool version or extension command from memory.

REST calls are GETs to the public GitHub API; the helper does not support a private enterprise API host.
For a different host or a repository requiring an untagged commit, use the host's native pin/origin checks and record the limitation rather than fabricating a tag.
If authentication is required, configure the existing `GH_TOKEN` mechanism or use the repository's authenticated CLI; do not paste a credential into arguments.
