REVIEWED: plan.md at sha256 a1b2; scope: R1-01 and the revised import contract

### R1-01 [should] plan.md:§2: The import and cache contracts contradict each other.
Evidence (static): plan.md §2 says "import commits new prices without invalidating cached prices"; §3 promises "cached reads always return the latest committed price".
Change: Require price-key invalidation at the end of the bulk import.

VERDICT: OBJECTIONS REMAIN (0 blockers, 1 should, 0 nits)
