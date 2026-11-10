#!/usr/bin/env python3
"""Compare exported trust with an explicit contract; never request a token."""
import argparse
import json
from pathlib import Path
import re
import sys
from urllib.parse import unquote, urlsplit


def one(value, expected):
    return value == expected or value == [expected]


def exact(value):
    return isinstance(value, str) and bool(value) and not any(c in value for c in "*?\r\n")


def aws(policy, expected):
    if not isinstance(policy, dict):
        raise ValueError("invalid AWS document")
    if "Role" in policy:
        policy = policy["Role"]
        if not isinstance(policy, dict):
            raise ValueError("invalid AWS role export")
    policy = policy.get("AssumeRolePolicyDocument", policy)
    if isinstance(policy, str):
        policy = json.loads(unquote(policy) if policy.lstrip().startswith("%") else policy)
    if not isinstance(policy, dict):
        raise ValueError("invalid AWS document")
    statements = policy.get("Statement")
    if isinstance(statements, dict):
        statements = [statements]
    if not isinstance(statements, list) or not statements:
        raise ValueError("missing AWS statements")
    findings, allowed = [], 0
    prefix = expected["issuer"].removeprefix("https://").rstrip("/")
    for index, statement in enumerate(statements, 1):
        if not isinstance(statement, dict):
            raise ValueError("invalid AWS statement")
        if statement.get("Effect") == "Deny":
            continue
        allowed += 1
        codes = []
        if statement.get("Effect") != "Allow" or not one(statement.get("Action"), "sts:AssumeRoleWithWebIdentity") or "NotAction" in statement:
            codes.append("unexpected-allow-action")
        principal = statement.get("Principal", {})
        if not isinstance(principal, dict) or set(principal) != {"Federated"} or not one(principal.get("Federated"), expected["principal"]):
            codes.append("issuer-principal-mismatch")
        if "NotPrincipal" in statement:
            codes.append("unsupported-negative-principal")
        condition = statement.get("Condition", {})
        claims = {}
        if not isinstance(condition, dict):
            raise ValueError("invalid AWS condition")
        for operator, values in condition.items():
            if operator not in ("StringEquals", "StringLike") or not isinstance(values, dict):
                codes.append("unsupported-condition")
                continue
            for key, value in values.items():
                if key in claims:
                    codes.append("duplicate-condition-key")
                claims[key] = value
                if not (exact(value) or isinstance(value, list) and len(value) == 1 and exact(value[0])):
                    codes.append("wildcard-or-alternative-condition")
        for claim, value in {"aud": expected["audience"], "sub": expected["subject"], **expected.get("claims", {})}.items():
            if not one(claims.get(prefix + ":" + claim), value):
                codes.append("required-claim-missing-or-mismatched")
        findings.extend({"entry": index, "code": code} for code in sorted(set(codes)))
    if not allowed:
        findings.append({"code": "no-allow-statement"})
    return findings


def azure(policy, expected):
    if isinstance(policy, dict) and "value" in policy:
        if policy.get("@odata.nextLink"):
            raise ValueError("incomplete Azure export; collect all pages")
        policy = policy["value"]
    entries = policy if isinstance(policy, list) else [policy]
    if not entries or not all(isinstance(e, dict) for e in entries):
        raise ValueError("invalid Azure credentials export")
    findings = [{"code": "extra-claims-unsupported-for-azure"}] if expected.get("claims") else []
    for index, entry in enumerate(entries, 1):
        checks = {"issuer-mismatch": entry.get("issuer") == expected["issuer"],
                  "subject-mismatch": entry.get("subject") == expected["subject"],
                  "audience-mismatch": entry.get("audiences") == [expected["audience"]],
                  "flexible-subject-unsupported": "claimsMatchingExpression" not in entry}
        findings.extend({"entry": index, "code": code} for code, passed in checks.items() if not passed)
    return findings


def gcp(policy, expected):
    if not isinstance(policy, dict) or not isinstance(policy.get("oidc"), dict):
        raise ValueError("invalid GCP provider export")
    findings = []
    checks = {"issuer-mismatch": policy["oidc"].get("issuerUri") == expected["issuer"],
              "audience-mismatch-or-implicit-default": policy["oidc"].get("allowedAudiences") == [expected["audience"]],
              "subject-mapping-unsupported": isinstance(policy.get("attributeMapping"), dict) and policy["attributeMapping"].get("google.subject") == "assertion.sub",
              "provider-disabled": policy.get("disabled") is not True}
    findings.extend({"code": code} for code, passed in checks.items() if not passed)
    condition = policy.get("attributeCondition", "")
    if not isinstance(condition, str):
        raise ValueError("invalid GCP condition")
    claims = {}
    # Deliberately not a CEL evaluator: accept only exact string equalities joined by &&.
    # Reject quotes, escapes and operators inside literals rather than approximating CEL.
    term = re.compile(r"\s*assertion\.([a-zA-Z_][a-zA-Z_0-9]*)\s*==\s*(?:'([^'\\\r\n]*)'|\"([^\"\\\r\n]*)\")\s*\Z")
    for part in condition.split("&&"):
        match = term.fullmatch(part)
        if not match:
            findings.append({"code": "unsupported-cel-review-natively"})
            continue
        key, single, double = match.groups()
        value = single if single is not None else double
        if key in claims or not exact(value):
            findings.append({"code": "duplicate-or-wildcard-cel-claim"})
        claims[key] = value
    required = {"sub": expected["subject"], **expected.get("claims", {})}
    if any(claims.get(key) != value for key, value in required.items()):
        findings.append({"code": "required-claim-missing-or-mismatched"})
    return findings


def main():
    parser = argparse.ArgumentParser(description=(
        "Read local native AWS/Azure/GCP trust JSON and an exact expected contract. "
        "No cloud calls, token requests or writes. JSON codes/positions on stdout; "
        "diagnostics on stderr. Exits: 0 supported static form matches, 1 findings "
        "or unsupported form, 2 invalid input. Live allow/deny tests remain required."))
    parser.add_argument("policy", type=Path)
    parser.add_argument("--provider", required=True, choices=("aws", "azure", "gcp"))
    parser.add_argument("--expected", required=True, type=Path)
    args = parser.parse_args()
    try:
        expected = json.loads(args.expected.read_bytes())
        if not isinstance(expected, dict) or not all(exact(expected.get(key)) for key in ("issuer", "audience", "subject")):
            raise ValueError("expected contract needs exact issuer/audience/subject")
        parsed = urlsplit(expected["issuer"])
        if parsed.scheme != "https" or not parsed.hostname or parsed.query or parsed.fragment or parsed.username:
            raise ValueError("expected issuer must be an HTTPS issuer URL")
        claims = expected.get("claims", {})
        if not isinstance(claims, dict) or any(not isinstance(k, str) or not re.fullmatch(r"[A-Za-z_][A-Za-z_0-9]*", k) or not exact(v) or k in ("sub", "aud") for k, v in claims.items()):
            raise ValueError("invalid exact additional claims")
        if args.provider == "aws" and not exact(expected.get("principal")):
            raise ValueError("AWS requires an exact federated principal ARN")
        policy = json.loads(args.policy.read_bytes())
        findings = {"aws": aws, "azure": azure, "gcp": gcp}[args.provider](policy, expected)
    except (OSError, ValueError, TypeError, RecursionError):
        print("error: cannot check trust; supply complete native JSON and exact issuer/audience/subject expectations (payload withheld)", file=sys.stderr)
        return 2
    print(json.dumps({"provider": args.provider, "scope": "static export only; effective IAM and exchange unverified", "findings": findings}, sort_keys=True))
    return int(bool(findings))


if __name__ == "__main__":
    sys.exit(main())
