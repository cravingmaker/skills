#!/usr/bin/env python3
"""Check independent exact package identities in an SBOM, read-only.

Python 3.12+ standard library. Input: native-schema-validated CycloneDX component
JSON or SPDX package JSON, and --expected nonempty [{"purl":...,"version":...}].
Expected inventory must come independently from the same final runtime/platform.
Supports package projections only, not all schema revisions. This is NOT a
signature verifier, artifact binding, or proof that a partial inventory is complete.
Output: JSON findings on stdout; generic input diagnostics on stderr.
Exit: 0 pass, 1 missing/conflicting components, 2 usage/input. --help does no IO.
"""

import argparse
import json
import sys
from collections import defaultdict
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


def cdx_components(nodes):
    if not isinstance(nodes, list):
        raise ValueError('components list required')
    for node in nodes:
        if not isinstance(node, dict):
            raise ValueError('component mapping required')
        if 'purl' in node:
            yield node['purl'], node.get('version')
        yield from cdx_components(node.get('components', []))


def extract(document):
    if not isinstance(document, dict):
        raise ValueError('SBOM mapping required')
    if document.get('bomFormat') == 'CycloneDX':
        yield from cdx_components(document.get('components', []))
        root = document.get('metadata', {}).get('component')
        if root is not None:
            yield from cdx_components([root])
    elif isinstance(document.get('spdxVersion'), str):
        packages = document.get('packages')
        if not isinstance(packages, list):
            raise ValueError('packages list required')
        for package in packages:
            if not isinstance(package, dict) or not isinstance(package.get('externalRefs', []), list):
                raise ValueError('package mapping required')
            for ref in package.get('externalRefs', []):
                if not isinstance(ref, dict):
                    raise ValueError('external reference mapping required')
                if ref.get('referenceType') == 'purl':
                    yield ref.get('referenceLocator'), package.get('versionInfo')
    else:
        raise ValueError('unsupported SBOM projection')


def check(document, expected):
    if not isinstance(expected, list) or not expected:
        raise ValueError('nonempty expected inventory required')
    wanted = set()
    for item in expected:
        if not isinstance(item, dict) or set(item) != {'purl', 'version'}:
            raise ValueError('expected purl and version required')
        if not all(isinstance(item[k], str) and item[k] for k in item) or not item['purl'].startswith('pkg:'):
            raise ValueError('exact package identity required')
        key = (item['purl'], item['version'])
        if key in wanted:
            raise ValueError('duplicate expected component')
        wanted.add(key)
    actual, findings = defaultdict(set), []
    for index, (purl, version) in enumerate(extract(document), 1):
        if not isinstance(purl, str) or not purl.startswith('pkg:'):
            raise ValueError('package URL required')
        if not isinstance(version, str) or not version:
            findings.append(f'component {index}: record its exact version')
            continue
        actual[purl].add(version)
    for index, (purl, version) in enumerate(sorted(wanted), 1):
        versions = actual.get(purl, set())
        if version not in versions:
            findings.append(f'expected component {index}: include the independently observed package and version')
        elif versions != {version}:
            findings.append(f'expected component {index}: resolve conflicting versions for the exact package URL')
    return {'expected': len(wanted), 'observed_purls': len(actual), 'findings': findings}


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('sbom', type=Path)
    parser.add_argument('--expected', type=Path, required=True, help='independently captured runtime package identities')
    args = parser.parse_args()
    if sys.version_info < (3, 12):
        print('error: use Python 3.12 or later', file=sys.stderr)
        return 2
    try:
        result = check(load(args.sbom), load(args.expected))
    except (OSError, UnicodeError, ValueError, TypeError, AttributeError, RecursionError):
        print('error: pass supported unique-key SBOM JSON and a nonempty independent purl/version inventory; see --help', file=sys.stderr)
        return 2
    print(json.dumps(result, indent=2))
    return 1 if result['findings'] else 0


if __name__ == '__main__':
    sys.exit(main())
