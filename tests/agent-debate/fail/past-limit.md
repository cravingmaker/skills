REVIEWED: plan.md at sha256 9b1c; scope: open findings and the diff since round 3

### R1-01 [should] plan.md:§3: The rollback step still assumes a single region.
Evidence (executed): the new dry run in round 4 failed in the second region.
Change: Add a per-region rollback step.

VERDICT: OBJECTIONS REMAIN (0 blockers, 1 should, 0 nits)
