# Proposed Rust rewrite

Rewrite the existing TypeScript CLI in Rust over six weeks to reduce startup time from 230 ms to 30 ms. The current CLI uses 14 Node-specific libraries, ships two weekly feature releases, and has no Rust maintainers. The performance target is a proposal, not a measurement. The plan assigns all three maintainers to the rewrite, with no parallel TypeScript maintenance. It assumes existing integration tests can be reused unchanged.
