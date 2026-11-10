"""Offline native-linter fixtures. No cluster contact and no downloaded schemas."""
import copy
import json
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest
import re

HERE=Path(__file__).resolve().parent
LINTER=shutil.which('kube-linter')
ASSETS=HERE.parents[1]/'skills/kubernetes-workloads/assets'

@unittest.skipUnless(LINTER, 'install the repository-pinned kube-linter and rerun; no linter/runtime claim from this skip')
class WorkloadFixtures(unittest.TestCase):
    def test_native_positive_and_independent_rejections(self):
        base=json.loads((HERE/'fixtures/valid.json').read_text())
        variants=[('valid',base,None)]
        privileged=copy.deepcopy(base)
        privileged['spec']['template']['spec']['containers'][0]['securityContext']['privileged']=True
        variants.append(('privileged',privileged,'privileged-container'))
        missing=copy.deepcopy(base)
        missing['spec']['template']['spec']['containers'][0]['resources']['requests'].pop('cpu')
        variants.append(('missing-request',missing,'cpu-request-unset'))
        memory=copy.deepcopy(base)
        memory['spec']['template']['spec']['containers'][0]['resources']['requests'].pop('memory')
        variants.append(('missing-memory',memory,'memory-request-unset'))
        no_limits=copy.deepcopy(base)
        no_limits['spec']['template']['spec']['containers'][0]['resources'].pop('limits')
        variants.append(('measured-no-limits',no_limits,None))
        for field,rule in [('livenessProbe','no-liveness-probe'),('readinessProbe','no-readiness-probe')]:
            manifest=copy.deepcopy(base)
            manifest['spec']['template']['spec']['containers'][0].pop(field)
            variants.append((rule,manifest,rule))
        for field,rule in [('readOnlyRootFilesystem','no-read-only-root-fs'),
                           ('allowPrivilegeEscalation','privilege-escalation-container')]:
            manifest=copy.deepcopy(base)
            manifest['spec']['template']['spec']['containers'][0]['securityContext'][field]=field=='allowPrivilegeEscalation'
            variants.append((rule,manifest,rule))
        mismatch=copy.deepcopy(base)
        mismatch['spec']['selector']['matchLabels']['app']='different'
        variants.append(('selector-mismatch',mismatch,'mismatching-selector'))
        with tempfile.TemporaryDirectory(prefix='workload-lint-') as directory:
            for name,manifest,rule in variants:
                path=Path(directory)/(name+'.json')
                path.write_text(json.dumps(manifest))
                result=subprocess.run([LINTER,'lint',str(path),'--config',str(ASSETS/'kube-linter.yaml')],text=True,capture_output=True)
                if rule is None:
                    self.assertEqual(result.returncode,0,result.stdout+result.stderr)
                else:
                    self.assertEqual(result.returncode,1,result.stdout+result.stderr)
                    self.assertIn(rule,result.stdout+result.stderr)

    def test_comparison_asset_and_exact_negative_checks(self):
        expected={
            'privileged.yaml':{'privileged-container','privilege-escalation-container','run-as-non-root','no-read-only-root-fs'},
            'missing-requests.yaml':{'cpu-request-unset','memory-request-unset'},
            'mismatched-selector.yaml':{'dangling-service'},
        }
        for name,rules in [('workload.example.yaml',set()),*expected.items()]:
            path=ASSETS/name if not rules else ASSETS/'negative'/name
            result=subprocess.run([LINTER,'lint','--config',str(ASSETS/'kube-linter.yaml'),str(path)],text=True,capture_output=True)
            self.assertEqual(result.returncode,1 if rules else 0,result.stdout+result.stderr)
            found=set(re.findall(r'\(check: ([a-z-]+),',result.stdout+result.stderr))
            self.assertEqual(found,rules,name)
            if rules:
                header=path.read_text().splitlines()[0]
                self.assertTrue(all(rule in header for rule in rules),name)

if __name__=='__main__':
    unittest.main(verbosity=2)
