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

SCRIPT = ROOT/'skills/docker-compose-environments/scripts/check-compose.py'
FIXTURE = 'config.json'
BASE_OPTIONS = ['--expected-project','fixture','--stateful','db']

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

    def test_project_and_volume_identity(self):
        model=copy.deepcopy(self.fixture)
        model['name']='other'
        model['volumes']['data'].pop('name')
        self.assertEqual(self.rules(self.report(model,expected=1)),{'project-identity','volume-identity'})
        model=copy.deepcopy(self.fixture)
        model['services']['db']['volumes'][0].pop('source')
        self.assertIn('anonymous-or-undeclared-volume',self.rules(self.report(model,expected=1)))

    def test_health_and_dependency_conditions(self):
        model=copy.deepcopy(self.fixture)
        model['services']['db']['healthcheck']['disable']=True
        model['services']['app']['depends_on']['db']['condition']='service_started'
        self.assertEqual(self.rules(self.report(model,expected=1)),{'stateful-healthcheck','stateful-ordering'})
        model['services']['app']['depends_on']['db']['condition']='service_healthy'
        self.assertIn('missing-dependency-healthcheck',self.rules(self.report(model,expected=1)))

    def test_exposure_is_declared(self):
        model=copy.deepcopy(self.fixture)
        model['services']['app']['ports'][0].pop('host_ip')
        self.assertIn('public-port',self.rules(self.report(model,expected=1)))
        self.report(model,options=BASE_OPTIONS+['--public-service','app'])
        model['services']['app']['ports'][0]['host_ip']='::1'
        self.report(model)

    def test_secret_value_and_key_are_omitted(self):
        model=copy.deepcopy(self.fixture)
        model['services']['app']['environment']={'API_TOKEN':'SECRET_SENTINEL','DATABASE_URL':'SECRET_SENTINEL'}
        report=self.report(model,expected=1)
        self.assertEqual(self.rules(report),{'credential-environment'})
        self.assertNotIn('API_TOKEN',json.dumps(report))

    def test_wrong_types_and_unknown_declared_service_fail(self):
        model=copy.deepcopy(self.fixture)
        model['services']['app']['environment']=['SECRET_SENTINEL']
        self.assertEqual(self.run_script(model).returncode,2)
        self.assertEqual(self.run_script(options=BASE_OPTIONS+['--stateful','absent']).returncode,2)

    def test_stateful_service_requires_a_persistent_mount(self):
        model=copy.deepcopy(self.fixture)
        model['services']['db'].pop('volumes')
        self.assertIn('stateful-storage',self.rules(self.report(model,expected=1)))
        model['services']['db']['volumes']=[{'type':'tmpfs','target':'/data'}]
        self.assertIn('stateful-storage',self.rules(self.report(model,expected=1)))
        model['services']['db']['volumes']=[{'type':'bind','source':'/fixture-data','target':'/data'}]
        self.report(model)
        model['services']['app']='SECRET_SENTINEL'
        self.assertEqual(self.run_script(model).returncode,2)

    def test_cli_errors_do_not_echo_argument_values(self):
        result=self.run_script(options=BASE_OPTIONS+['--unknown-option=SECRET_SENTINEL'])
        self.assertEqual(result.returncode,2)
        self.assertEqual(result.stdout,'')
        self.assertNotIn('SECRET_SENTINEL',result.stderr)

if __name__ == '__main__':
    unittest.main(verbosity=2)
