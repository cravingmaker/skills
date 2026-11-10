#!/usr/bin/env python3
"""Check Docker inspect plus same-context docker info JSON against a strict baseline.

Python 3.12+, stdlib only. Local files/stdin only; never invokes Docker or mutates.
Output: JSON counts, security-mode booleans and indexed findings on stdout.
No environment, names, commands, raw options or mount paths are emitted.
Exit: 0 checks pass, 1 baseline findings, 2 invalid input/usage/Python version.
--help exits 0 without reading input. Passing is configuration evidence only.
"""

import argparse
import json
import posixpath
import re
import sys
from pathlib import Path

HOST_PATHS = ('/etc', '/proc', '/sys', '/dev', '/boot', '/root', '/var/lib/docker',
              '/var/lib/containerd', '/var/lib/kubelet')


def unique(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError('duplicate member')
        result[key] = value
    return result


def reject_constant(_):
    raise ValueError('invalid numeric constant')


def load(path):
    raw = sys.stdin.read() if path == '-' else Path(path).read_text(encoding='utf-8')
    return json.loads(raw, object_pairs_hook=unique, parse_constant=reject_constant)


def strings(value):
    if value is None:
        return []
    if not isinstance(value, list) or any(not isinstance(item, str) for item in value):
        raise ValueError('expected string list')
    return value


def socket_mount(path, ancestors=False):
    path = posixpath.normpath(path)
    sockets = ('/var/run/docker.sock', '/run/docker.sock', '/run/containerd/containerd.sock',
               '/run/podman/podman.sock')
    return (path in sockets or bool(re.search(r'/(?:docker|containerd|podman|crio|buildkitd)\.sock(?:/|$)', path))
            or (ancestors and (path == '/' or any(sock.startswith(path.rstrip('/') + '/') for sock in sockets))))


def check(containers, info, mode):
    if not isinstance(containers, list) or not containers or not isinstance(info, dict):
        raise ValueError('expected inspect array and info object')
    if 'SecurityOptions' not in info:
        raise ValueError('missing daemon security evidence')
    security = strings(info['SecurityOptions'])
    options = {item.removeprefix('name=').split(',', 1)[0] for item in security}
    findings = []

    def finding(index, rule, fix):
        findings.append({'container': index, 'rule': rule, 'fix': fix})

    expected = 'rootless' if mode == 'rootless' else 'userns'
    if expected not in options:
        finding(0, 'daemon-mode-unproven', 'Capture the chosen daemon mode from the same confirmed Docker context.')
    if 'seccomp' not in options:
        finding(0, 'daemon-seccomp-unproven', 'Enable and verify daemon/kernel seccomp support on the target.')
    for index, container in enumerate(containers, 1):
        if not isinstance(container, dict):
            raise ValueError('invalid container')
        config, host = container.get('Config'), container.get('HostConfig')
        if not isinstance(config, dict) or not isinstance(host, dict):
            raise ValueError('missing inspect fields')
        user = config.get('User', '')
        if not isinstance(user, str):
            raise ValueError('invalid user')
        if not re.fullmatch(r'[0-9]+(?::[0-9]+)?', user) or int(user.split(':', 1)[0]) == 0:
            finding(index, 'numeric-nonroot', 'Use an explicit numeric nonzero runtime UID.')
        for field in ('Privileged', 'ReadonlyRootfs'):
            if type(host.get(field)) is not bool:
                raise ValueError('missing runtime flag')
        if host['Privileged']:
            finding(index, 'privileged', 'Remove privileged mode and identify the narrow application need.')
        if not host['ReadonlyRootfs']:
            finding(index, 'writable-root', 'Use a read-only root and declared writable mounts.')
        if 'ALL' not in {item.upper().removeprefix('CAP_') for item in strings(host.get('CapDrop'))}:
            finding(index, 'cap-drop', 'Drop ALL capabilities before adding back a documented need.')
        if strings(host.get('CapAdd')):
            finding(index, 'cap-add', 'Review each added capability as an explicit baseline exception.')
        opts = {item.replace(':', '=', 1).lower() for item in strings(host.get('SecurityOpt'))}
        if not opts.intersection({'no-new-privileges', 'no-new-privileges=true'}):
            finding(index, 'privilege-escalation', 'Set and verify no-new-privileges.')
        if 'seccomp=unconfined' in opts:
            finding(index, 'unconfined-seccomp', 'Restore the default or reviewed restrictive seccomp profile.')
        if opts.intersection({'apparmor=unconfined', 'label=disable'}):
            finding(index, 'unconfined-lsm', 'Restore supported LSM confinement or record the disabled profile as an exception.')
        for field in ('PidMode', 'IpcMode', 'NetworkMode', 'UTSMode', 'UsernsMode'):
            if host.get(field) == 'host':
                finding(index, 'host-namespace', 'Remove host namespace sharing or record its scoped exception.')
        if host.get('Devices') or host.get('DeviceRequests'):
            finding(index, 'host-devices', 'Review device access as an explicit baseline exception.')
        memory, pids = host.get('Memory', 0), host.get('PidsLimit')
        if type(memory) is not int or memory < 0 or (pids is not None and (type(pids) is not int or pids < -1)):
            raise ValueError('invalid resource bounds')
        if memory == 0:
            finding(index, 'memory-unbounded', 'Set a memory bound from measured demand and test failure/recovery behavior.')
        if pids in (None, 0, -1):
            finding(index, 'pids-unbounded', 'Set a finite positive process bound from measured demand.')
        mounts = container.get('Mounts')
        if not isinstance(mounts, list):
            raise ValueError('missing mounts')
        for mount in mounts:
            if not isinstance(mount, dict) or not isinstance(mount.get('Source', ''), str) or not isinstance(mount.get('Destination'), str):
                raise ValueError('invalid mount')
            if socket_mount(mount.get('Source', ''), ancestors=mount.get('Type') == 'bind') or socket_mount(mount['Destination']):
                finding(index, 'control-socket-mount', 'Remove runtime sockets and parent-directory mounts; inspect proxies separately.')
            if mount.get('Type') == 'bind':
                source = posixpath.normpath(mount.get('Source', ''))
                if any(source == path or source.startswith(path + '/') for path in HOST_PATHS):
                    finding(index, 'host-system-mount', 'Replace sensitive host-system mounts with narrowly scoped application storage.')
    return {'checked': len(containers), 'daemon_mode_observed': expected in options,
            'daemon_seccomp_observed': 'seccomp' in options, 'findings': findings}


class ValueSafeArgumentParser(argparse.ArgumentParser):
    def error(self, message):
        self.print_usage(sys.stderr)
        self.exit(2, 'error: use the documented arguments; see --help\n')


def main():
    parser = ValueSafeArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('inspect_json', help='container inspect array file, or - for stdin')
    parser.add_argument('--info', required=True, help='same-context docker info JSON object file')
    parser.add_argument('--daemon-mode', required=True, choices=['rootless', 'userns-remap'])
    args = parser.parse_args()
    if sys.version_info < (3, 12):
        print('error: use Python 3.12 or later', file=sys.stderr)
        return 2
    try:
        if args.inspect_json == args.info == '-':
            raise ValueError('two stdin inputs')
        report = check(load(args.inspect_json), load(args.info), args.daemon_mode)
    except (OSError, UnicodeError, ValueError, RecursionError):
        print('error: supply Docker container inspect JSON and same-context info with SecurityOptions; see --help', file=sys.stderr)
        return 2
    print(json.dumps(report, sort_keys=True))
    return int(bool(report['findings']))


if __name__ == '__main__':
    sys.exit(main())
