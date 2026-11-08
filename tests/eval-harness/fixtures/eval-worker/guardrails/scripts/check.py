import pathlib,sys
mode=sys.argv[1]
errors=[]
for p in pathlib.Path('src').rglob('*.ts'):
    for n,line in enumerate(p.read_text().splitlines(),1):
        if mode=='format' and line.rstrip()!=line: errors.append(f'{p}:{n}: remove trailing whitespace')
        if mode=='lint' and 'debugger;' in line: errors.append(f'{p}:{n}: remove debugger statement')
print('\n'.join(errors) if errors else mode+' checks pass')
sys.exit(bool(errors))
