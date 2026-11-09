# Sources

All accessed 2026-11-08.

## Why reports are claims

- Cemri et al., "Why Do Multi-Agent LLM Systems Fail?", NeurIPS 2025. Of 14 failure modes found in more than 1,600 traces, a whole category is task verification: premature termination, and incomplete or incorrect verification. https://arxiv.org/abs/2503.13657
- Anthropic, "How we built our multi-agent research system", 2025-06-13. Subagent outputs written to files, an end-state evaluation of the combined result, and human spot checks that caught failures the automated judges missed. https://www.anthropic.com/engineering/multi-agent-research-system
- Claude, "When to use multi-agent systems (and when not to)", 2026-01-23. Verifier agents declare a pass without running everything unless told explicitly to run the complete suite. https://claude.com/resources/articles/building-multi-agent-systems-when-and-how-to-use-them
- Huang et al., "Large Language Models Cannot Self-Correct Reasoning Yet", ICLR 2024. Revision without external feedback, such as executed tests, can make results worse. https://arxiv.org/abs/2310.01798
- Choi, Zhu, and Li, "Debate or Vote", NeurIPS 2025, and Wynn, Satija, and Hadfield, "Talk Isn't Always Cheap", 2025. Agreement between agents is weak evidence of correctness. https://arxiv.org/abs/2508.17536 ; https://arxiv.org/abs/2509.05396
- OWASP, "LLM06:2025 Excessive Agency". Peer agents are a prompt-injection path; their output is data, not authority. https://genai.owasp.org/llmrisk/llm062025-excessive-agency/

## Ownership check

- Git documentation: `git diff`, `git log --name-only`, `git ls-files --others --exclude-standard`, `git merge-base --is-ancestor`. https://git-scm.com/docs
- Git worktrees share one repository and are a checkout boundary, not a security boundary. https://git-scm.com/docs/git-worktree

## Practice

- Rerunning a cited command before keeping a finding, and recording a missing report as a gap that does not count as a pass, follow review and fan-out skills in cursor/plugins pstack (https://github.com/cursor/plugins/tree/main/pstack). No text is copied from them.
