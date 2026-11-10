"""Offline native expression/routing tests; no server, notifications or SQL."""
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile

HERE = Path(__file__).resolve().parent
PROMTOOL = shutil.which(os.environ.get('PROMTOOL', 'promtool'))
AMTOOL = shutil.which(os.environ.get('AMTOOL', 'amtool'))
PINT = shutil.which(os.environ.get('PINT', 'pint'))
fixtures = HERE / 'fixtures'
rules = json.loads((fixtures / 'rules.json').read_text())
alerts = [r for g in rules['groups'] for r in g['rules'] if 'alert' in r]
assert alerts, 'empty alert inventory'
cases = json.loads((fixtures / 'rule-tests.json').read_text())['tests']
coverage = {alert['alert']: set() for alert in alerts}
for case in cases:
    for check in case.get('alert_rule_test', []):
        assert check['alertname'] in coverage, 'test names an undefined alert'
        coverage[check['alertname']].add(bool(check['exp_alerts']))
assert all(states == {False, True} for states in coverage.values()), 'each alert needs firing and quiet cases'
for alert in alerts:
    assert alert['annotations']['runbook_url'].startswith('https://')
    assert alert['labels']['severity'] in ('page', 'ticket')
    assert alert['labels']['owner']
print(f'alert contract: {len(alerts)} synthetic alerts have runbooks and routing labels')

with tempfile.TemporaryDirectory(prefix='prometheus-rules-') as directory:
    target = Path(directory)
    for source in fixtures.iterdir():
        shutil.copyfile(source, target / source.name)
    # On Darwin os.UserConfigDir depends on HOME. Remove it only from this child
    # environment, so amtool's fallback resolves under our disposable cwd.
    # Do not read a user's client configuration or the system amtool config.
    env = dict(os.environ, XDG_CONFIG_HOME=str(target), XDG_CONFIG_DIRS=str(target))
    env.pop('HOME', None)
    def run(binary, *args):
        return subprocess.run([binary, *args], cwd=target, env=env, text=True, capture_output=True, timeout=40)
    def passes(result):
        assert result.returncode == 0, result.stdout + result.stderr
    if PROMTOOL:
        for args in (('check', 'rules', 'rules.json'), ('check', 'config', 'prometheus.json'), ('test', 'rules', 'rule-tests.json')):
            passes(run(PROMTOOL, *args))
        changed = json.loads((target / 'rules.json').read_text())
        changed['groups'][0]['rules'][1]['expr'] = 'avg by (service) (rate(fixture_duration_seconds_bucket{le="0.5"}[5m]) / ignoring (le) rate(fixture_duration_seconds_count[5m]))'
        (target / 'rules.json').write_text(json.dumps(changed))
        passes(run(PROMTOOL, 'check', 'rules', 'rules.json'))
        broken = run(PROMTOOL, 'test', 'rules', 'rule-tests.json')
        assert broken.returncode != 0 and 'fixture:latency_fraction' in broken.stdout + broken.stderr, broken
        shutil.copyfile(fixtures / 'rules.json', target / 'rules.json')
        passes(run(PROMTOOL, 'test', 'rules', 'rule-tests.json'))
        print(f'promtool: {len(cases)} synthetic cases passed; unweighted instance-fraction mutation failed; restored repeat passed')
    else:
        print('Skipped promtool cases: install the project-pinned deployed-version promtool or set PROMTOOL; no native rule claim is made')
    if AMTOOL:
        passes(run(AMTOOL, 'check-config', 'alertmanager.json'))
        for labels, receiver in ((('severity=page', 'owner=example_owner'), 'pager'), (('severity=ticket', 'owner=example_owner'), 'tickets'), (('severity=page', 'owner=unknown'), 'fallback'), (('owner=example_owner',), 'fallback')):
            passes(run(AMTOOL, 'config', 'routes', 'test', '--config.file=alertmanager.json', '--verify.receivers=' + receiver, *labels))
        broken = run(AMTOOL, 'config', 'routes', 'test', '--config.file=alertmanager.json', '--verify.receivers=tickets', 'severity=page', 'owner=example_owner')
        assert broken.returncode != 0, 'wrong receiver expectation must fail'
        passes(run(AMTOOL, 'config', 'routes', 'test', '--config.file=alertmanager.json', '--verify.receivers=pager', 'severity=page', 'owner=example_owner'))
        print('amtool: page, ticket and two fallback routes passed; wrong receiver rejected; repeat passed')
    else:
        print('Skipped amtool cases: install the project-pinned amtool or set AMTOOL; no native routing claim is made')
    if PINT:
        policy = HERE.parents[1] / 'skills/prometheus-alerting-rules/assets/pint.hcl'
        # JSON is YAML input for the native parser. Do not implement a YAML reader.
        policy_rules = target / 'policy-rules.yml'
        def lint(document):
            policy_rules.write_text(json.dumps(document))
            return run(PINT, '-n', '--offline', '-c', str(policy), 'lint', str(policy_rules))
        passes(lint(rules))
        for field in ('runbook_url', 'severity', 'owner'):
            changed = json.loads(json.dumps(rules))
            alert = next(rule for rule in changed['groups'][0]['rules'] if 'alert' in rule)
            del alert['annotations' if field == 'runbook_url' else 'labels'][field]
            broken = lint(changed)
            assert broken.returncode != 0 and field in broken.stdout + broken.stderr, broken
        passes(lint(rules))
        print('pint: native YAML policy passed; missing runbook, severity and owner rejected; restored repeat passed')
    else:
        print('Skipped pint cases: install project-pinned pint or set PINT; native metadata policy is unrun')
print('Limits: actual collector permissions, Alertmanager inhibition and notification delivery are unrun')
