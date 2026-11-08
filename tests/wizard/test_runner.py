#!/usr/bin/env python3
"""Check that offline setup skips cleanly while actual fixture failures propagate."""
import os
from pathlib import Path
import subprocess
import tempfile

RUNNER = Path(__file__).with_name('run.sh')
with tempfile.TemporaryDirectory(prefix='wizard-offline-') as directory:
    root = Path(directory)
    uv = root / 'uv'
    uv.write_text('''#!/bin/sh
printf '%s\\n' "$*" >> "$WIZARD_UV_LOG"
case "$1" in
  sync) exit "${WIZARD_SYNC_EXIT:-0}" ;;
  run) exit "${WIZARD_RUN_EXIT:-0}" ;;
  *) exit 91 ;;
esac
''')
    uv.chmod(0o755)
    # Prevent recursive runner tests in this copy; exercise the real wrapper bytes.
    runner = root / 'run.sh'
    runner.write_bytes(RUNNER.read_bytes())
    (root / 'test_runner.py').write_text('')
    log = root / 'calls'
    env = dict(os.environ, PATH=str(root) + os.pathsep + os.environ['PATH'], WIZARD_UV_LOG=str(log))
    for setup, test, expected in ((1, 0, 0), (0, 7, 7), (0, 0, 0)):
        log.write_text('')
        result = subprocess.run(['sh', str(runner)], env=dict(env, WIZARD_SYNC_EXIT=str(setup), WIZARD_RUN_EXIT=str(test)), text=True, capture_output=True)
        assert result.returncode == expected, result
        calls = log.read_text().splitlines()
        assert calls and all('--offline' in call for call in calls), calls
        assert len(calls) == (1 if setup else 2), calls
        assert ('Skipped wizard parser fixtures:' in result.stdout) == bool(setup), result
        if setup:
            assert 'python-dotenv==1.1.1' in result.stdout and 'uv sync --script' in result.stdout
print('wizard runner: offline skip and test-failure propagation passed')
