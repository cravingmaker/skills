# Preserved review history (synthetic fixture)

Review r1, 2026-10-01: src/app.js imported fixture-boundary/internal/db.js; use the public query export. The same file called db.query("select 1") without await.

Review r2, 2026-10-15: the internal import and unawaited db.query were repeated; reviewer again required the public API and await.

Current r3 has both wrong patterns again in src/app.js.
