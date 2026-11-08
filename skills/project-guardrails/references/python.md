# Python profile

This profile lists capabilities and candidate tools. None of it is verified against a reference repository yet, so confirm each tool and its settings from official documentation for the versions in use before adopting them, and record the source in the report.

| Capability | Candidates to verify | Where to look in a project |
| --- | --- | --- |
| Formatter | Ruff format | `pyproject.toml` `[tool.ruff]` |
| Linter with an explicit rule selection | Ruff | `[tool.ruff.lint]` `select` and `ignore` |
| Strict type checking | mypy in strict mode, or Pyright in strict mode | `[tool.mypy]`, `pyrightconfig.json` |
| Tests | pytest | `[tool.pytest.ini_options]`, `tests/` |
| Reproducible installs | uv with a committed `uv.lock` | `uv.lock`, CI install step |
| Dependency audit | pip-audit | CI job |
| Scripts | one command per job | `Makefile`, `noxfile.py`, `[tool.uv]` or `[project.scripts]` |
| Git hooks | pre-commit | `.pre-commit-config.yaml` |

## Data projects

For data pipelines and archives, the most valuable guardrails check the data, not the code style: row counts, schema and type checks, hashes of raw inputs, and exact readback after a write. Treat a validator script that fails on bad data as a first-class guardrail, wired into the same command as the tests.
