#!/usr/bin/env python3
"""Check normalized docker compose config --format json without echoing values.

Python 3.12+, stdlib only. Read-only files/stdin; never calls Docker or mutates.
Declare the expected project, each stateful service and each agreed public service.
Output: JSON counts and indexed fixed findings on stdout; diagnostics on stderr.
No service names, environment values, port numbers or storage paths are printed.
Exit: 0 checks pass, 1 findings, 2 invalid input/usage/Python version.
--help exits 0 without reading input. This is not a complete secret scanner.
"""

import argparse
import ipaddress
import json
import re
import sys
from pathlib import Path

SECRET_NAME = re.compile(r'(?:PASSW(?:OR)?D|TOKEN|SECRET|(?:API|PRIVATE|ACCESS)_?KEY|CREDENTIAL|DATABASE_URL|DSN)', re.I)


def unique(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError('duplicate member')
        result[key] = value
    return result


def reject_constant(_):
    raise ValueError('invalid numeric constant')


def mapping(value):
    if not isinstance(value, dict):
        raise ValueError('expected mapping')
    return value


def sequence(value):
    if not isinstance(value, list):
        raise ValueError('expected list')
    return value


def healthy(service):
    health = mapping(service.get('healthcheck', {}))
    test = health.get('test', [])
    if not isinstance(test, list) or any(not isinstance(item, str) for item in test):
        raise ValueError('normalized healthcheck required')
    return bool(test) and test[0] != 'NONE' and health.get('disable') is not True


def check(model, expected, stateful, public):
    model = mapping(model)
    services = mapping(model.get('services'))
    volumes = mapping(model.get('volumes', {}))
    if not services or stateful - set(services) or public - set(services):
        raise ValueError('declare existing services')
    findings = []

    def finding(index, rule, fix):
        findings.append({'service': index, 'rule': rule, 'fix': fix})

    if model.get('name') != expected:
        finding(0, 'project-identity', 'Render with the explicit expected project name and preserve it through cleanup.')
    if 'version' in model:
        finding(0, 'obsolete-version', 'Remove the authored top-level version key and rerender.')
    for volume in volumes.values():
        volume = mapping(volume)
        if not isinstance(volume.get('name'), str) or not volume['name']:
            finding(0, 'volume-identity', 'Record the normalized physical name and ownership of each named volume.')
    published = 0
    for index, (name, service) in enumerate(services.items(), 1):
        service = mapping(service)
        if name in stateful and not healthy(service):
            finding(index, 'stateful-healthcheck', 'Add an enabled usable-protocol healthcheck for this stateful service.')
        for target, dependency in mapping(service.get('depends_on', {})).items():
            dependency = mapping(dependency)
            if target not in services:
                raise ValueError('missing dependency')
            condition = dependency.get('condition')
            if condition not in ('service_started', 'service_healthy', 'service_completed_successfully'):
                raise ValueError('normalized dependency condition required')
            if target in stateful and condition != 'service_healthy':
                finding(index, 'stateful-ordering', 'Wait for the stateful dependency with service_healthy.')
            if condition == 'service_healthy' and not healthy(mapping(services[target])):
                finding(index, 'missing-dependency-healthcheck', 'Give the service_healthy dependency an enabled healthcheck.')
        for port in sequence(service.get('ports', [])):
            port = mapping(port)
            if 'published' not in port:
                continue
            published += 1
            address = port.get('host_ip', '')
            if not isinstance(address, str):
                raise ValueError('invalid host_ip')
            try:
                loopback = ipaddress.ip_address(address).is_loopback
            except ValueError:
                loopback = False
            if not loopback and name not in public:
                finding(index, 'public-port', 'Bind to loopback or explicitly declare this service public after exposure review.')
        for key, value in mapping(service.get('environment', {})).items():
            if not isinstance(key, str) or (value is not None and not isinstance(value, (str, int, float, bool))):
                raise ValueError('invalid environment')
            if SECRET_NAME.search(key) and not key.upper().endswith('_FILE') and value not in ('', None):
                finding(index, 'credential-environment', 'Use a scoped secret file or approved delivery method instead of a literal credential environment value.')
        mounts = sequence(service.get('volumes', []))
        if name in stateful and not any(mapping(mount).get('type') in ('volume', 'bind') and
                                        mapping(mount).get('source') for mount in mounts):
            finding(index, 'stateful-storage', 'Mount reviewed persistent storage at the service data path; a top-level declaration alone stores nothing.')
        for mount in mounts:
            mount = mapping(mount)
            if mount.get('type') == 'volume' and (not mount.get('source') or mount['source'] not in volumes):
                finding(index, 'anonymous-or-undeclared-volume', 'Declare a named volume and record its physical identity and cleanup ownership.')
            if mount.get('type') not in ('volume', 'bind', 'tmpfs', 'image', 'npipe', 'cluster'):
                raise ValueError('unsupported normalized mount; consult installed Compose')
    return {'checked': len(services), 'named_volumes': len(volumes), 'published_ports': published,
            'declared_public_services': len(public), 'findings': findings}


class ValueSafeArgumentParser(argparse.ArgumentParser):
    def error(self, message):
        self.print_usage(sys.stderr)
        self.exit(2, 'error: use the documented arguments; see --help\n')


def main():
    parser = ValueSafeArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('config_json', help='normalized config JSON file, or - for stdin')
    parser.add_argument('--expected-project', required=True)
    parser.add_argument('--stateful', action='append', default=[], metavar='SERVICE')
    parser.add_argument('--public-service', action='append', default=[], metavar='SERVICE')
    args = parser.parse_args()
    if sys.version_info < (3, 12):
        print('error: use Python 3.12 or later', file=sys.stderr)
        return 2
    try:
        raw = sys.stdin.read() if args.config_json == '-' else Path(args.config_json).read_text(encoding='utf-8')
        model = json.loads(raw, object_pairs_hook=unique, parse_constant=reject_constant)
        report = check(model, args.expected_project, set(args.stateful), set(args.public_service))
    except (OSError, UnicodeError, ValueError, RecursionError, TypeError):
        print('error: supply normalized Compose JSON and existing declared services; see --help', file=sys.stderr)
        return 2
    print(json.dumps(report, sort_keys=True))
    return int(bool(report['findings']))


if __name__ == '__main__':
    sys.exit(main())
