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

SCRIPT = ROOT/'skills/container-runtime-hardening/scripts/check-runtime.py'
FIXTURE = 'containers.json'
BASE_OPTIONS = ['--info',str(HERE/'fixtures/info.json'),'--daemon-mode','rootless']

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

    def test_each_runtime_boundary_is_checked(self):
        cases=[('Privileged',True,'privileged'),('ReadonlyRootfs',False,'writable-root'),
               ('CapDrop',[],'cap-drop'),('CapAdd',['SYS_ADMIN'],'cap-add'),
               ('SecurityOpt',[],'privilege-escalation'),
               ('SecurityOpt',['no-new-privileges=true','seccomp:unconfined'],'unconfined-seccomp'),
               ('PidMode','host','host-namespace'),('UsernsMode','host','host-namespace'),
               ('Devices',[{'PathOnHost':'SECRET_SENTINEL'}],'host-devices')]
        for field,value,rule in cases:
            with self.subTest(field=field,rule=rule):
                model=copy.deepcopy(self.fixture)
                model[0]['HostConfig'][field]=value
                self.assertIn(rule,self.rules(self.report(model,expected=1)))
        model=copy.deepcopy(self.fixture)
        model[0]['Config']['User']='0:1000'
        self.assertIn('numeric-nonroot',self.rules(self.report(model,expected=1)))

    def test_socket_and_parent_mounts_even_read_only(self):
        for source,destination in [('/run','/runtime'),('/var/run/docker.sock','/fixture.sock'),
                                  ('/run/user/1000/docker.sock','/fixture'),('/','/host'),('/x','/run/docker.sock')]:
            model=copy.deepcopy(self.fixture)
            model[0]['Mounts']=[{'Type':'bind','Source':source,'Destination':destination,'RW':False}]
            self.assertIn('control-socket-mount',self.rules(self.report(model,expected=1)))

    def test_tmpfs_directory_is_not_host_socket_exposure(self):
        model=copy.deepcopy(self.fixture)
        model[0]['Mounts']=[{'Type':'tmpfs','Source':'','Destination':'/run','RW':True}]
        self.report(model)

    def test_daemon_mode_and_seccomp_require_evidence(self):
        info=self.directory/'info.json'
        info.write_text(json.dumps({'SecurityOptions':[]}))
        report=self.report(expected=1,options=['--info',str(info),'--daemon-mode','rootless'])
        self.assertEqual(self.rules(report),{'daemon-mode-unproven','daemon-seccomp-unproven'})
        info.write_text(json.dumps({'SecurityOptions':['name=userns','name=seccomp,profile=builtin']}))
        self.report(options=['--info',str(info),'--daemon-mode','userns-remap'])

    def test_invalid_inspect_shapes_fail(self):
        for field,value in [('Mounts',None),('HostConfig',[]),('Config',{})]:
            model=copy.deepcopy(self.fixture)
            model[0][field]=value
            result=self.run_script(model)
            # A missing USER is a policy finding; malformed structure is usage.
            self.assertEqual(result.returncode,1 if field=='Config' else 2,result)

    def test_lsm_uts_and_resource_bounds(self):
        cases=[('SecurityOpt',['no-new-privileges','apparmor=unconfined'],'unconfined-lsm'),
               ('SecurityOpt',['no-new-privileges','label:disable'],'unconfined-lsm'),
               ('UTSMode','host','host-namespace'),('Memory',0,'memory-unbounded')]
        cases.extend(('PidsLimit',value,'pids-unbounded') for value in [None,0,-1])
        for field,value,rule in cases:
            with self.subTest(field=field,value=value):
                model=copy.deepcopy(self.fixture)
                model[0]['HostConfig'][field]=value
                self.assertIn(rule,self.rules(self.report(model,expected=1)))
        for field,value in [('Memory',True),('Memory',-1),('PidsLimit','SECRET_SENTINEL')]:
            model=copy.deepcopy(self.fixture)
            model[0]['HostConfig'][field]=value
            self.assertEqual(self.run_script(model).returncode,2)

    def test_sensitive_host_subpaths_and_more_control_sockets(self):
        for source in ['/etc/shadow','/proc/1','/var/lib/kubelet/pods']:
            model=copy.deepcopy(self.fixture)
            model[0]['Mounts']=[{'Type':'bind','Source':source,'Destination':'/fixture','RW':False}]
            self.assertIn('host-system-mount',self.rules(self.report(model,expected=1)))
        for source in ['/run/crio/crio.sock','/run/buildkit/buildkitd.sock']:
            model=copy.deepcopy(self.fixture)
            model[0]['Mounts']=[{'Type':'bind','Source':source,'Destination':'/fixture','RW':False}]
            self.assertIn('control-socket-mount',self.rules(self.report(model,expected=1)))
        self.fixture[0]['Config']['User']='000:1000'
        self.assertIn('numeric-nonroot',self.rules(self.report(expected=1)))

    def test_cli_errors_do_not_echo_argument_values(self):
        result=self.run_script(options=BASE_OPTIONS+['--unknown-option=SECRET_SENTINEL'])
        self.assertEqual(result.returncode,2)
        self.assertEqual(result.stdout,'')
        self.assertNotIn('SECRET_SENTINEL',result.stderr)

if __name__ == '__main__':
    unittest.main(verbosity=2)
