#!/usr/bin/env python3
"""Calculate owner-supplied burn thresholds or emit native counter-SLI rules.

Python 3.12+ standard library; reads one explicit JSON contract, writes no files
and never connects to services. JSON results/help on stdout, diagnostics on
stderr. Exits: 0 coherent inputs, 1 policy findings, 2 malformed input/usage.
--help exits 0 without reading a contract. --emit rules refuses policy findings.
"""

import argparse
from decimal import Decimal, DecimalException, InvalidOperation, localcontext
import json
from pathlib import Path
import re
import sys
from urllib.parse import urlsplit


class ContractError(ValueError):
    pass


def unique_pairs(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ContractError("remove duplicate JSON keys")
        result[key] = value
    return result


def invalid_constant(_):
    raise ContractError("replace nonfinite JSON numbers with finite values")


def number(value, field, *, integer=False):
    if isinstance(value, bool) or not isinstance(value, (str, int, Decimal)):
        raise ContractError(f"set {field} to a finite decimal number")
    try:
        result = Decimal(value)
    except InvalidOperation:
        raise ContractError(f"set {field} to a finite decimal number") from None
    if not result.is_finite() or (integer and result != result.to_integral_value()):
        raise ContractError(f"set {field} to a finite {'integer' if integer else 'number'}")
    return result


def identity(value, field, pattern):
    if not isinstance(value, str) or not re.fullmatch(pattern, value):
        raise ContractError(f"set {field} to the identifier form in the contract reference")
    return value


def decimal_text(value):
    return format(value.normalize(), "f") if value else "0"


def calculate(spec):
    if not isinstance(spec, dict) or spec.get("schema_version") != "1":
        raise ContractError('use a JSON object with schema_version "1"')
    target = number(spec.get("target"), "target")
    window = number(spec.get("objective_window_seconds"), "objective_window_seconds", integer=True)
    if not 0 < target < 1 or window <= 0:
        raise ContractError("use 0 < target < 1 and a positive objective window")
    policies = spec.get("policies")
    if not isinstance(policies, list) or not policies:
        raise ContractError("supply a nonempty policies array")
    result, findings, seen = [], [], set()
    for policy in policies:
        if not isinstance(policy, dict):
            raise ContractError("make every policy a JSON object")
        name = identity(policy.get("name"), "policy name", r"[a-z][a-z0-9_]*")
        if name in seen:
            raise ContractError("give policies distinct names")
        seen.add(name)
        long = number(policy.get("long_seconds"), "long_seconds", integer=True)
        short = number(policy.get("short_seconds"), "short_seconds", integer=True)
        fraction = number(policy.get("budget_fraction"), "budget_fraction")
        if not 0 < short < long <= window or not 0 < fraction <= 1:
            raise ContractError("use 0 < short < long <= objective window and 0 < budget_fraction <= 1")
        burn = fraction * window / long
        ratio = burn * (1 - target)
        if ratio >= 1:
            findings.append(f"{name}: lower the spend threshold or revise the window; a strict bad fraction > 1 or equal threshold cannot fire")
        floors = {}
        for part in ("long", "short"):
            count = number(policy.get(f"{part}_min_events"), f"{part}_min_events", integer=True)
            if count < 0:
                raise ContractError("use nonnegative minimum eligible event counts")
            single = None if count == 0 else 1 / count
            crosses = single is None or single > ratio
            if crosses:
                findings.append(f"{name}/{part}: choose an explicit sparse-traffic policy; one event can cross the threshold or the floor is empty")
            floors[part] = {"min_events": int(count), "single_bad_fraction": None if single is None else decimal_text(single), "single_event_can_cross": crosses}
        result.append({"name": name, "long_seconds": int(long), "short_seconds": int(short), "budget_fraction": decimal_text(fraction), "burn_threshold": decimal_text(burn), "bad_fraction_threshold": decimal_text(ratio), "traffic": floors})
    return {"target": decimal_text(target), "allowed_bad_fraction": decimal_text(1 - target), "objective_window_seconds": int(window), "policies": result, "findings": findings}


def generate_rules(spec, calculation):
    service = identity(spec.get("service"), "service", r"[a-zA-Z][a-zA-Z0-9_-]*")
    owner = identity(spec.get("owner"), "owner", r"[a-zA-Z][a-zA-Z0-9_-]*")
    sli = spec.get("sli")
    if not isinstance(sli, dict):
        raise ContractError("supply sli.eligible_counter and sli.bad_counter")
    metrics = [identity(sli.get(field), f"sli.{field}", r"[a-zA-Z_:][a-zA-Z0-9_:]*") for field in ("eligible_counter", "bad_counter")]
    if metrics[0] == metrics[1]:
        raise ContractError("use distinct eligible and subset bad counters")
    runbook = spec.get("runbook_url")
    if not isinstance(runbook, str):
        raise ContractError("supply an HTTP(S) runbook_url")
    parsed = urlsplit(runbook)
    if parsed.scheme not in ("https", "http") or not parsed.netloc or parsed.username or parsed.password:
        raise ContractError("supply an HTTP(S) runbook_url without credentials")
    eligible, bad = [metric + '{service=' + json.dumps(service) + '}' for metric in metrics]
    rules, recorded = [], set()
    for policy, computed in zip(spec["policies"], calculation["policies"], strict=True):
        if policy.get("severity") not in ("page", "ticket"):
            raise ContractError("set each policy severity to page or ticket")
        hold = number(policy.get("hold_seconds"), "hold_seconds", integer=True)
        if hold < 0:
            raise ContractError("use a nonnegative hold_seconds")
        terms = []
        for part in ("long", "short"):
            duration = f'{computed[part + "_seconds"]}s'
            record = f"slo:bad_ratio:{duration}"
            if record not in recorded:
                rules.append({"record": record, "expr": f"sum by (service) (rate({bad}[{duration}])) / sum by (service) (rate({eligible}[{duration}]))"})
                recorded.add(record)
            floor = computed["traffic"][part]["min_events"]
            terms.extend([f'({record} > {computed["bad_fraction_threshold"]})', f"(sum by (service) (increase({eligible}[{duration}])) >= {floor})"])
        rules.append({"alert": f'SloBurn_{computed["name"]}', "expr": " and on (service) ".join(terms), "for": f"{int(hold)}s", "labels": {"severity": policy["severity"], "owner": owner}, "annotations": {"runbook_url": runbook, "summary": f'{service} {computed["name"]} budget burn'}})
    return {"groups": [{"name": "slo_" + service, "rules": rules}]}


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("contract", type=Path, help="explicit local JSON contract; no ambient config is read")
    parser.add_argument("--emit", choices=("calculations", "rules"), default="calculations", help="JSON calculations (default) or native counter-SLI rules on stdout")
    args = parser.parse_args()
    try:
        with args.contract.open(encoding="utf-8") as stream:
            spec = json.load(stream, parse_float=Decimal, parse_constant=invalid_constant, object_pairs_hook=unique_pairs)
        with localcontext() as context:
            context.prec = 50
            calculation = calculate(spec)
            if args.emit == "rules" and calculation["findings"]:
                print("error: resolve calculator findings before generating rules; run without --emit rules for calculations", file=sys.stderr)
                return 1
            output = generate_rules(spec, calculation) if args.emit == "rules" else calculation
    except ContractError as error:
        print(f"error: {error}; see references/burn-math.md", file=sys.stderr)
        return 2
    except (OSError, UnicodeError, ValueError, DecimalException, OverflowError):
        print("error: use a readable JSON contract with finite, valid fields; see references/burn-math.md and the contract asset", file=sys.stderr)
        return 2
    print(json.dumps(output, indent=2, allow_nan=False))
    return 1 if calculation["findings"] else 0


if __name__ == "__main__":
    sys.exit(main())
