REVIEWED: plan.md at sha256 9b1c; scope: open findings and the diff since round 1

### R1-01 [should] plan.md:§2: The cache may serve stale prices after a bulk import.
Evidence (hypothesis): run the bulk import, then read one price through the cache.
Change: Invalidate the price keys at the end of the bulk import.

VERDICT: OBJECTIONS REMAIN (0 blockers, 1 should, 0 nits)
