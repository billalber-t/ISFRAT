from test_case_generator.src.utils import load_api_spec
from test_case_generator.src.generator import build_test_case
import json
from pathlib import Path

OUTPUT_DIR = Path(__file__).resolve().parent.parent / "outputs"
SPEC_PATH = Path(__file__).resolve().parent.parent / "specs" / "api_spec.yaml"

def main():
    OUTPUT_DIR.mkdir(exist_ok=True)

    # Load API specification
    spec = load_api_spec(SPEC_PATH)

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
    output_file = OUTPUT_DIR / "generated_test_cases.json"
    with open(output_file, "w") as f:
        json.dump(all_test_cases, f, indent=2)

    print(f"✅ Test cases generated and saved to {output_file}")

if __name__ == "__main__":
    main()
