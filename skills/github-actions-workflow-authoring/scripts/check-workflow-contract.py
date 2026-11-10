#!/usr/bin/env python3
"""Check parser-produced workflow JSON and effective ruleset JSON, read-only.

Python 3.12+ standard library. Run actionlint and an established YAML parser first.
Checks graph/name declarations and environment-job cancellation, not expressions, matrix expansion, gate shell
behavior, repository settings or event reachability. Never pass raw YAML.
Output: JSON findings on stdout; invalid-input diagnostics on stderr, no values.
Exit: 0 pass, 1 findings, 2 usage/input. --help has no effects.
"""

import argparse
import json
import sys
from collections import Counter
from pathlib import Path


def unique(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError('duplicate key')
        result[key] = value
    return result


def load(path):
    return json.loads(path.read_text(encoding='utf-8'), object_pairs_hook=unique)


def rules_from(value):
    if isinstance(value, list):
        return [rule for item in value for rule in rules_from(item)]
    if not isinstance(value, dict):
        raise ValueError('rules must be objects')
    if 'rules' in value:
        return rules_from(value['rules'])
    if 'contexts' in value or 'checks' in value:
        contexts, checks = value.get('contexts', []), value.get('checks', [])
        if not isinstance(contexts, list) or not isinstance(checks, list):
            raise ValueError('legacy required check lists required')
        if not all(isinstance(c, str) and c for c in contexts):
            raise ValueError('legacy context strings required')
        return [{'type': 'required_status_checks', 'parameters': {
            'required_status_checks': [{'context': c} for c in contexts] + checks}}]
    if isinstance(value.get('type'), str):
        return [value]
    raise ValueError('fetch full ruleset details')


def check(workflows, rules):
    findings, names, job_count = [], Counter(), 0
    for number, workflow in enumerate(workflows, 1):
        if not isinstance(workflow, dict):
            raise ValueError('workflow mapping required')
        prefix = f'workflow {number}'
        if 'on' not in workflow:
            findings.append(prefix + ': preserve the on key with a YAML-aware parser')
        if 'permissions' not in workflow:
            findings.append(prefix + ': declare workflow permissions')
        jobs = workflow.get('jobs')
        if not isinstance(jobs, dict) or not jobs:
            raise ValueError('nonempty job mapping required')
        graph = {}
        for index, (job_id, job) in enumerate(jobs.items(), 1):
            if not isinstance(job, dict):
                raise ValueError('job mapping required')
            job_count += 1
            label = prefix + f' job {index}'
            if not workflow.get('concurrency') and not job.get('concurrency'):
                findings.append(label + ': declare workflow or job concurrency')
            if 'environment' in job:
                for scope, policy in (('workflow', workflow.get('concurrency')), ('job', job.get('concurrency'))):
                    if isinstance(policy, dict) and policy.get('cancel-in-progress', False) is not False:
                        findings.append(label + f': disable or prove {scope} cancellation before mutation')
            if 'uses' not in job:
                timeout = job.get('timeout-minutes')
                if type(timeout) is not int or timeout <= 0:
                    findings.append(label + ': set a positive integer runner timeout')
            needs = job.get('needs', [])
            needs = [needs] if isinstance(needs, str) else needs
            if not isinstance(needs, list) or not all(isinstance(n, str) for n in needs):
                raise ValueError('needs must contain job IDs')
            graph[job_id] = needs
            if any(n not in jobs for n in needs):
                findings.append(label + ': resolve every needs job ID')
            name = job.get('name', job_id)
            strategy = job.get('strategy', {})
            if not isinstance(strategy, dict):
                raise ValueError('strategy mapping required')
            if isinstance(name, str) and '${{' not in name and 'matrix' not in strategy and 'uses' not in job:
                names[name] += 1
        visiting, visited = set(), set()

        def cyclic(node):
            if node in visiting:
                return True
            if node in visited or node not in graph:
                return False
            visiting.add(node)
            if any(cyclic(dep) for dep in graph[node]):
                return True
            visiting.remove(node)
            visited.add(node)
            return False

        if any(cyclic(node) for node in graph):
            findings.append(prefix + ': remove the needs cycle')
    required = set()
    for rule in rules:
        if rule.get('type') != 'required_status_checks':
            continue
        parameters = rule.get('parameters')
        if not isinstance(parameters, dict):
            raise ValueError('rule parameters missing')
        checks = parameters.get('required_status_checks')
        if not isinstance(checks, list):
            raise ValueError('required check list missing')
        for item in checks:
            if not isinstance(item, dict) or not isinstance(item.get('context'), str) or not item['context']:
                raise ValueError('context missing')
            required.add(item['context'])
    for index, name in enumerate(sorted(required), 1):
        if names[name] != 1:
            findings.append(f'required context {index}: provide one matching static non-matrix job or obtain hosted naming evidence')
    return {'workflows': len(workflows), 'jobs': job_count,
            'required_contexts': len(required), 'findings': findings}


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('workflow', type=Path, nargs='+', help='actual workflows exported as JSON by a YAML parser')
    parser.add_argument('--rules', type=Path, required=True, help='fully expanded effective ruleset JSON')
    args = parser.parse_args()
    if sys.version_info < (3, 12):
        print('error: use Python 3.12 or later', file=sys.stderr)
        return 2
    try:
        result = check([load(path) for path in args.workflow], rules_from(load(args.rules)))
    except (OSError, UnicodeError, ValueError, TypeError, RecursionError):
        print('error: pass valid unique-key workflow JSON and full ruleset detail JSON; see --help', file=sys.stderr)
        return 2
    print(json.dumps(result, indent=2))
    return 1 if result['findings'] else 0


if __name__ == '__main__':
    sys.exit(main())
