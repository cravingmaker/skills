import json,pathlib,sys
p=pathlib.Path
releases=json.loads(p('registry/releases.json').read_text())
pkg=json.loads(p('package.json').read_text())
command=sys.argv[1]
if command=='releases': print(json.dumps(releases,indent=2))
elif command=='config':
    v=pkg['devDependencies']['@fixture/eslint-plugin']
    rules=releases[v]['rules']|json.loads(p('eslint-policy.json').read_text())['overrides']
    print(json.dumps({'version':v,'rules':rules},indent=2,sort_keys=True))
elif command=='upgrade':
    v=sys.argv[2]
    if v not in releases: raise SystemExit('Unknown fixture version; read registry/releases.json')
    pkg['devDependencies']={k:v for k in pkg['devDependencies']}
    p('package.json').write_text(json.dumps(pkg,indent=2)+'\n')
    p('package-lock.json').write_text(json.dumps({'lockfileVersion':3,'resolved':pkg['devDependencies']},indent=2)+'\n')
    print('Fixture upgrade complete:',v)
elif command=='check':
    lock=json.loads(p('package-lock.json').read_text())
    assert lock['resolved']==pkg['devDependencies'], 'Refresh lockfile'
    print('Fixture package and lock consistency checks pass')
else: raise SystemExit('Use config, releases, upgrade VERSION, or check')
