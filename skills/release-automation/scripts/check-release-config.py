#!/usr/bin/env python3
"""Compare generated candidate versions with release-please or Changesets state.

Python 3.12+ standard library, read-only. --root is the candidate tree, not an
arbitrary development tree. Paths including symlinks must stay inside it.
release-please: state maps package directories to candidate version strings;
each directory has one package.json, Cargo.toml or static pyproject.toml.
changesets: state is status JSON (releases[].name/newVersion); supply candidate
--package paths to package.json. Optional --config checks candidate package membership.
Does not check workflow trust or publication.
Output: JSON findings on stdout, generic setup diagnostics on stderr.
Exit: 0 pass/no release, 1 version/adapter findings, 2 usage/input.
"""

import argparse
import json
import sys
import tomllib
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


def inside(root, relative):
    path = Path(relative)
    if path.is_absolute() or '..' in path.parts:
        raise ValueError('relative path required')
    result = (root / path).resolve()
    if not result.is_relative_to(root):
        raise ValueError('path escapes root')
    return result


def package_version(directory):
    choices = [directory / name for name in ('package.json', 'Cargo.toml', 'pyproject.toml')
               if (directory / name).is_file()]
    if len(choices) != 1:
        return None
    path = choices[0]
    if not path.resolve().is_relative_to(directory):
        raise ValueError('manifest symlink escapes package directory')
    if path.suffix == '.json':
        return load(path).get('version')
    data = tomllib.loads(path.read_text(encoding='utf-8'))
    if path.name == 'Cargo.toml':
        return data.get('package', {}).get('version')
    return data.get('project', {}).get('version') or data.get('tool', {}).get('poetry', {}).get('version')


def check(root, mode, state, packages, config=None):
    if not isinstance(state, dict):
        raise ValueError('state mapping required')
    findings, count = [], 0
    if mode == 'release-please':
        if not state:
            raise ValueError('manifest must contain a package')
        if config is not None:
            configured = config.get('packages') if isinstance(config, dict) else None
            if not isinstance(configured, dict) or not configured:
                raise ValueError('configured package mapping required')
            for directory in configured:
                inside(root, directory)
            if set(configured) != set(state):
                findings.append('manifest: match every configured candidate package path')
        for directory, expected in state.items():
            if not isinstance(expected, str) or not expected:
                raise ValueError('version string required')
            actual = package_version(inside(root, directory))
            count += 1
            if actual != expected:
                findings.append(f'package {count}: match the generated candidate version or use its native adapter')
    else:
        releases = state.get('releases')
        if not isinstance(releases, list):
            raise ValueError('Changesets releases list required')
        actual = {}
        for relative in packages:
            data = load(inside(root, relative))
            name = data.get('name')
            if not isinstance(name, str) or not name or name in actual:
                raise ValueError('unique named package required')
            actual[name] = data.get('version')
        planned = set()
        for entry in releases:
            if not isinstance(entry, dict):
                raise ValueError('release entry required')
            name, expected = entry.get('name'), entry.get('newVersion')
            if not isinstance(name, str) or not name or name in planned or not isinstance(expected, str) or not expected:
                raise ValueError('unique release name and newVersion required')
            planned.add(name)
            count += 1
            if actual.get(name) != expected:
                findings.append(f'package {count}: provide its candidate package.json and match newVersion')
    return {'packages': count, 'findings': findings}


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--root', type=Path, required=True, help='explicit generated candidate directory')
    parser.add_argument('--mode', choices=('release-please', 'changesets'), required=True)
    parser.add_argument('--state', required=True, help='JSON state path relative to candidate root')
    parser.add_argument('--package', action='append', default=[], help='candidate package.json path, for Changesets')
    parser.add_argument('--config', help='release-please config path relative to candidate root')
    args = parser.parse_args()
    if sys.version_info < (3, 12):
        print('error: use Python 3.12 or later', file=sys.stderr)
        return 2
    try:
        root = args.root.resolve(strict=True)
        if not root.is_dir():
            raise ValueError('root must be a directory')
        if args.config and args.mode != 'release-please':
            raise ValueError('--config requires release-please mode')
        config = load(inside(root, args.config)) if args.config else None
        result = check(root, args.mode, load(inside(root, args.state)), args.package, config)
    except (OSError, UnicodeError, ValueError, TypeError, AttributeError, RecursionError):
        print('error: pass readable unique-key candidate state/manifests with paths inside --root; see --help', file=sys.stderr)
        return 2
    print(json.dumps(result, indent=2))
    return 1 if result['findings'] else 0


if __name__ == '__main__':
    sys.exit(main())
