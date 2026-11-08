# Status feature and migration

Implement a status card backed by the fixed API in contracts/status.json. Backend owns backend/service.py, frontend owns frontend/client.py, QA owns tests/test_contract.py; one coordinator integrates. Migration replaces the old active boolean with status=active|paused. No schema changes, no dependencies, no external actions, no deployment. Each task may need a unique report under reports/. Run ./scripts/validate.sh.

Planning tasks: determine whether this cohesive migration merits independent workers; alternatively split the two independent consumers backend and frontend against the fixed contract. State a finite budget and preserve integration capacity. Cache design: freshness <=30 seconds; 100 reads/s; one service instance now, three next quarter; Redis adds an external dependency; process-local cache loses cross-instance invalidation. Background work choice: events arrive in bursts; at-least-once processing and per-event retries are mandatory; the existing cron cannot track per-event acknowledgements. Do not claim a live model route exists in this fixture.

No commits or pushes are permitted, including in temporary repositories.
