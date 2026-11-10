#!/usr/bin/env python3
"""Summarize one docker image inspect result without dumping image configuration.

Python 3.12+, stdlib only. Read-only; no Docker, network, build or host calls.
Input: the nonempty one-image JSON array emitted by docker image inspect.
Output: JSON sizes, layer count, platform and fixed policy findings on stdout.
Diagnostics on stderr omit input values. --help exits 0 without reading input.
Exit: 0 checks pass, 1 findings, 2 invalid input, usage or unsupported Python.
A configured numeric nonroot USER does not prove the effective runtime identity.
"""

import argparse
import json
import re
import sys
from pathlib import Path


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
    items = json.loads(raw, object_pairs_hook=unique, parse_constant=reject_constant)
    if not isinstance(items, list) or len(items) != 1 or not isinstance(items[0], dict):
        raise ValueError('one image required')
    image = items[0]
    if not isinstance(image.get('Config'), dict) or not isinstance(image.get('RootFS'), dict):
        raise ValueError('image inspect fields required')
    if type(image.get('Size')) is not int or image['Size'] < 0:
        raise ValueError('invalid size')
    layers = image['RootFS'].get('Layers')
    if not isinstance(layers, list) or any(not isinstance(v, str) for v in layers):
        raise ValueError('invalid layers')
    if not isinstance(image['Config'].get('User', ''), str):
        raise ValueError('invalid user')
    for field in ('Os', 'Architecture'):
        if not isinstance(image.get(field), str) or not re.fullmatch(r'[a-z0-9_.-]+', image[field]):
            raise ValueError('missing platform')
    if 'Variant' in image and (not isinstance(image['Variant'], str) or
                               not re.fullmatch(r'[a-z0-9_.-]*', image['Variant'])):
        raise ValueError('invalid platform variant')
    return image


class ValueSafeArgumentParser(argparse.ArgumentParser):
    def error(self, message):
        self.print_usage(sys.stderr)
        self.exit(2, 'error: use the documented arguments; see --help\n')


def main():
    parser = ValueSafeArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('inspect_json', help='one-image inspect JSON file, or - for stdin')
    parser.add_argument('--previous', help='previous one-image inspect JSON for a byte delta')
    args = parser.parse_args()
    if sys.version_info < (3, 12):
        print('error: use Python 3.12 or later', file=sys.stderr)
        return 2
    try:
        if args.inspect_json == '-' and args.previous == '-':
            raise ValueError('two stdin inputs')
        image = load(args.inspect_json)
        previous = load(args.previous) if args.previous else None
        user = image['Config'].get('User', '')
        findings = []
        if not re.fullmatch(r'[0-9]+(?::[0-9]+)?', user):
            findings.append({'rule': 'numeric-user', 'fix': 'Set an explicit numeric nonzero runtime USER.'})
        elif int(user.split(':', 1)[0]) == 0:
            findings.append({'rule': 'root-user', 'fix': 'Use a nonzero numeric UID and test volume ownership.'})
        report = {'size_bytes': image['Size'], 'layers': len(image['RootFS']['Layers']),
                  'platform': '/'.join(part for part in (image['Os'], image['Architecture'], image.get('Variant')) if part),
                  'size_delta_bytes': image['Size'] - previous['Size'] if previous else None,
                  'findings': findings}
    except (OSError, UnicodeError, ValueError, RecursionError):
        print('error: supply readable UTF-8 one-image docker image inspect JSON; see --help', file=sys.stderr)
        return 2
    print(json.dumps(report, sort_keys=True))
    return int(bool(findings))


if __name__ == '__main__':
    sys.exit(main())
