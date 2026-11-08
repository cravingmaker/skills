REVIEWED: plan.md at sha256 a1b2; scope: R1-01 after the spike ran

### R1-01 [should] plan.md:§2: The cache serves stale prices after a bulk import.
Evidence (executed): `python3 probes/import-cache.py` exits 1 and prints `price after import: 120; cache: 100`.
Change: Invalidate the price keys at the end of the bulk import.

VERDICT: OBJECTIONS REMAIN (0 blockers, 1 should, 0 nits)
