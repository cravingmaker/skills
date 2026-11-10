import copy
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]

SCRIPT = ROOT/'skills/kubernetes-troubleshooting/scripts/pod-triage.py'
FIXTURE = 'snapshot.json'
BASE_OPTIONS = []

class Contract(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix='skill-fixture-')
        self.addCleanup(self.temporary.cleanup)
        self.directory = Path(self.temporary.name)
        self.fixture = json.loads((HERE/'fixtures'/FIXTURE).read_text())

    def run_script(self, model=None, raw=None, options=None):
        source = self.directory/'input.json'
        source.write_text(json.dumps(self.fixture if model is None else model) if raw is None else raw)
        before = source.read_bytes()
        result = subprocess.run([sys.executable, str(SCRIPT), str(source), *(BASE_OPTIONS if options is None else options)],
                                text=True, capture_output=True, env=dict(os.environ, PYTHONDONTWRITEBYTECODE='1'))
        self.assertEqual(source.read_bytes(), before, 'checker changed the input')
        self.assertNotIn('SECRET_SENTINEL', result.stdout + result.stderr)
        return result

    def report(self, model=None, expected=0, options=None):
        result = self.run_script(model=model, options=options)
        self.assertEqual(result.returncode, expected, result.stderr + result.stdout)
        self.assertEqual(result.stderr, '')
        return json.loads(result.stdout)

    def rules(self, report):
        return {item['rule'] for item in report['findings']}

    def test_help_does_not_read_inputs(self):
        result = subprocess.run([sys.executable, str(SCRIPT), '--help'], text=True, capture_output=True,
                                cwd=self.directory)
        self.assertEqual(result.returncode, 0)
        self.assertIn('Exit', result.stdout)
        self.assertEqual(list(self.directory.iterdir()), [])

    def test_accept_repeat_and_read_only(self):
        first, second = self.run_script(), self.run_script()
        self.assertEqual(first.returncode, 0, first.stderr + first.stdout)
        self.assertEqual(first.stdout, second.stdout)
        self.assertEqual(first.stderr, '')

    def test_malformed_and_duplicate_inputs_are_not_echoed(self):
        for raw in ('{"SECRET_SENTINEL":', 'null', '[]', '{"items":[],"items":"SECRET_SENTINEL"}', '{"x":NaN}'):
            result = self.run_script(raw=raw)
            self.assertEqual(result.returncode, 2, result.stdout + result.stderr)
            self.assertEqual(result.stdout, '')
            self.assertIn('error:', result.stderr)

    def test_stdin_matches_file_without_echoing_configuration(self):
        result=subprocess.run([sys.executable,str(SCRIPT),'-',*BASE_OPTIONS],
                              input=json.dumps(self.fixture),text=True,capture_output=True)
        self.assertEqual(result.returncode,0,result.stderr+result.stdout)
        self.assertEqual(json.loads(result.stdout),self.report())
        self.assertNotIn('SECRET_SENTINEL',result.stdout+result.stderr)

    def test_missing_input_is_usage(self):
        result = subprocess.run([sys.executable, str(SCRIPT), str(self.directory/'missing'), *BASE_OPTIONS], text=True, capture_output=True)
        self.assertEqual(result.returncode, 2)
        self.assertEqual(result.stdout, '')

    def signals(self, report):
        return {item['signal'] for item in report['signals']}

    def test_exit_137_does_not_claim_oom(self):
        model=copy.deepcopy(self.fixture)
        state=model['items'][0]['status']['containerStatuses'][0]
        state['lastState']={'terminated':{'exitCode':137,'reason':'Error'}}
        report=self.report(model,expected=1)
        self.assertIn('exit-137-cause-unknown',self.signals(report))
        self.assertNotIn('oom-reported',self.signals(report))
        evidence=next(item for item in report['signals'] if item['signal']=='exit-137-cause-unknown')
        self.assertEqual((evidence['container_group'],evidence['container'],evidence['state']),('containerStatuses',1,'lastState'))
        state['lastState']['terminated']['reason']='OOMKilled'
        report=self.report(model,expected=1)
        self.assertIn('oom-reported',self.signals(report))
        self.assertNotIn('exit-137-cause-unknown',self.signals(report))

    def event(self, uid='pod-current', reason='FailedScheduling', message='Insufficient cpu SECRET_SENTINEL'):
        return {'kind':'Event','metadata':{'namespace':'fixture','name':'event-1'},
                'involvedObject':{'kind':'Pod','namespace':'fixture','name':'app-1','uid':uid},
                'reason':reason,'message':message}

    def test_events_bind_to_current_uid(self):
        model=copy.deepcopy(self.fixture)
        model['items'].append(self.event(uid='pod-old'))
        report=self.report(model)
        self.assertEqual(report['ignored_unmatched_events'],1)
        model['items'][-1]=self.event()
        self.assertIn('scheduling-resources',self.signals(self.report(model,expected=1)))
        model['items'][-1]=self.event(message='untolerated taint; unbound PersistentVolumeClaims SECRET_SENTINEL')
        self.assertTrue({'scheduling-taints','scheduling-storage'}<=self.signals(self.report(model,expected=1)))

    def test_backoff_and_init_container_pull_errors_are_symptoms(self):
        model=copy.deepcopy(self.fixture)
        model['items'][0]['status']['initContainerStatuses']=[{'state':{'waiting':{'reason':'ImagePullBackOff'}}}]
        model['items'][0]['status']['containerStatuses'][0]['state']={'waiting':{'reason':'CrashLoopBackOff'}}
        self.assertTrue({'image-pull','restart-backoff'}<=self.signals(self.report(model,expected=1)))

    def test_selector_namespace_and_endpoint_evidence_are_separate(self):
        model=copy.deepcopy(self.fixture)
        model['items'][0]['metadata']['namespace']='other'
        self.assertIn('selector-no-pods',self.signals(self.report(model,expected=1)))
        model=copy.deepcopy(self.fixture)
        model['items'][2]['endpoints'][0]['conditions']['ready']=False
        self.assertIn('no-ready-endpoint',self.signals(self.report(model,expected=1)))
        model['items'].pop()
        self.assertIn('endpoints-not-observed',self.signals(self.report(model,expected=1)))

    def test_rollout_deadline_does_not_auto_rollback(self):
        model=copy.deepcopy(self.fixture)
        model['items'].append({'kind':'Deployment','metadata':{'namespace':'fixture','name':'app'},
            'status':{'conditions':[{'type':'Progressing','status':'False','reason':'ProgressDeadlineExceeded'}]}})
        report=self.report(model,expected=1)
        self.assertIn('progress-deadline-no-auto-rollback',self.signals(report))
        self.assertNotIn('kubectl',json.dumps(report))

    def test_invalid_exit_code_type_fails_without_values(self):
        model=copy.deepcopy(self.fixture)
        model['items'][0]['status']['containerStatuses'][0]['lastState']={'terminated':{'exitCode':'SECRET_SENTINEL'}}
        result=self.run_script(model)
        self.assertEqual(result.returncode,2)
        self.assertEqual(result.stdout,'')

    def test_empty_list_is_missing_evidence(self):
        self.assertEqual(self.signals(self.report({'kind':'List','items':[]},expected=1)),{'missing-pod-evidence'})

    def test_waiting_configuration_runtime_and_image_classes(self):
        expected={'InvalidImageName':'invalid-image-name','CreateContainerConfigError':'configuration-error',
                  'CreateContainerError':'runtime-start-error','RunContainerError':'runtime-start-error'}
        for reason,signal in expected.items():
            model=copy.deepcopy(self.fixture)
            model['items'][0]['status']['containerStatuses'][0]['state']={'waiting':{'reason':reason,'message':'SECRET_SENTINEL'}}
            self.assertIn(signal,self.signals(self.report(model,expected=1)))

    def test_mount_sandbox_eviction_and_typed_probe_events_remain_uid_bound(self):
        cases=[('FailedMount','mount','volume-mount-failure'),('FailedAttachVolume','attach','volume-mount-failure'),
               ('FailedCreatePodSandBox','sandbox','sandbox-failure'),('Evicted','evicted','eviction-reported')]
        cases.extend(('Unhealthy',kind+' probe failed SECRET_SENTINEL',kind+'-probe-failure')
                     for kind in ['liveness','readiness','startup'])
        for reason,message,signal in cases:
            model=copy.deepcopy(self.fixture)
            event=self.event(reason=reason,message=message+' SECRET_SENTINEL')
            model['items'].append(event)
            self.assertIn(signal,self.signals(self.report(model,expected=1)))
            event['involvedObject']['uid']='old-pod'
            self.assertNotIn(signal,self.signals(self.report(model)))
            event['regarding']=event.pop('involvedObject')
            event['regarding']['uid']='pod-current'
            event['note']=event.pop('message')
            self.assertIn(signal,self.signals(self.report(model,expected=1)))

    def test_pvc_and_running_not_ready_are_observations(self):
        model=copy.deepcopy(self.fixture)
        model['items'].append({'kind':'PersistentVolumeClaim','metadata':{'namespace':'fixture','name':'claim'},
                               'status':{'phase':'Pending'}})
        model['items'][0]['status']['containerStatuses'][0]['ready']=False
        model['items'][0]['status']['reason']='Evicted'
        self.assertTrue({'pvc-pending','container-not-ready','eviction-reported'}<=self.signals(self.report(model,expected=1)))

    def test_endpoint_ready_null_or_omitted_follows_the_api(self):
        endpoint=self.fixture['items'][2]['endpoints'][0]
        endpoint['conditions']['ready']=None
        self.report()
        endpoint['conditions'].pop('ready')
        self.report()
        endpoint['conditions']['ready']='SECRET_SENTINEL'
        self.assertEqual(self.run_script().returncode,2)

    def test_cli_errors_do_not_echo_argument_values(self):
        result=self.run_script(options=BASE_OPTIONS+['--unknown-option=SECRET_SENTINEL'])
        self.assertEqual(result.returncode,2)
        self.assertEqual(result.stdout,'')
        self.assertNotIn('SECRET_SENTINEL',result.stderr)

if __name__ == '__main__':
    unittest.main(verbosity=2)
