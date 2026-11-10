#!/usr/bin/env python3
"""Verify strict action SHA pins against live upstream GitHub tag refs.

Python 3.12+ standard library. Read-only GET requests to api.github.com.
Input: actual YAML-parser workflow/action JSON files; --tags maps each remote
uses string to its reviewed release tag. Include local action documents too.
GH_TOKEN is optional and is never printed. No native lockfile/GHES support.
Docker digests get syntax checks only; local actions need source review.
Output: JSON findings/commit IDs on stdout; generic API/input errors on stderr.
Exit: 0 pass, 1 findings, 2 usage/API/input. --help does no IO.
"""

import argparse
import json
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

SHA = re.compile(r'[0-9a-f]{40}', re.ASCII)
REMOTE = re.compile(r'([A-Za-z0-9_.-]+)/([A-Za-z0-9_.-]+)(/[^@\s]+)?@([^@\s]+)', re.ASCII)
DOCKER = re.compile(r'docker://[^@\s]+@sha256:[0-9a-f]{64}', re.ASCII)


def unique(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError('duplicate key')
        result[key] = value
    return result


def load(path):
    return json.loads(path.read_text(encoding='utf-8'), object_pairs_hook=unique)


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


def fetch(endpoint):
    headers = {'Accept': 'application/vnd.github+json', 'User-Agent': 'owned-skills-pin-resolver'}
    token = os.environ.get('GH_TOKEN')
    if token:
        headers['Authorization'] = 'Bearer ' + token
    request = urllib.request.Request('https://api.github.com/' + endpoint, headers=headers, method='GET')
    opener = urllib.request.build_opener(NoRedirect())
    with opener.open(request, timeout=20) as response:
        return json.load(response, object_pairs_hook=unique)


def tag_commit(repository, tag):
    ref = fetch(f'repos/{repository}/git/ref/tags/' + urllib.parse.quote(tag, safe=''))
    if ref.get('ref') != 'refs/tags/' + tag:
        raise ValueError('exact tag not found')
    obj = ref.get('object', {})
    seen = set()
    for _ in range(10):
        sha = obj.get('sha')
        if not isinstance(sha, str) or not SHA.fullmatch(sha) or sha in seen:
            raise ValueError('invalid tag object')
        seen.add(sha)
        if obj.get('type') == 'commit':
            return sha
        if obj.get('type') != 'tag':
            raise ValueError('tag must reach a commit')
        obj = fetch(f'repos/{repository}/git/tags/{sha}').get('object', {})
    raise ValueError('tag chain too deep')


def uses_in(value):
    if isinstance(value, dict):
        for key, child in value.items():
            if key == 'uses':
                yield child
            else:
                yield from uses_in(child)
    elif isinstance(value, list):
        for child in value:
            yield from uses_in(child)


def check(documents, tags):
    if not isinstance(tags, dict) or not all(isinstance(v, str) and v for v in tags.values()):
        raise ValueError('tag mapping required')
    findings, resolved, count, cache = [], [], 0, {}
    for document in documents:
        if not isinstance(document, dict):
            raise ValueError('document mapping required')
        for use in uses_in(document):
            count += 1
            label = f'reference {count}'
            if not isinstance(use, str):
                raise ValueError('uses must be strings')
            if use.startswith('./'):
                if '..' in use.split('/'):
                    findings.append(label + ': keep local action paths inside the checkout')
                continue
            if use.startswith('docker://'):
                if not DOCKER.fullmatch(use):
                    findings.append(label + ': resolve and pin the container action by digest')
                continue
            match = REMOTE.fullmatch(use)
            if not match or not SHA.fullmatch(match[4]):
                findings.append(label + ': resolve a full upstream commit SHA before checking')
                continue
            tag = tags.get(use)
            if not tag:
                findings.append(label + ': provide the reviewed upstream tag in --tags')
                continue
            repository = match[1] + '/' + match[2]
            key = (repository, tag)
            if key not in cache:
                cache[key] = tag_commit(repository, tag)
            if cache[key] != match[4]:
                findings.append(label + ': investigate tag/commit mismatch; do not update blindly')
            else:
                resolved.append({'reference': count, 'sha': match[4]})
    return {'references': count, 'resolved': resolved, 'findings': findings}


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('document', nargs='+', type=Path, help='YAML-parser workflow or local action JSON')
    parser.add_argument('--tags', required=True, type=Path, help='remote uses to reviewed upstream tag mapping')
    args = parser.parse_args()
    if sys.version_info < (3, 12):
        print('error: use Python 3.12 or later', file=sys.stderr)
        return 2
    try:
        result = check([load(p) for p in args.document], load(args.tags))
    except (OSError, UnicodeError, ValueError, TypeError, AttributeError, RecursionError, urllib.error.URLError):
        print('error: use readable JSON and an available GitHub API; configure GH_TOKEN with the existing secret mechanism if required; see --help', file=sys.stderr)
        return 2
    print(json.dumps(result, indent=2))
    return 1 if result['findings'] else 0


if __name__ == '__main__':
    sys.exit(main())
