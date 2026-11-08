---
name: sharpen
description: "Make a requested task deeper without making it bigger, then rewrite its prompt. Use when the user invokes sharpen to refine a supplied task rather than execute it."
license: MIT
metadata:
  source: "https://github.com/cursor/plugins/blob/6b0300214a09fd6029cfb7077043125758cd1fd2/pstack/skills/sharpen/SKILL.md"
  source-revision: "6b0300214a09fd6029cfb7077043125758cd1fd2"
  source-files: "pstack/skills/sharpen/SKILL.md"
  local-changes: "Mechanical changes only: spec frontmatter, owned invocation preference and description, provenance, source links, licenses, and eval packaging. The upstream body is unchanged."
---

I want a deeper version of this task, not a bigger one. Before rewriting it, do four things:

1. Say what a top professional in this field would do here that I'm not asking for.
2. Name the rawest material they would start from instead of what has already been digested for me.
3. Name the specific methods and tools they would use.
4. Say what, other than you or me, would show the result is right.

Then rewrite my prompt to ask for exactly that.

Leave choices that are mine to make open instead of deciding them.

## Provenance

Read [the per-file sources](references/SOURCES.md) when checking attribution, original hashes, destinations, and adaptation.
