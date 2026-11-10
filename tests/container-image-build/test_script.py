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

SCRIPT = ROOT/'skills/container-image-build/scripts/image-report.py'
FIXTURE = 'image.json'
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

    def test_numeric_nonroot_user(self):
        for value, rule in [('', 'numeric-user'), ('app', 'numeric-user'), ('0', 'root-user'), ('000:1000', 'root-user')]:
            model=copy.deepcopy(self.fixture)
            model[0]['Config']['User']=value
            self.assertIn(rule, self.rules(self.report(model, expected=1)))
        self.fixture[0]['Config']['User']='10001'
        self.report()

    def test_size_delta_and_platform_are_data_not_configuration(self):
        previous=copy.deepcopy(self.fixture)
        previous[0]['Size']=15000
        prior=self.directory/'previous.json'
        prior.write_text(json.dumps(previous))
        report=self.report(options=['--previous',str(prior)])
        self.assertEqual(report['size_delta_bytes'],-3000)
        self.assertEqual(report['layers'],1)
        self.assertEqual(report['platform'],'linux/arm64')
        self.assertNotIn('Env', json.dumps(report))

    def test_wrong_shapes_fail(self):
        for field,value in [('Size',True),('RootFS',[]),('Config',None),('Architecture',None)]:
            model=copy.deepcopy(self.fixture)
            model[0][field]=value
            result=self.run_script(model)
            self.assertEqual(result.returncode,2,result)

    def test_platform_variant_is_retained_and_validated(self):
        self.fixture[0]['Architecture']='arm'
        self.fixture[0]['Variant']='v7'
        self.assertEqual(self.report()['platform'],'linux/arm/v7')
        self.fixture[0]['Variant']='SECRET_SENTINEL/invalid'
        self.assertEqual(self.run_script().returncode,2)

    def test_cli_errors_do_not_echo_argument_values(self):
        result=self.run_script(options=BASE_OPTIONS+['--unknown-option=SECRET_SENTINEL'])
        self.assertEqual(result.returncode,2)
        self.assertEqual(result.stdout,'')
        self.assertNotIn('SECRET_SENTINEL',result.stderr)

if __name__ == '__main__':
    unittest.main(verbosity=2)
