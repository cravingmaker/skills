"""Fixture tests for rust-async-services/scripts/check-workspace-lints.py."""

import json
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "skills" / "rust-async-services" / "scripts" / "check-workspace-lints.py"
FIXTURES = Path(__file__).resolve().parent / "fixtures"
FAILURES = []


def run(*args):
    command = [sys.executable, str(SCRIPT), *args]
    # Independent member inventories for the two existing workspace fixtures.
    if "--root" in args:
        root = Path(args[args.index("--root") + 1])
        if root.name in ("good", "missing-opt-in") and "--metadata" not in args:
            with tempfile.TemporaryDirectory() as tmp:
                metadata = Path(tmp) / "metadata.json"
                metadata.write_text(json.dumps(metadata_for(root, ["crates/api", "crates/worker"])))
                return subprocess.run(command + ["--metadata", str(metadata)], capture_output=True, text=True, timeout=10)
    return subprocess.run(command, capture_output=True, text=True, timeout=10)


def metadata_for(root, members):
    return {"version": 1, "workspace_root": str(root.resolve()),
            "workspace_members": ["fixture:" + name for name in members],
            "packages": [{"id": "fixture:" + name, "manifest_path": str(root / name / "Cargo.toml")}
                         for name in members]}


def expect(name, condition, detail=""):
    if not condition:
        FAILURES.append(f"{name}: {detail}")


result = run("--help")
expect("help exits 0", result.returncode == 0 and "Exit:" in result.stdout, result.stderr)
expect("missing manifest is usage", run("--root", str(FIXTURES / "absent")).returncode == 2)
expect("broken manifest is usage", run("--root", str(FIXTURES / "broken")).returncode == 2)
expect("bad --require is usage", run("--root", str(FIXTURES / "good"), "--require", "unwrap_used").returncode == 2)

result = run("--root", str(FIXTURES / "good"))
expect("good workspace passes, excluded crate skipped", result.returncode == 0 and result.stdout.strip() == "OK 2 crates", result.stdout + result.stderr)

result = run("--root", str(FIXTURES / "missing-opt-in"))
expect("missing opt-in fails", result.returncode == 1, result.stdout)
expect("names the worker", "FAIL worker: no lint table applies; add [lints] workspace = true" in result.stdout, result.stdout)
expect("api is fine", "FAIL api" not in result.stdout, result.stdout)

result = run("--root", str(FIXTURES / "allowed-lint"))
expect("allowed lint fails", result.returncode == 1, result.stdout)
expect("allow reported", "FAIL svc: clippy::unwrap_used is set to 'allow' in [lints]" in result.stdout, result.stdout)
expect("missing reported", "FAIL svc: clippy::expect_used is missing in [lints]" in result.stdout, result.stdout)
expect("two findings", result.stdout.count("FAIL ") == 2, result.stdout)

result = run("--root", str(FIXTURES / "single"))
expect("single package passes", result.returncode == 0 and "OK 1 crates" in result.stdout, result.stdout)

result = run("--root", str(FIXTURES / "single"), "--require", "clippy::large_futures")
expect("custom requirement", result.returncode == 1 and "clippy::large_futures is missing" in result.stdout, result.stdout)

with tempfile.TemporaryDirectory() as tmp:
    root = Path(tmp)
    root.joinpath("Cargo.toml").write_text('[workspace]\nmembers = ["api"]\n[workspace.lints.clippy]\nunwrap_used="deny"\nexpect_used="deny"\nawait_holding_lock="deny"\n')
    for name, lints in [("api", "[lints]\nworkspace=true\n"), ("implicit", "")]:
        root.joinpath(name).mkdir()
        root.joinpath(name, "Cargo.toml").write_text('[package]\nname="' + name + '"\nversion="0.1.0"\n' + lints)
    metadata = root / "metadata.json"
    metadata.write_text(json.dumps(metadata_for(root, ["api", "implicit"])))
    result = run("--root", str(root), "--metadata", str(metadata))
    expect("implicit path member cannot escape check", result.returncode == 1 and "FAIL implicit:" in result.stdout, result.stdout + result.stderr)
    expect("workspace without authoritative metadata refused", run("--root", str(root)).returncode == 2)
    root.joinpath("implicit", "Cargo.toml").write_text('[package]\nname="implicit"\nversion="0.1.0"\n[lints]\nworkspace=true\n')
    first = run("--root", str(root), "--metadata", str(metadata))
    second = run("--root", str(root), "--metadata", str(metadata))
    expect("fixed implicit member and repeat", first.returncode == 0 and first.stdout == second.stdout, first.stdout + first.stderr)
    metadata.write_text('{"version":1,"workspace_root":"/wrong"}')
    expect("stale metadata refused", run("--root", str(root), "--metadata", str(metadata)).returncode == 2)

for failure in FAILURES:
    print(f"FAIL {failure}", file=sys.stderr)
if FAILURES:
    sys.exit(1)
print("rust-async-services lint fixtures passed")
