"""Offline real JUnit parsing, reject/accept/repeat and secret-safe fixtures."""
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
SCRIPT = HERE.parents[1] / "skills/integration-test-harness/scripts/check-results.py"
PASSED = (HERE / "passed.xml").read_text()
EXPECTED = json.loads((HERE / "expected-cases.json").read_text())


class ResultTests(unittest.TestCase):
    def check_report(self, xml, code=1, expected=None, more=None):
        with tempfile.TemporaryDirectory() as temporary:
            work = Path(temporary)
            report = work / "report.xml"
            report.write_text(xml)
            selection = work / "selection.json"
            selection.write_text(json.dumps(EXPECTED if expected is None else expected))
            args = [sys.executable, str(SCRIPT), str(report)]
            if more is not None:
                second = work / "second.xml"
                second.write_text(more)
                args.append(str(second))
            args += ["--expected-file", str(selection)]
            before = {p.name: p.read_bytes() for p in work.iterdir()}
            outputs = [subprocess.run(args, cwd=work, capture_output=True, text=True) for _ in range(2)]
            self.assertEqual(outputs[0].stdout, outputs[1].stdout)
            for result in outputs:
                self.assertEqual(result.returncode, code, result.stdout + result.stderr)
                self.assertNotIn("SECRET_SENTINEL", result.stdout + result.stderr)
                self.assertNotIn("Traceback", result.stderr)
            self.assertEqual(before, {p.name: p.read_bytes() for p in work.iterdir()})
            return json.loads(outputs[0].stdout) if code != 2 else None

    def test_pass_and_nested_aggregate_not_double_counted(self):
        result = self.check_report(PASSED, 0)
        self.assertEqual(result["cases"], 2)
        self.assertEqual(result["passed"], 2)
        self.assertEqual(result["count_or_setup_errors"], 0)

    def test_empty_all_skipped_and_failures(self):
        self.assertIn("empty_selection", self.check_report('<testsuite tests="0"/>')["findings"])
        for child in ('<skipped/>', '<failure>SECRET_SENTINEL</failure>', '<error>SECRET_SENTINEL</error>'):
            result = self.check_report('<testsuite><testcase classname="stock" name="atomic_increment">' + child + '</testcase></testsuite>')
            self.assertGreater(result["expected_not_passed"], 0)

    def test_missing_wrong_expected_and_misleading_counts(self):
        xml = '<testsuite tests="2"><testcase classname="stock" name="atomic_increment"/></testsuite>'
        result = self.check_report(xml)
        self.assertEqual(result["expected_not_passed"], 1)
        self.assertEqual(result["count_or_setup_errors"], 1)
        self.check_report(PASSED, expected=["stock::missing"])

    def test_failed_unexpected_case_and_duplicates_cannot_hide(self):
        extra = '<testsuite><testcase name="unrelated"><failure>SECRET_SENTINEL</failure></testcase></testsuite>'
        self.assertEqual(self.check_report(PASSED, more=extra)["failed"], 1)
        self.assertEqual(self.check_report(PASSED, more=PASSED)["duplicates"], 2)
        skipped = '<testsuite><testcase name="unrelated"><skipped/></testcase></testsuite>'
        self.assertEqual(self.check_report(PASSED, more=skipped)["skipped"], 1)

    def test_suite_setup_error_and_bad_counts(self):
        self.check_report(PASSED.replace('<system-out>', '<error>').replace('</system-out>', '</error>'))
        for value in ('-1', '1.5', 'SECRET_SENTINEL'):
            self.check_report('<testsuite tests="' + value + '"/>', 2)

    def test_invalid_xml_selection_and_dtd(self):
        for xml in ('<SECRET_SENTINEL', '<other/>', '<!DOCTYPE x [<!ENTITY x "SECRET_SENTINEL">]><testsuite/>', '<testsuite><testcase/></testsuite>'):
            self.check_report(xml, 2)
        for expected in ([], ["stock::a", "stock::a"], [True], ["missing-separator"], ["stock::"]):
            self.check_report(PASSED, 2, expected=expected)

    def test_namespaces_and_help(self):
        namespaced = PASSED.replace('<testsuites ', '<testsuites xmlns="urn:junit" ')
        self.check_report(namespaced, 0)
        result = subprocess.run([sys.executable, str(SCRIPT), "--help"], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0)
        self.assertIn("stdout", result.stdout)

    def test_disabled_result_without_skipped_element_is_not_a_pass(self):
        xml = '<testsuite><testcase classname="stock" name="atomic_increment" status="notrun" result="suppressed"/></testsuite>'
        result = self.check_report(xml)
        self.assertEqual(result["passed"], 0)
        self.assertEqual(result["skipped"], 1)
        unknown = '<testsuite><testcase name="x" status="SECRET_SENTINEL"/></testsuite>'
        self.check_report(unknown, 2)

    def test_node_filtered_file_does_not_satisfy_behavior_selection(self):
        xml = (HERE / "filtered-node.xml").read_text()
        result = self.check_report(xml, expected=["test::orders repository commits a reservation"])
        self.assertEqual(result["passed"], 1)
        self.assertEqual(result["expected_not_passed"], 1)
        self.assertIn("expected_cases_not_passed", result["findings"])


if __name__ == "__main__":
    unittest.main()
