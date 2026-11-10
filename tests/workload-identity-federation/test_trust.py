"""Inert exported policy fixtures; no credentials or cloud endpoints."""
from copy import deepcopy
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from urllib.parse import quote

ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "skills/workload-identity-federation/scripts/check-oidc-trust.py"
MARKER = "SYNTHETIC_CLAIM_WITHHELD"
EXPECTED = {"issuer": "https://issuer.example.invalid", "audience": "test-audience",
            "subject": "repo:example/service:ref:refs/heads/main",
            "principal": "arn:aws:iam::000000000000:oidc-provider/issuer.example.invalid"}
AWS = {"Statement": [{"Effect": "Allow", "Action": "sts:AssumeRoleWithWebIdentity",
                     "Principal": {"Federated": EXPECTED["principal"]}, "Condition": {"StringEquals": {
                         "issuer.example.invalid:aud": EXPECTED["audience"], "issuer.example.invalid:sub": EXPECTED["subject"]}}}]}
AZURE = {"issuer": EXPECTED["issuer"], "audiences": [EXPECTED["audience"]], "subject": EXPECTED["subject"]}
GCP = {"oidc": {"issuerUri": EXPECTED["issuer"], "allowedAudiences": [EXPECTED["audience"]]},
       "attributeMapping": {"google.subject": "assertion.sub"},
       "attributeCondition": "assertion.sub == '" + EXPECTED["subject"] + "'"}


class TrustTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix="trust-test-")
        self.root = Path(self.tmp.name)
        self.policy, self.expected = self.root / "policy.json", self.root / "expected.json"

    def tearDown(self):
        self.tmp.cleanup()

    def check(self, provider, policy, expected=None):
        self.policy.write_text(json.dumps(policy))
        self.expected.write_text(json.dumps(expected or EXPECTED))
        before = (self.policy.read_bytes(), self.expected.read_bytes())
        result = subprocess.run([sys.executable, str(SCRIPT), str(self.policy), "--provider", provider, "--expected", str(self.expected)], text=True, capture_output=True)
        self.assertEqual(before, (self.policy.read_bytes(), self.expected.read_bytes()))
        self.assertNotIn(MARKER, result.stdout + result.stderr)
        return result

    def test_accept_all_providers_and_repeat(self):
        for provider, policy in (("aws", AWS), ("azure", AZURE), ("gcp", GCP)):
            results = [self.check(provider, policy) for _ in range(2)]
            self.assertEqual(results[0].returncode, 0, results[0].stderr)
            self.assertEqual(results[0].stdout, results[1].stdout)
        self.assertEqual(self.check("azure", {"value": [AZURE]}).returncode, 0)

    def test_aws_deny_wrong_branch_audience_and_extra_allow(self):
        for key in ("sub", "aud"):
            policy = deepcopy(AWS)
            policy["Statement"][0]["Condition"]["StringEquals"]["issuer.example.invalid:" + key] = MARKER
            self.assertEqual(self.check("aws", policy).returncode, 1)
        policy = deepcopy(AWS)
        policy["Statement"].append({"Effect": "Allow", "Principal": "*", "Action": "sts:AssumeRoleWithWebIdentity"})
        self.assertEqual(self.check("aws", policy).returncode, 1)
        policy = deepcopy(AWS)
        policy["Statement"][0]["Condition"] = {"StringLike": {"issuer.example.invalid:aud": "test-audience", "issuer.example.invalid:sub": "repo:example/*"}}
        self.assertEqual(self.check("aws", policy).returncode, 1)
        policy = deepcopy(AWS)
        policy["Statement"][0]["Condition"]["StringEqualsIfExists"] = {"issuer.example.invalid:sub": EXPECTED["subject"]}
        self.assertEqual(self.check("aws", policy).returncode, 1)

    def test_native_aws_get_role_exports_and_encoded_policy(self):
        for document in (AWS, json.dumps(AWS), quote(json.dumps(AWS), safe="")):
            wrapped = {"Role": {"AssumeRolePolicyDocument": document}}
            self.assertEqual(self.check("aws", wrapped).returncode, 0)
        expected = dict(EXPECTED, subject=EXPECTED["subject"] + "%3Aliteral")
        policy = deepcopy(AWS)
        policy["Statement"][0]["Condition"]["StringEquals"]["issuer.example.invalid:sub"] = expected["subject"]
        self.assertEqual(self.check("aws", {"Role": {"AssumeRolePolicyDocument": json.dumps(policy)}}, expected).returncode, 0)
        self.assertEqual(self.check("aws", {"Role": MARKER}).returncode, 2)
        self.assertEqual(self.check("aws", {"Role": {"AssumeRolePolicyDocument": "%7Bbroken"}}).returncode, 2)

    def test_azure_alternatives_flexible_subject_and_pagination(self):
        changed = dict(AZURE, subject=MARKER)
        self.assertEqual(self.check("azure", [AZURE, changed]).returncode, 1)
        self.assertEqual(self.check("azure", dict(AZURE, audiences=[EXPECTED["audience"], MARKER])).returncode, 1)
        self.assertEqual(self.check("azure", dict(AZURE, claimsMatchingExpression={})).returncode, 1)
        self.assertEqual(self.check("azure", {"value": [AZURE], "@odata.nextLink": MARKER}).returncode, 2)
        expected = dict(EXPECTED, claims={"ref": "refs/heads/main"})
        self.assertEqual(self.check("azure", AZURE, expected).returncode, 1)

    def test_gcp_or_mapping_wildcard_and_extra_claim(self):
        for expression in (GCP["attributeCondition"] + " || true", "assertion.sub.startsWith('repo:example/')", "assertion.sub == 'repo:example/*'", "assertion.repository == 'example/service'"):
            self.assertEqual(self.check("gcp", dict(GCP, attributeCondition=expression)).returncode, 1)
        expected = dict(EXPECTED, claims={"ref": "refs/heads/main"})
        self.assertEqual(self.check("gcp", GCP, expected).returncode, 1)
        policy = dict(GCP, attributeCondition=GCP["attributeCondition"] + " && assertion.ref == 'refs/heads/main'")
        self.assertEqual(self.check("gcp", policy, expected).returncode, 0)
        policy = dict(GCP, attributeMapping={"google.subject": "assertion.repository"})
        self.assertEqual(self.check("gcp", policy).returncode, 1)

    def test_malformed_expectation_and_help(self):
        self.assertEqual(self.check("aws", [], EXPECTED).returncode, 2)
        self.assertEqual(self.check("aws", AWS, dict(EXPECTED, subject="repo:example/*")).returncode, 2)
        self.policy.write_text('{"bad": "' + MARKER)
        self.expected.write_text(json.dumps(EXPECTED))
        result = subprocess.run([sys.executable, str(SCRIPT), str(self.policy), "--provider", "aws", "--expected", str(self.expected)], text=True, capture_output=True)
        self.assertEqual(result.returncode, 2)
        self.assertNotIn(MARKER, result.stderr)
        result = subprocess.run([sys.executable, str(SCRIPT), "--help"], cwd=self.root, text=True, capture_output=True)
        self.assertEqual(result.returncode, 0)
        self.assertEqual(set(p.name for p in self.root.iterdir()), {"policy.json", "expected.json"})


if __name__ == "__main__":
    unittest.main(verbosity=2)
