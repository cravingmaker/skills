# Offline lint upgrade exercise

The synthetic @fixture/eslint-plugin and @fixture/typescript-eslint stand in for ESLint plugins and typescript-eslint. They are not real upstream releases. The fixture registry and changelogs in registry/ are the authoritative local inputs for this exercise; do not infer current public versions. The evaluation date is 2026-11-08. Policy: exact pins, minimum release age seven days, new preset rules stay off until individually decided, no network or new external tools. A simulated Dependabot PR proposes @fixture/typescript-eslint 1.1.0 from 1.0.0. Both plugins share the behavior described in registry/releases.json.

Run `python3 -B scripts/tooling.py config` before and after, `python3 -B scripts/tooling.py releases`, `python3 -B scripts/tooling.py upgrade VERSION`, and `./scripts/validate.sh`. `upgrade` refreshes both exact pins and the lockfile. 1.2.0 is too young. CI passes at 1.1.0 even though eqeqeq is added and max-len changes default. A policy override in eslint-policy.json takes precedence. Explain the ESLint eqeqeq finding in src/example.js when asked why it fires.

No commits or pushes are permitted, including in temporary repositories.
