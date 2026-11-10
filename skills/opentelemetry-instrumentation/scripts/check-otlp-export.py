#!/usr/bin/env python3
"""Check a complete synthetic OTLP JSON/JSONL capture against a fixture policy.

Python 3.12+ standard library; read-only, offline, no prompts.
Usage: check-otlp-export.py --policy POLICY.json EXPORT [EXPORT ...]
stdout: JSON signal counts and finding codes/structural locations; no payloads.
stderr: usage/input diagnostics. Exit: 0 pass, 1 findings, 2 malformed input.
This checks the declared fixture contract, not every semantic convention or
production secret/cardinality risk. See references/export-checks.md.
"""

import argparse
import json
import math
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

SIGNALS = {
    "spans": ("resourceSpans", "scopeSpans", "spans"),
    "metrics": ("resourceMetrics", "scopeMetrics", "metrics"),
    "logs": ("resourceLogs", "scopeLogs", "logRecords"),
}
SECRET = re.compile(
    r"\bbearer\s+[a-z0-9._~+/-]{8,}|"
    r"\b[a-z][a-z0-9+.-]*://[^\s/:]+:[^\s/@]+@|"
    r"\beyJ[a-z0-9_-]+\.[a-z0-9_-]+\.[a-z0-9_-]+|"
    r"\bAKIA[0-9A-Z]{16}\b|-----BEGIN [A-Z ]*PRIVATE KEY-----|"
    r"\b(?:password|passwd|secret|api[_-]?key|access[_-]?token)=[^&\s]{4,}",
    re.I,
)


def unique(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("duplicate JSON key")
        result[key] = value
    return result


def reject_constant(_):
    raise ValueError("nonfinite JSON")


def finite_float(value):
    result = float(value)
    if not math.isfinite(result):
        raise ValueError("nonfinite JSON")
    return result


def decode(text):
    return json.loads(text, object_pairs_hook=unique, parse_constant=reject_constant,
                      parse_float=finite_float)


def obj(value):
    if not isinstance(value, dict):
        raise ValueError("expected object")
    return value


def array(value):
    if not isinstance(value, list):
        raise ValueError("expected array")
    return value


def strings(value):
    if not isinstance(value, list) or any(not isinstance(x, str) or not x for x in value):
        raise ValueError("expected nonempty strings in array")
    return value


def scalar(value):
    value = obj(value)
    if len(value) != 1:
        raise ValueError("expected one OTLP AnyValue field")
    kind, item = next(iter(value.items()))
    if kind == "intValue":
        if type(item) not in (int, str) or isinstance(item, str) and not re.fullmatch(r"-?\d+", item):
            raise ValueError("invalid integer")
        return int(item)
    if kind in {"stringValue", "bytesValue"} and isinstance(item, str):
        return item
    if kind == "boolValue" and type(item) is bool:
        return item
    if kind == "doubleValue" and type(item) in (int, float):
        return item
    if kind in {"arrayValue", "kvlistValue"} and isinstance(item, dict):
        return item
    raise ValueError("unsupported OTLP AnyValue")


def attributes(record):
    result = {}
    for attribute in array(obj(record).get("attributes", [])):
        attribute = obj(attribute)
        key = attribute.get("key")
        if not isinstance(key, str) or not key or key in result:
            raise ValueError("invalid or repeated attribute key")
        result[key] = scalar(attribute.get("value"))
    return result


def canon(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False)


def validate_policy(policy):
    keys = {"spans", "metrics", "logs", "edges", "resource_required_attributes",
            "forbidden_keys", "redaction_canaries"}
    if set(obj(policy)) != keys:
        raise ValueError("policy fields differ from documented asset")
    for key in ("resource_required_attributes", "forbidden_keys", "redaction_canaries"):
        strings(policy[key])
    if not any(obj(policy[signal]) for signal in SIGNALS):
        raise ValueError("empty policy")
    for signal in SIGNALS:
        for name, rule in obj(policy[signal]).items():
            if not isinstance(name, str) or not name:
                raise ValueError("empty signal name")
            rule = obj(rule)
            expected = {"attributes", "max_series"} if signal == "metrics" else {"required_attributes"}
            if signal == "logs":
                expected |= {"required_values"}
                if "require_span_context" in rule:
                    expected.add("require_span_context")
                    if type(rule["require_span_context"]) is not bool:
                        raise ValueError("require_span_context must be boolean")
            if set(rule) != expected:
                raise ValueError("unknown or missing rule field")
            if signal != "metrics":
                strings(rule["required_attributes"])
            dimensions = rule.get("attributes", rule.get("required_values", {}))
            for key, values in obj(dimensions).items():
                if not key or not array(values):
                    raise ValueError("empty finite value set")
                if any(type(v) not in (str, int, float, bool) for v in values):
                    raise ValueError("dimension must be scalar")
            if signal == "metrics" and (type(rule["max_series"]) is not int or rule["max_series"] < 1):
                raise ValueError("invalid series bound")
    for edge in array(policy["edges"]):
        if set(obj(edge)) != {"source", "target", "relation", "match_attributes"}:
            raise ValueError("invalid edge fields")
        strings(edge["match_attributes"])
        if edge["source"] not in policy["spans"] or edge["target"] not in policy["spans"]:
            raise ValueError("edge needs declared spans")
        if edge["relation"] not in {"parent", "link"}:
            raise ValueError("invalid edge relation")


def documents(text):
    try:
        return [obj(decode(text))]
    except json.JSONDecodeError:
        lines = [line for line in text.splitlines() if line.strip()]
        if not lines:
            raise ValueError("empty input")
        return [obj(decode(line)) for line in lines]


def records(document):
    found = False
    for signal, (resource_key, scope_key, record_key) in SIGNALS.items():
        if resource_key not in document:
            continue
        found = True
        for ri, resource in enumerate(array(document[resource_key])):
            resource = obj(resource)
            resource_attrs = attributes(obj(resource.get("resource", {})))
            for si, scope in enumerate(array(resource.get(scope_key))):
                for ei, record in enumerate(array(obj(scope).get(record_key))):
                    yield signal, f"{resource_key}[{ri}].{scope_key}[{si}].{record_key}[{ei}]", obj(record), resource_attrs
    if not found:
        raise ValueError("no supported resource signal")


def inspect(policy, docs):
    findings, spans, logs = [], [], []
    forbidden = {key.casefold() for key in policy["forbidden_keys"]}
    counts = {signal: Counter() for signal in SIGNALS}
    series, log_values = defaultdict(set), defaultdict(set)
    def fail(code, location):
        findings.append({"code": code, "location": location})
    def redact(value, location):
        if isinstance(value, dict):
            if isinstance(value.get("key"), str) and value["key"].casefold() in forbidden:
                fail("privacy.forbidden_attribute", location)
            for index, (key, item) in enumerate(value.items()):
                if key.casefold() in forbidden:
                    fail("privacy.forbidden_field", location)
                redact(item, f"{location}.object[{index}]")
        elif isinstance(value, list):
            for index, item in enumerate(value):
                redact(item, f"{location}[{index}]")
        elif isinstance(value, str):
            if SECRET.search(value) or any(c in value for c in policy["redaction_canaries"]):
                fail("privacy.secret_value", location)
    def identifier(value, length, location):
        if not isinstance(value, str) or not re.fullmatch(rf"[0-9a-fA-F]{{{length}}}", value) or not int(value, 16):
            fail("context.invalid_id", location)
            return None
        return value.lower()
    for di, document in enumerate(docs):
        redact(document, f"input[{di}]")
        for signal, location, record, resource_attrs in records(document):
            location = f"input[{di}].{location}"
            if any(key not in resource_attrs for key in policy["resource_required_attributes"]):
                fail("resource.required_attribute", location)
            attrs = attributes(record)
            if signal == "logs":
                native = record.get("eventName")
                if native is not None and not isinstance(native, str):
                    raise ValueError("eventName must be a string")
                if native:
                    if attrs.get("event.name", native) != native:
                        fail("logs.event_name_conflict", location)
                    attrs["event.name"] = native
            name = attrs.get("event.name") if signal == "logs" else record.get("name")
            if not isinstance(name, str):
                raise ValueError("signal name missing")
            counts[signal][name] += 1
            rule = policy[signal].get(name)
            if rule is None:
                fail(f"{signal}.unexpected_name", location)
            elif any(key not in attrs for key in rule.get("required_attributes", [])):
                fail(f"{signal}.required_attribute", location)
            if signal == "spans":
                if "kind" in record and (type(record["kind"]) is not int or not 0 <= record["kind"] <= 5):
                    raise ValueError("use integer OTLP span kind")
                trace = identifier(record.get("traceId"), 32, location)
                span = identifier(record.get("spanId"), 16, location)
                parent = record.get("parentSpanId")
                parent = None if not parent or parent == "0" * 16 else identifier(parent, 16, location)
                links = []
                for link in array(record.get("links", [])):
                    link = obj(link)
                    links.append((identifier(link.get("traceId"), 32, location),
                                  identifier(link.get("spanId"), 16, location)))
                spans.append({"key": (trace, span), "parent": (trace, parent) if parent else None,
                              "links": links, "name": name, "location": location, "attrs": attrs})
            elif signal == "logs":
                required = rule.get("require_span_context", True) if rule else True
                has_trace, has_span = "traceId" in record, "spanId" in record
                trace = identifier(record.get("traceId"), 32, location) if has_trace or has_span or required else None
                span = identifier(record.get("spanId"), 16, location) if has_span or required else None
                if has_trace or has_span or required:
                    logs.append((trace, span, location))
                if rule:
                    for key, allowed in rule["required_values"].items():
                        value = canon(attrs.get(key))
                        log_values[(name, key)].add(value)
                        if value not in {canon(v) for v in allowed}:
                            fail("logs.unexpected_value", location)
            else:
                data = [record[key] for key in ("gauge", "sum", "histogram", "exponentialHistogram", "summary") if key in record]
                if len(data) != 1:
                    raise ValueError("expected one supported metric type")
                points = array(obj(data[0]).get("dataPoints"))
                if not points:
                    fail("metrics.no_points", location)
                for point in points:
                    point_attrs = attributes(point)
                    series[name].add(canon(point_attrs))
                    if rule:
                        allowed = rule["attributes"]
                        if set(point_attrs) != set(allowed):
                            fail("metrics.dimension_set", location)
                        for key, value in point_attrs.items():
                            if key not in allowed or canon(value) not in {canon(v) for v in allowed[key]}:
                                fail("metrics.unbounded_value", location)
    by_key = {}
    for span in spans:
        if span["key"] in by_key:
            fail("context.duplicate_span", span["location"])
        by_key[span["key"]] = span
    for span in spans:
        if span["parent"] and span["parent"] not in by_key:
            fail("context.missing_parent", span["location"])
        if any(key not in by_key for key in span["links"]):
            fail("context.missing_link", span["location"])
        visited, current = set(), span
        while current:
            if current["key"] in visited:
                fail("context.parent_cycle", span["location"])
                break
            visited.add(current["key"])
            current = by_key.get(current["parent"])
    for trace, span, location in logs:
        if span is None:
            if not any(key[0] == trace for key in by_key):
                fail("context.log_trace_missing", location)
        elif (trace, span) not in by_key:
            fail("context.log_span_missing", location)
    for ei, edge in enumerate(policy["edges"]):
        for target in (s for s in spans if s["name"] == edge["target"]):
            related = [target["parent"]] if edge["relation"] == "parent" else target["links"]
            if not any(
                key in by_key and by_key[key]["name"] == edge["source"]
                and all(
                    attr in target["attrs"] and attr in by_key[key]["attrs"]
                    and canon(target["attrs"][attr]) == canon(by_key[key]["attrs"][attr])
                    for attr in edge["match_attributes"]
                )
                for key in related
            ):
                fail("context.declared_edge_missing", f"policy.edges[{ei}]")
    for signal in SIGNALS:
        for index, (name, rule) in enumerate(policy[signal].items()):
            location = f"policy.{signal}[{index}]"
            if not counts[signal][name]:
                fail(f"{signal}.expected_missing", location)
            if signal == "metrics" and len(series[name]) > rule["max_series"]:
                fail("metrics.series_limit", location)
            if signal == "logs":
                for key, required in rule["required_values"].items():
                    if not {canon(v) for v in required} <= log_values[(name, key)]:
                        fail("logs.value_coverage_missing", location)
    return {"counts": {signal: sum(counts[signal].values()) for signal in SIGNALS},
            "findings": findings}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--policy", required=True, type=Path)
    parser.add_argument("exports", nargs="+", type=Path)
    args = parser.parse_args()
    if sys.version_info < (3, 12):
        print("error: use Python 3.12 or later", file=sys.stderr)
        return 2
    try:
        policy = decode(args.policy.read_text(encoding="utf-8"))
        validate_policy(policy)
        docs = [doc for path in args.exports for doc in documents(path.read_text(encoding="utf-8"))]
        result = inspect(policy, docs)
    except (OSError, UnicodeError, ValueError, TypeError, KeyError, RecursionError, OverflowError):
        print("error: use valid policy and supported OTLP JSON/JSONL shapes; see --help and export-checks.md", file=sys.stderr)
        return 2
    print(json.dumps(result, sort_keys=True))
    return 1 if result["findings"] else 0


if __name__ == "__main__":
    sys.exit(main())
