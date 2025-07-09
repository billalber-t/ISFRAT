from utils import load_api_spec
from generator import build_test_case
import json

# Load API specification
spec = load_api_spec("specs/api_spec.yaml")

paths = spec['paths']
all_test_cases = []

for path, methods in paths.items():
    for method, details in methods.items():
        parameters = details.get('parameters', [])
        print(f"Generating test cases for {method.upper()} {path}")

        cases = build_test_case(path, method, parameters)
        all_test_cases.extend([
            {
                "endpoint": path,
                "method": method.upper(),
                "type": c["type"],
                "payload": c["payload"]
            }
            for c in cases
        ])

# Save test cases to JSON file
with open("generated_test_cases.json", "w") as f:
    json.dump(all_test_cases, f, indent=2)

print("✅ Test cases generated and saved to generated_test_cases.json")

