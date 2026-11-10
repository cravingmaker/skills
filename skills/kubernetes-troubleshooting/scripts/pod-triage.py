#!/usr/bin/env python3
"""Classify bounded kubectl JSON evidence; never executes a suggested probe.

Python 3.12+, stdlib only. Input: a kubectl List/resource JSON file or stdin.
Supported: Pods, Events, Deployments, ReplicaSets, Services, EndpointSlices and PVCs.
Output: JSON object indexes, fixed signal/next-probe labels and counts on stdout.
Raw names, messages, logs, selectors, commands and environment values stay private.
Exit: 0 no recognized signals (not a health proof), 1 signals, 2 usage/invalid input.
--help exits 0 without reading input. Read-only; no kubectl or network calls.
"""

import argparse
import json
import sys
from pathlib import Path

KINDS = {'Pod', 'Event', 'Deployment', 'ReplicaSet', 'Service', 'EndpointSlice', 'PersistentVolumeClaim'}
LISTS = {'List'} | {kind + 'List' for kind in KINDS}
WAITING = {
    'ImagePullBackOff': ('image-pull', 'read-pull-error-and-resolved-image-platform'),
    'ErrImagePull': ('image-pull', 'read-pull-error-and-resolved-image-platform'),
    'InvalidImageName': ('invalid-image-name', 'inspect-rendered-image-reference'),
    'CreateContainerConfigError': ('configuration-error', 'check-referenced-config-and-secret-key-existence'),
    'CreateContainerError': ('runtime-start-error', 'compare-entrypoint-platform-permissions-and-node-runtime'),
    'RunContainerError': ('runtime-start-error', 'compare-entrypoint-platform-permissions-and-node-runtime'),
    'CrashLoopBackOff': ('restart-backoff', 'read-previous-container-logs-and-probe-events'),
}


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


def resources(value):
    value = mapping(value)
    kind = value.get('kind')
    if not isinstance(kind, str):
        raise ValueError('missing kind')
    if kind in LISTS:
        result = []
        for item in sequence(value.get('items')):
            result.extend(resources(item))
        return result
    if kind not in KINDS:
        raise ValueError('unsupported kind')
    meta = mapping(value.get('metadata'))
    if not isinstance(meta.get('name'), str) or not meta['name'] or not isinstance(meta.get('namespace', ''), str):
        raise ValueError('missing object identity')
    return [value]


def identity(obj):
    meta = obj['metadata']
    return meta.get('namespace', ''), meta['name']


def endpoint_ready(endpoint):
    ready = mapping(mapping(endpoint).get('conditions', {})).get('ready')
    if ready is not None and type(ready) is not bool:
        raise ValueError('invalid endpoint readiness')
    # The discovery API defines omitted/null readiness as true; it is not app proof.
    return ready is not False


def check(items):
    signals = []

    def signal(index, code, probe, **details):
        record = {'object': index, 'signal': code, 'next_probe': probe, **details}
        if record not in signals:
            signals.append(record)

    pods = {identity(obj): obj for obj in items if obj['kind'] == 'Pod'}
    if not pods:
        signal(0, 'missing-pod-evidence', 'collect-current-pods')
    ignored_events = 0
    for index, obj in enumerate(items, 1):
        kind = obj['kind']
        status = mapping(obj.get('status', {}))
        if kind == 'Pod':
            phase = status.get('phase')
            if not phase:
                signal(index, 'missing-pod-status', 'read-current-pod-status')
            if phase == 'Pending':
                signal(index, 'pending', 'compare-scheduling-volume-and-node-evidence')
            if phase == 'Failed':
                signal(index, 'pod-failed', 'read-termination-and-node-evidence')
            if status.get('reason') == 'Evicted':
                signal(index, 'eviction-reported', 'correlate-node-pressure-and-eviction-evidence')
            for field in ('initContainerStatuses', 'containerStatuses', 'ephemeralContainerStatuses'):
                for container_index, container in enumerate(sequence(status.get(field, [])), 1):
                    container = mapping(container)
                    for state_field in ('state', 'lastState'):
                        state = mapping(container.get(state_field, {}))
                        terminated = mapping(state.get('terminated', {}))
                        waiting = mapping(state.get('waiting', {}))
                        details = {'container_group': field, 'container': container_index, 'state': state_field}
                        if 'exitCode' in terminated and type(terminated['exitCode']) is not int:
                            raise ValueError('invalid exit code')
                        reason = waiting.get('reason')
                        if isinstance(reason, str) and reason in WAITING:
                            code, probe = WAITING[reason]
                            signal(index, code, probe, **details)
                        if terminated.get('reason') == 'OOMKilled':
                            signal(index, 'oom-reported', 'correlate-memory-limit-usage-and-node-evidence', **details)
                        elif terminated.get('exitCode') == 137:
                            signal(index, 'exit-137-cause-unknown', 'correlate-kill-timeout-eviction-and-memory-evidence', **details)
                        elif type(terminated.get('exitCode')) is int and terminated['exitCode'] != 0:
                            signal(index, 'nonzero-exit', 'read-bounded-previous-logs-and-termination-reason', **details)
                    if container.get('ready') is False and 'running' in mapping(container.get('state', {})):
                        signal(index, 'container-not-ready', 'inspect-readiness-contract-and-events',
                               container_group=field, container=container_index)
        elif kind == 'Event':
            ref = mapping(obj.get('involvedObject', obj.get('regarding', {})))
            if ref.get('kind') == 'Pod':
                pod = pods.get((ref.get('namespace', obj['metadata'].get('namespace', '')), ref.get('name')))
                if not pod or not ref.get('uid') or pod['metadata'].get('uid') != ref['uid']:
                    ignored_events += 1
                    continue
            else:
                # Do not attribute unmatched event objects to the workload snapshot.
                if not any(other['kind'] == ref.get('kind') and identity(other) ==
                           (ref.get('namespace', obj['metadata'].get('namespace', '')), ref.get('name')) for other in items):
                    ignored_events += 1
                    continue
            reason, message = obj.get('reason'), obj.get('message', obj.get('note', ''))
            if not isinstance(message, str):
                raise ValueError('invalid event message')
            if reason == 'FailedScheduling':
                message = message.lower()
                choices = [('insufficient', 'scheduling-resources', 'compare-requests-to-allocatable'),
                           ('taint', 'scheduling-taints', 'compare-taints-and-tolerations'),
                           ('persistentvolumeclaim', 'scheduling-storage', 'inspect-pvc-binding-events')]
                matched = False
                for word, code, probe in choices:
                    if word in message:
                        signal(index, code, probe)
                        matched = True
                if not matched:
                    signal(index, 'scheduling-other', 'compare-affinity-topology-quota-and-node-conditions')
            if reason == 'Unhealthy':
                probe_type = next((kind for kind in ('liveness', 'readiness', 'startup')
                                   if message.lower().startswith(kind + ' probe')), None)
                signal(index, probe_type + '-probe-failure' if probe_type else 'probe-failure',
                       'identify-probe-type-endpoint-and-timing')
            if reason in ('FailedMount', 'FailedAttachVolume'):
                signal(index, 'volume-mount-failure', 'inspect-claim-attachment-and-config-reference-events')
            if reason == 'FailedCreatePodSandBox':
                signal(index, 'sandbox-failure', 'inspect-node-runtime-and-cni-evidence')
            if reason == 'Evicted':
                signal(index, 'eviction-reported', 'correlate-node-pressure-and-eviction-evidence')
        elif kind == 'PersistentVolumeClaim':
            if status.get('phase') == 'Pending':
                signal(index, 'pvc-pending', 'inspect-storageclass-provisioner-and-binding-events')
        elif kind == 'Deployment':
            for condition in sequence(status.get('conditions', [])):
                condition = mapping(condition)
                if condition.get('type') == 'Progressing' and condition.get('status') == 'False' and condition.get('reason') == 'ProgressDeadlineExceeded':
                    signal(index, 'progress-deadline-no-auto-rollback', 'compare-replicas-pods-and-delivery-controller')
        elif kind == 'Service':
            spec = mapping(obj.get('spec', {}))
            selector = mapping(spec.get('selector', {}))
            if selector and not any(identity(pod)[0] == identity(obj)[0] and
                                    all(mapping(pod['metadata'].get('labels', {})).get(k) == v for k, v in selector.items())
                                    for pod in pods.values()):
                signal(index, 'selector-no-pods', 'compare-service-selector-with-namespaced-pod-labels')
            if spec.get('type') != 'ExternalName':
                endpoints = [entry for entry in items if entry['kind'] == 'EndpointSlice' and
                             identity(entry)[0] == identity(obj)[0] and
                             mapping(entry['metadata'].get('labels', {})).get('kubernetes.io/service-name') == obj['metadata']['name']]
                if not endpoints:
                    signal(index, 'endpoints-not-observed', 'collect-service-endpointslices')
                elif not any(endpoint_ready(endpoint)
                             for entry in endpoints for endpoint in sequence(entry.get('endpoints', []))):
                    signal(index, 'no-ready-endpoint', 'inspect-endpointslice-readiness-and-target-ports')
    return {'objects': len(items), 'ignored_unmatched_events': ignored_events, 'signals': signals}


class ValueSafeArgumentParser(argparse.ArgumentParser):
    def error(self, message):
        self.print_usage(sys.stderr)
        self.exit(2, 'error: use the documented arguments; see --help\n')


def main():
    parser = ValueSafeArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('snapshot_json', help='kubectl List/resource JSON file, or - for stdin')
    args = parser.parse_args()
    if sys.version_info < (3, 12):
        print('error: use Python 3.12 or later', file=sys.stderr)
        return 2
    try:
        raw = sys.stdin.read() if args.snapshot_json == '-' else Path(args.snapshot_json).read_text(encoding='utf-8')
        report = check(resources(json.loads(raw, object_pairs_hook=unique, parse_constant=reject_constant)))
    except (OSError, UnicodeError, ValueError, RecursionError, TypeError):
        print('error: supply a native kubectl JSON List or supported resource with metadata; see --help', file=sys.stderr)
        return 2
    print(json.dumps(report, sort_keys=True))
    return int(bool(report['signals']))


if __name__ == '__main__':
    sys.exit(main())
