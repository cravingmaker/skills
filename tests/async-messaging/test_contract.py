"""Fixture tests for async-messaging/scripts/check-messaging-contract.py."""

import copy
import json
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SKILL = ROOT / "skills" / "async-messaging"
SCRIPT = SKILL / "scripts" / "check-messaging-contract.py"
TEMPLATE = SKILL / "assets" / "messaging-contract.json"
HERE = Path(__file__).resolve().parent
FAILURES = []


def run(*args):
    return subprocess.run([sys.executable, str(SCRIPT), *args], capture_output=True, text=True, timeout=10)


def run_contract(data):
    with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as handle:
        json.dump(data, handle)
    try:
        return run(handle.name)
    finally:
        Path(handle.name).unlink()


def expect(name, condition, detail=""):
    if not condition:
        FAILURES.append(f"{name}: {detail}")


base = json.loads(TEMPLATE.read_text(encoding="utf-8"))

result = run("--help")
expect("help exits 0", result.returncode == 0 and "Exit:" in result.stdout, result.stdout + result.stderr)

result = run()
expect("no args is usage", result.returncode == 2, str(result.returncode))

result = run(str(TEMPLATE))
expect("template passes", result.returncode == 0 and result.stdout.startswith("OK 1"), result.stdout)
before = TEMPLATE.read_bytes()
repeat = run(str(TEMPLATE))
expect("repeat and read-only", result.stdout == repeat.stdout and repeat.returncode == 0 and TEMPLATE.read_bytes() == before)

result = run(str(HERE / "bad-contract.json"))
expect("bad contract fails", result.returncode == 1, str(result.returncode))
expect("timeout above lease", "handler_timeout_seconds 120 is not below lease_seconds 60" in result.stdout, result.stdout)
expect("window above retention", "worst-case retry window" in result.stdout, result.stdout)
expect("exactly two findings", result.stdout.count("FAIL ") == 2, result.stdout)

cases = {
    "exactly-once rejected": (lambda c: c.update(delivery="exactly-once"), "outside this contract"),
    "unbounded attempts": (lambda c: c.update(max_attempts=0), "max_attempts must be a finite integer"),
    "missing dedupe": (lambda c: c.pop("dedupe_key"), "dedupe_key is missing"),
    "no jitter": (lambda c: c["backoff"].update(jitter="none"), "jitter must be"),
    "ordering without reason": (lambda c: c.update(ordering="per-key:order_id"), "ordering_reason is missing"),
    "ordering without key": (lambda c: c.update(ordering="per-key:", ordering_reason="x"), "needs the key name"),
    "no dead-letter owner": (lambda c: c.update(dead_letter_owner=""), "dead_letter_owner is missing"),
    "no replay owner": (lambda c: c.pop("replay_authorized_by"), "replay_authorized_by is missing"),
    "schema version": (lambda c: c["schema"].update(version="2"), "schema.version must be"),
    "at-most-once outside scope": (lambda c: c.update(delivery="at-most-once"), "outside this contract"),
    "timeout equal to lease": (lambda c: c.update(handler_timeout_seconds=300), "is not below lease_seconds"),
    "cancellation consumes lease": (lambda c: c.update(handler_timeout_seconds=295), "plus cancellation margin"),
    "queue delay consumes retention": (lambda c: c.update(queue_delay_bound_seconds=604800), "worst-case retry window"),
}
for name, (mutate, needle) in cases.items():
    data = copy.deepcopy(base)
    mutate(data["consumers"][0])
    result = run_contract(data)
    expect(name, result.returncode == 1 and needle in result.stdout, result.stdout + result.stderr)

result = run_contract({"consumers": []})
expect("empty consumers is usage", result.returncode == 2, str(result.returncode))

for text in ('{"consumers":[],"consumers":[]}', '{"consumers":[NaN]}', "{"):
    with tempfile.NamedTemporaryFile("w", suffix=".json") as handle:
        handle.write(text)
        handle.flush()
        expect("malformed input refused", run(handle.name).returncode == 2)

data = copy.deepcopy(base)
data["consumers"][0]["lease_seconds"] = 1e309
expect("nonfinite duration refused", run_contract(data).returncode == 2)

data = copy.deepcopy(base)
data["consumers"][0]["name"] = "SYNTHETIC_ONLY_CANARY"
data["consumers"][0]["delivery"] = "SYNTHETIC_ONLY_CANARY"
result = run_contract(data)
expect("source strings withheld", result.returncode == 1 and "SYNTHETIC_ONLY_CANARY" not in result.stdout + result.stderr)

data = copy.deepcopy(base)
data["consumers"][0]["max_attempts"] = 1000000
result = run_contract(data)
expect("large finite count is bounded arithmetic", result.returncode == 1 and "retry window" in result.stdout, result.stderr)

for failure in FAILURES:
    print(f"FAIL {failure}", file=sys.stderr)
if FAILURES:
    sys.exit(1)
print("async-messaging contract fixtures passed")
