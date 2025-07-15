# from test_case_generator.src.utils import load_api_spec
# from test_case_generator.src.generator import build_test_case
# import json
# from pathlib import Path

# OUTPUT_DIR = Path(__file__).resolve().parent.parent / "outputs"
# SPEC_PATH = Path(__file__).resolve().parent.parent / "specs" / "api_spec.yaml"


# def main(test_run_id=None):
#     assert test_run_id is not None, "test_run_id is required to persist test cases."

#     OUTPUT_DIR.mkdir(exist_ok=True)

#     spec = load_api_spec(SPEC_PATH)

#     paths = spec['paths']
#     all_test_cases = []

#     db = SessionLocal()

#     for path, methods in paths.items():
#         for method, details in methods.items():
#             parameters = details.get('parameters', [])
#             print(f"Generating test cases for {method.upper()} {path}")

#             cases = build_test_case(path, method, parameters)
#             for c in cases:
#                 test_case = {
#                     "endpoint": path,
#                     "method": method.upper(),
#                     "type": c["type"],
#                     "payload": c["payload"]
#                 }
#                 all_test_cases.append(test_case)

#                 # Persist to DB with test_run_id
#                 db.add(TestCase(
#                     test_run_id=test_run_id,
#                     endpoint=path,
#                     method=method.upper(),
#                     type=c["type"],
#                     payload=json.dumps(c["payload"])
#                 ))

#     db.commit()
#     db.close()

#     output_file = OUTPUT_DIR / "generated_test_cases.json"
#     with open(output_file, "w") as f:
#         json.dump(all_test_cases, f, indent=2)

#     print(f"✅ Test cases generated, saved to {output_file} and linked to test_run_id={test_run_id}")



from pathlib import Path
from app.db.session import SessionLocal
from app.db.models import TestCase
from test_case_generator.src.utils import load_api_spec
from test_case_generator.src.generator import build_test_case
import json

# output and spec paths
OUTPUT_DIR = Path(__file__).resolve().parent.parent / "outputs"
SPEC_PATH = Path(__file__).resolve().parent.parent / "specs" / "api_spec.yaml"

def main(test_run_id=None):
    assert test_run_id is not None, "test_run_id is required to persist test cases."

    OUTPUT_DIR.mkdir(exist_ok=True)

    # load spec
    spec = load_api_spec(SPEC_PATH)

    paths = spec['paths']
    all_test_cases = []

    db = SessionLocal()

    try:
        for path, methods in paths.items():
            for method, details in methods.items():
                parameters = details.get('parameters', [])
                print(f"Generating test cases for {method.upper()} {path}")

                cases = build_test_case(path, method, parameters)
                for c in cases:
                    test_case = {
                        "endpoint": path,
                        "method": method.upper(),
                        "type": c["type"],
                        "payload": c["payload"]
                    }
                    all_test_cases.append(test_case)

                    # Persist to DB
                    db.add(TestCase(
                        test_run_id=test_run_id,
                        endpoint=path,
                        method=method.upper(),
                        type=c["type"],
                        payload=json.dumps(c["payload"])
                    ))

        db.commit()

        # save JSON file
        output_file = OUTPUT_DIR / f"generated_test_cases_{test_run_id}.json"
        with open(output_file, "w") as f:
            json.dump(all_test_cases, f, indent=2)

        print(f"✅ Test cases generated, saved to {output_file} and linked to test_run_id={test_run_id}")
        return f"Test cases generated and saved (run_id={test_run_id})"

    except Exception as e:
        db.rollback()
        raise e

    finally:
        db.close()

if __name__ == "__main__":
    # For direct run: provide a dummy test_run_id
    main(test_run_id=1)
