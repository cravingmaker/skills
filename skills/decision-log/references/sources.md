# Sources and policy limits

Accessed 2026-11-08.

- **Durable progress.** [Anthropic, Effective harnesses for long-running agents](https://www.anthropic.com/research/effective-harnesses-for-long-running-agents), published 2025-11-26, describes progress artifacts, structured completion state, and inspection at the beginning of a fresh session; it demonstrates one coding harness rather than a universal persistence protocol.
- **Decision evidence.** [NASA Systems Engineering Handbook, 6.8 Decision Analysis](https://www.nasa.gov/reference/6-8-decision-analysis/) describes decision criteria, alternatives, uncertainty, evaluation results, recommendations, and decision authority, with effort proportional to the decision.

The exact file layout, intent/receipt ledger, immutable draft convention, cancellation reconciliation, retry limits, and scaffold behavior are original local operating policies. They are designed to make missing evidence and unfinished work visible; they do not provide transactional host dispatch or a guarantee against duplicate external effects. Use live host facilities for task discovery, receipts, completion, and cancellation; this skill asserts no fixed tool names or host behavior.
