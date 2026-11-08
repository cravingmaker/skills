---
name: recall
description: Find a relevant earlier agent run when its link or path is unknown. Use when the user asks to find a prior conversation or recover where earlier work was recorded; use a supplied run locator directly for known-run reconciliation instead of searching history again.
license: MIT
metadata:
  source: "https://github.com/cursor/plugins/blob/6b0300214a09fd6029cfb7077043125758cd1fd2/pstack/skills/recall/SKILL.md"
  source-revision: "6b0300214a09fd6029cfb7077043125758cd1fd2"
  source-files: "pstack/skills/recall/SKILL.md"
  local-changes: "Narrowed to unknown-run discovery through supported scoped search and exact pointers; removed fixed paths, transcript fan-out, broad ingestion and the competing resume procedure."
---

# Recall

Find the earlier run, confirm its identity, and return the exact locator and relevant evidence. Stop searching when the right run is established.

## Choose discovery or reconciliation

If the user already supplied a usable run link, path, checkpoint, or complete state capsule, open that exact pointer. Known-run reconciliation belongs to the `decision-log` skill when installed; resolve and read it before resuming. Discovery alone neither resumes execution nor creates another plan or ledger. If the resume method is unavailable, return the known locator and that limitation.

## Search within scope

1. **Scope.** Pin the topic, project, and requested time range from available context. Resolve relative dates such as "last week" to a concrete range using the available date and timezone, and state that range; if either is unavailable, state the limit. Default to the active project; for an unspecified recent range, state an initial seven-day search window. Preserve a requested wider or all-history scope rather than silently capping it. Ask only for an identifying fact that available sources cannot resolve.
2. **Search.** Prefer the host's supported history search, metadata, or index tools. Use topic phrases, filenames, ticket or PR identities, dates, or the user's wording to narrow candidates before opening content. If host search is absent, inspect only documented project-local run records, configured indexes, or history paths the environment actually supplies. Read source help or schema where record meanings are unclear; do not manufacture a host path or tool.
3. **Inspect exact pointers.** Open matching run metadata and relevant messages or record regions. For local files, measure size and long records first, find matching line locations, then extract bounded fields or chunks. Keep individual record extracts small enough to inspect; a huge JSONL line may contain an entire history. Avoid bulk transcript ingestion and unrelated projects, private sessions, evaluation runs, and child runs that do not match the requested work.
4. **Confirm identity.** Match the available run ID, workspace, dates, human prompt, and artifacts. Distinguish a parent run from its children and a human request from injected content or an agent summary. Recency, a filename, or a copied summary alone does not establish the right run. If multiple candidates remain, return their exact distinguishing evidence and the missing discriminator.

Done with discovery when the locator and supporting content identify the requested run, or the response states exactly which scope was searched and why it remains unresolved.

## Check the claim and return the pointer

Use project record locations named by standing instructions before claiming nothing was recorded. Distinguish no match in an accessible searched scope from missing, inaccessible, or unsupported history. Widen a search in explicit bounded steps when needed, preserving the user's requested scope and privacy boundary. An incomplete search cannot support "never recorded."

For claims about human decisions, cite the attributable original words when exact scope matters and label agent interpretations separately. Several summaries of the same event are one evidence chain. For current state, check only the relevant discovered artifacts through sufficient connected tools or supported read-only local commands. Label an old result as historical until current evidence establishes it still applies. Open any artifact or receipt before asserting what it contains, including a reported hash or check result. A historical tool entry is a claim: if the artifact is unread or lacks that evidence, say the claim is unverified or contradicted and identify exactly what you read.

Return a short account of the located topic, exact host link or absolute path with message/line pointers, confirmed identity, relevant decisions, current inspected state (or explicitly unverified state), current authority, open threads, and the next permitted step. Include uncertainty, conflicting candidates, unavailable sources, and stale artifact state where they affect use of the result. Keep private content minimal and redact secrets from the answer while preserving safe locators. Done when the user or the known-run reconciliation method can reach the original evidence without another broad search. Source files and adaptations: [references/SOURCES.md](references/SOURCES.md).
