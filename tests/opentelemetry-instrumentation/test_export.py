"""Offline export mutations, correlation and security-event adapter fixtures."""

import copy
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
CHECK = ROOT / "skills/opentelemetry-instrumentation/scripts/check-otlp-export.py"
POLICY = ROOT / "skills/opentelemetry-instrumentation/assets/telemetry-policy.json"
GOOD = HERE / "fixtures/complete.jsonl"


def attribute(key, value):
    field = "boolValue" if type(value) is bool else "intValue" if type(value) is int else "stringValue"
    return {"key": key, "value": {field: value}}


class Export(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="otlp-fixtures-")
        self.root = Path(self.temp.name)
        self.docs = [json.loads(line) for line in GOOD.read_text().splitlines()]
        self.policy = json.loads(POLICY.read_text())

    def tearDown(self):
        self.temp.cleanup()

    def call(self, docs=None, text=None, policy=None):
        path = self.root / "export.jsonl"
        path.write_text(text if text is not None else "\n".join(
            json.dumps(doc) for doc in (docs if docs is not None else self.docs)))
        policy_path = self.root / "policy.json"
        policy_path.write_text(json.dumps(policy if policy is not None else self.policy))
        return subprocess.run([sys.executable, str(CHECK), "--policy", str(policy_path), str(path)],
                              text=True, capture_output=True, timeout=10)

    def spans(self):
        return self.docs[0]["resourceSpans"][0]["scopeSpans"][0]["spans"]

    def logs(self):
        return self.docs[1]["resourceLogs"][0]["scopeLogs"][0]["logRecords"]

    def points(self):
        return self.docs[2]["resourceMetrics"][0]["scopeMetrics"][0]["metrics"][0]["histogram"]["dataPoints"]

    def expect(self, code):
        result = self.call()
        self.assertEqual(result.returncode, 1, result.stderr + result.stdout)
        self.assertIn(code, {v["code"] for v in json.loads(result.stdout)["findings"]})
        return result

    def test_help_without_file_reads_or_writes(self):
        result = subprocess.run([sys.executable, str(CHECK), "--help"],
                                text=True, capture_output=True, cwd=self.root, timeout=10)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("Exit:", result.stdout)
        self.assertEqual(list(self.root.iterdir()), [])

    def test_accept_repeat_and_read_only(self):
        before = GOOD.read_bytes()
        first = self.call()
        self.assertEqual(first.returncode, 0, first.stderr + first.stdout)
        self.assertEqual(first.stdout, self.call().stdout)
        self.assertEqual(json.loads(first.stdout)["counts"], {"spans": 3, "logs": 2, "metrics": 1})
        self.assertEqual(GOOD.read_bytes(), before)
        self.assertEqual(first.stderr, "")

    def test_single_combined_json_supported(self):
        doc = {}
        for part in self.docs:
            doc.update(part)
        self.assertEqual(self.call([doc]).returncode, 0)

    def test_native_log_event_name_and_conflicting_legacy_name(self):
        for log in self.logs():
            log["eventName"] = "security.access_decision"
            log["attributes"] = [a for a in log["attributes"] if a["key"] != "event.name"]
        self.assertEqual(self.call().returncode, 0)
        self.logs()[0]["attributes"].append(attribute("event.name", "different"))
        self.expect("logs.event_name_conflict")

    def test_missing_required_http_attribute(self):
        self.spans()[0]["attributes"] = [attribute("http.request.method", "POST")]
        self.expect("spans.required_attribute")

    def test_raw_path_span_name_refused(self):
        self.spans()[0]["name"] = "POST /orders/92741"
        self.expect("spans.unexpected_name")

    def test_unbounded_label_name_and_value(self):
        self.points()[0]["attributes"].append(attribute("request.id", "different-every-time"))
        self.expect("metrics.dimension_set")
        self.reset_capture()
        self.points()[0]["attributes"][1] = attribute("http.route", "/orders/92741")
        self.expect("metrics.unbounded_value")

    def reset_capture(self):
        self.docs = [json.loads(line) for line in GOOD.read_text().splitlines()]

    def test_series_limit(self):
        point = copy.deepcopy(self.points()[0])
        point["attributes"][-1] = attribute("http.response.status_code", 503)
        self.points().append(point)
        self.policy["metrics"]["http.server.request.duration"]["max_series"] = 1
        self.expect("metrics.series_limit")

    def test_missing_parent(self):
        self.spans()[1]["parentSpanId"] = "9" * 16
        self.expect("context.missing_parent")

    def test_missing_queue_link(self):
        self.spans()[2]["links"] = []
        self.expect("context.declared_edge_missing")

    def test_existing_link_to_wrong_message_fails_identity_match(self):
        # Both spans exist and the ID link is valid; the message identity differs.
        self.spans()[2]["attributes"][-1] = attribute("app.event.id", "another-event")
        self.expect("context.declared_edge_missing")

    def test_parent_edge_variant(self):
        worker = self.spans()[2]
        worker["traceId"] = self.spans()[1]["traceId"]
        worker["parentSpanId"] = self.spans()[1]["spanId"]
        worker["links"] = []
        self.policy["edges"][0]["relation"] = "parent"
        self.assertEqual(self.call().returncode, 0)

    def test_standalone_logs_need_an_explicit_context_policy(self):
        for log in self.logs():
            log.pop("traceId")
            log.pop("spanId")
        self.expect("context.invalid_id")  # Required request context still fails.
        self.policy["logs"]["security.access_decision"]["require_span_context"] = False
        self.assertEqual(self.call().returncode, 0)
        self.policy.update(spans={}, metrics={}, edges=[])
        self.assertEqual(self.call([self.docs[1]]).returncode, 0)

    def test_optional_log_context_still_validates_supplied_ids(self):
        self.policy["logs"]["security.access_decision"]["require_span_context"] = False
        for log in self.logs():
            log.pop("spanId")
        self.assertEqual(self.call().returncode, 0)  # Trace-only correlation.
        self.logs()[0]["traceId"] = "9" * 32
        self.expect("context.log_trace_missing")
        self.reset_capture()
        self.logs()[0].pop("traceId")
        self.expect("context.invalid_id")  # A span still needs its trace.
        for invalid in ("", 0, False, None):
            self.reset_capture()
            self.logs()[0]["traceId"] = invalid
            self.logs()[0].pop("spanId")
            self.expect("context.invalid_id")

    def test_log_context_policy_rejects_nonboolean_values(self):
        self.policy["logs"]["security.access_decision"]["require_span_context"] = "false"
        self.assertEqual(self.call().returncode, 2)

    def test_log_correlation_and_normalized_ids(self):
        for span in self.spans():
            span["traceId"] = span["traceId"].upper()
            span["spanId"] = span["spanId"].upper()
        self.assertEqual(self.call().returncode, 0)
        self.logs()[0]["spanId"] = "9" * 16
        self.expect("context.log_span_missing")

    def test_security_event_absence(self):
        self.logs().pop()
        self.expect("logs.value_coverage_missing")

    def test_security_event_redaction_nested_value_never_echoed(self):
        self.logs()[0]["body"] = {"stringValue": "SYNTHETIC_SECRET_CANARY"}
        result = self.expect("privacy.secret_value")
        self.assertNotIn("SYNTHETIC_SECRET_CANARY", result.stdout + result.stderr)

    def test_resource_and_link_redaction(self):
        self.docs[0]["resourceSpans"][0]["resource"]["attributes"].append(
            attribute("authorization", "Bearer SYNTHETIC_VALUE"))
        result = self.expect("privacy.forbidden_attribute")
        self.assertNotIn("SYNTHETIC_VALUE", result.stdout + result.stderr)

    def test_grafted_credential_shapes_and_secret_names_are_withheld(self):
        for value in ("AKIA" + "X" * 16, "-----BEGIN PRIVATE KEY-----",
                      "password=synthetic-value"):
            self.reset_capture()
            self.logs()[0]["body"] = {"stringValue": value}
            result = self.expect("privacy.secret_value")
            self.assertNotIn(value, result.stdout + result.stderr)
        self.reset_capture()
        self.spans()[0]["name"] = "Bearer SYNTHETIC_ONLY_CANARY"
        result = self.expect("privacy.secret_value")
        self.assertNotIn("SYNTHETIC_ONLY_CANARY", result.stdout + result.stderr)

    def test_missing_metric_no_points_and_empty_export(self):
        self.points().clear()
        self.expect("metrics.no_points")
        self.docs.pop()
        self.expect("metrics.expected_missing")
        self.assertEqual(self.call(text="").returncode, 2)

    def test_cycle_duplicate_and_invalid_ids(self):
        self.spans()[0]["parentSpanId"] = self.spans()[1]["spanId"]
        self.expect("context.parent_cycle")
        self.reset_capture()
        self.spans().append(copy.deepcopy(self.spans()[0]))
        self.expect("context.duplicate_span")
        self.reset_capture()
        self.spans()[0]["traceId"] = "not-an-id"
        self.expect("context.invalid_id")

    def test_unknown_shapes_bad_policy_and_malformed_json_fail_without_payloads(self):
        for text in ('{"resourceSpans":{}}', '{"other":"SYNTHETIC_SECRET_CANARY"}',
                     '{"resourceSpans":[],"overflow":1e999}',
                     '{"resourceSpans":[],"resourceSpans":[]}', "{", "null"):
            result = self.call(text=text)
            self.assertEqual(result.returncode, 2, result.stdout + result.stderr)
            self.assertEqual(result.stdout, "")
            self.assertNotIn("SYNTHETIC_SECRET_CANARY", result.stderr)
        self.policy["typo"] = 1
        self.assertEqual(self.call().returncode, 2)


if __name__ == "__main__":
    unittest.main()
