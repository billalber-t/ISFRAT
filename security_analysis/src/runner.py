import json
from pathlib import Path
import requests
from urllib.parse import urljoin

BASE_DIR = Path(__file__).resolve().parent.parent
OUTPUT_DIR = BASE_DIR / "outputs"
OUTPUT_DIR.mkdir(exist_ok=True)

TCG_OUTPUTS = BASE_DIR.parent / "test_case_generator" / "outputs"
SPEC_FILE = BASE_DIR.parent / "test_case_generator" / "specs" / "api_spec.yaml"

SECURITY_FINDINGS_FILE = OUTPUT_DIR / "security_findings.json"

API_BASE_URL = "http://localhost:5000"  # adjust as needed

MALICIOUS_PAYLOADS = [
    "' OR '1'='1",                         # SQLi
    "<script>alert(1)</script>",          # XSS
    "`rm -rf /`",                         # Command injection
    "../../../../etc/passwd",            # Path traversal
]

def load_test_cases(filepath=TCG_OUTPUTS / "generated_test_cases.json"):
    with open(filepath) as f:
        return json.load(f)

def test_for_security_issues(test_cases):
    findings = []
    for tc in test_cases:
        endpoint = tc["endpoint"]
        method = tc["method"]
        params = tc["payload"]

        for param in params:
            for payload in MALICIOUS_PAYLOADS:
                attack_payload = params.copy()
                attack_payload[param] = payload
                url = urljoin(API_BASE_URL, endpoint)

                try:
                    resp = None
                    if method == "GET":
                        resp = requests.get(url, params=attack_payload)
                    elif method == "POST":
                        resp = requests.post(url, json=attack_payload)
                    elif method == "PUT":
                        resp = requests.put(url, json=attack_payload)
                    elif method == "DELETE":
                        resp = requests.delete(url, json=attack_payload)

                    if resp is not None and resp.status_code < 400:
                        findings.append({
                            "endpoint": endpoint,
                            "method": method,
                            "parameter": param,
                            "malicious_payload": payload,
                            "response_status": resp.status_code,
                            "finding": "Potential vulnerability: malicious payload accepted"
                        })

                except Exception as e:
                    findings.append({
                        "endpoint": endpoint,
                        "method": method,
                        "parameter": param,
                        "malicious_payload": payload,
                        "error": str(e),
                        "finding": "Error during security test"
                    })

    return findings

def save_findings(findings):
    with open(SECURITY_FINDINGS_FILE, "w") as f:
        json.dump(findings, f, indent=2)

def main():
    print("🚀 Running Security Analysis Module...")
    test_cases = load_test_cases()
    findings = test_for_security_issues(test_cases)
    save_findings(findings)

    print(f"✅ Security analysis complete. Found {len(findings)} findings.")
    print(f"📁 Results saved to: {SECURITY_FINDINGS_FILE}")

if __name__ == "__main__":
    main()
