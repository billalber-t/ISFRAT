# import json
# import csv
# import requests
# from collections import defaultdict
# from urllib.parse import urljoin
# from pathlib import Path

# API_BASE_URL = "http://localhost:5000"  # adjust if needed
# OUTPUT_DIR = Path(__file__).resolve().parent.parent / "outputs"

# def load_test_cases(filepath=OUTPUT_DIR / "generated_test_cases.json"):
#     with open(filepath) as f:
#         return json.load(f)

# def execute_test_case(test_case):
#     method = test_case["method"]
#     endpoint = test_case["endpoint"]
#     payload = test_case["payload"]
#     url = urljoin(API_BASE_URL, endpoint)

#     try:
#         if method == "GET":
#             response = requests.get(url, params=payload)
#         elif method == "POST":
#             response = requests.post(url, json=payload)
#         elif method == "PUT":
#             response = requests.put(url, json=payload)
#         elif method == "DELETE":
#             response = requests.delete(url, json=payload)
#         else:
#             print(f"Unsupported method: {method}")
#             return None
#         return response
#     except Exception as e:
#         print(f"Request failed: {e}")
#         return None

# def compute_metrics(test_cases, results):
#     metrics = {}
#     endpoints = set()
#     param_coverage = defaultdict(set)
#     success_count = 0
#     failure_count = 0

#     endpoint_success = defaultdict(int)
#     endpoint_failure = defaultdict(int)

#     for tc, res in zip(test_cases, results):
#         endpoints.add(tc["endpoint"])
#         for param in tc["payload"]:
#             param_coverage[tc["endpoint"]].add(param)

#         if res["status_code"] and 200 <= res["status_code"] < 400:
#             success_count += 1
#             endpoint_success[tc["endpoint"]] += 1
#         else:
#             failure_count += 1
#             endpoint_failure[tc["endpoint"]] += 1

#     total_endpoints = len(endpoints)
#     total_test_cases = len(test_cases)

#     metrics["total_endpoints"] = total_endpoints
#     metrics["total_test_cases"] = total_test_cases
#     metrics["success_count"] = success_count
#     metrics["failure_count"] = failure_count
#     metrics["success_rate_percent"] = (success_count / total_test_cases) * 100
#     metrics["failure_rate_percent"] = (failure_count / total_test_cases) * 100
#     metrics["diversity_score"] = sum(len(params) for params in param_coverage.values())
#     metrics["endpoint_success"] = dict(endpoint_success)
#     metrics["endpoint_failure"] = dict(endpoint_failure)

#     return metrics

# def save_metrics(metrics):
#     with open(OUTPUT_DIR / "metrics_report.json", "w") as f:
#         json.dump(metrics, f, indent=2)

#     with open(OUTPUT_DIR / "metrics_report.csv", "w", newline="") as csvfile:
#         writer = csv.writer(csvfile)
#         writer.writerow(["Metric", "Value"])
#         for k, v in metrics.items():
#             if isinstance(v, dict):
#                 for subk, subv in v.items():
#                     writer.writerow([f"{k}.{subk}", subv])
#             else:
#                 writer.writerow([k, v])

# def main():
#     OUTPUT_DIR.mkdir(exist_ok=True)

#     test_cases = load_test_cases()
#     results = []

#     print(f"Running {len(test_cases)} test cases...\n")

#     for idx, tc in enumerate(test_cases, 1):
#         print(f"[{idx}] {tc['method']} {tc['endpoint']} ({tc['type']})")
#         response = execute_test_case(tc)
#         result = {
#             "test_case": tc,
#             "status_code": response.status_code if response else None,
#             "response_time_ms": response.elapsed.total_seconds() * 1000 if response else None,
#             "response_body": response.text if response else None,
#         }
#         results.append(result)

#     with open(OUTPUT_DIR / "test_results.json", "w") as f:
#         json.dump(results, f, indent=2)

#     print("\n✅ Test execution complete. Results saved to outputs/test_results.json")

#     metrics = compute_metrics(test_cases, results)
#     save_metrics(metrics)

#     print("\n📊 Metrics:")
#     print(f"- Total endpoints: {metrics['total_endpoints']}")
#     print(f"- Total test cases: {metrics['total_test_cases']}")
#     print(f"- Success rate: {metrics['success_rate_percent']:.2f}%")
#     print(f"- Failure rate: {metrics['failure_rate_percent']:.2f}%")
#     print(f"- Diversity (unique params): {metrics['diversity_score']}")
#     print("\n📁 Metrics report written to outputs/metrics_report.json and outputs/metrics_report.csv")

# if __name__ == "__main__":
#     main()


import json
import csv
import requests
from collections import defaultdict
from urllib.parse import urljoin
from pathlib import Path

OUTPUT_DIR = Path(__file__).resolve().parent.parent / "outputs"
TEST_CASES_FILE = OUTPUT_DIR / "generated_test_cases.json"

API_BASE_URL = "http://localhost:5000"  # adjust if needed

# 🪪 Configurable auth
config = {
    "auth_method": "none",  # options: none, api_key, bearer_token, basic
    "api_key": "your-api-key-here",
    "bearer_token": "your-jwt-or-oauth-token-here",
    "basic_username": "your-username",
    "basic_password": "your-password"
}


def get_auth_headers():
    """
    Return the appropriate auth headers based on config.
    """
    if config["auth_method"] == "none":
        return {}
    elif config["auth_method"] == "api_key":
        return {"Authorization": f"Api-Key {config['api_key']}"}
    elif config["auth_method"] == "bearer_token":
        return {"Authorization": f"Bearer {config['bearer_token']}"}
    elif config["auth_method"] == "basic":
        # Basic Auth is handled differently — see below
        return {}
    else:
        raise ValueError(f"Unsupported auth_method: {config['auth_method']}")


def load_test_cases(filepath=TEST_CASES_FILE):
    with open(filepath) as f:
        return json.load(f)


def execute_test_case(test_case):
    method = test_case["method"]
    endpoint = test_case["endpoint"]
    payload = test_case["payload"]
    url = urljoin(API_BASE_URL, endpoint)

    headers = get_auth_headers()
    auth = None

    if config["auth_method"] == "basic":
        auth = (config["basic_username"], config["basic_password"])

    try:
        if method == "GET":
            response = requests.get(url, params=payload, headers=headers, auth=auth)
        elif method == "POST":
            response = requests.post(url, json=payload, headers=headers, auth=auth)
        elif method == "PUT":
            response = requests.put(url, json=payload, headers=headers, auth=auth)
        elif method == "DELETE":
            response = requests.delete(url, json=payload, headers=headers, auth=auth)
        else:
            print(f"Unsupported method: {method}")
            return None
        return response
    except Exception as e:
        print(f"Request failed: {e}")
        return None


def compute_metrics(test_cases, results):
    metrics = {}
    endpoints = set()
    param_coverage = defaultdict(set)
    success_count = 0
    failure_count = 0

    endpoint_success = defaultdict(int)
    endpoint_failure = defaultdict(int)

    for tc, res in zip(test_cases, results):
        endpoints.add(tc["endpoint"])
        for param in tc["payload"]:
            param_coverage[tc["endpoint"]].add(param)

        if res["status_code"] and 200 <= res["status_code"] < 400:
            success_count += 1
            endpoint_success[tc["endpoint"]] += 1
        else:
            failure_count += 1
            endpoint_failure[tc["endpoint"]] += 1

    total_endpoints = len(endpoints)
    total_test_cases = len(test_cases)

    metrics["total_endpoints"] = total_endpoints
    metrics["total_test_cases"] = total_test_cases
    metrics["success_count"] = success_count
    metrics["failure_count"] = failure_count
    metrics["success_rate_percent"] = (success_count / total_test_cases) * 100
    metrics["failure_rate_percent"] = (failure_count / total_test_cases) * 100
    metrics["diversity_score"] = sum(len(params) for params in param_coverage.values())
    metrics["endpoint_success"] = dict(endpoint_success)
    metrics["endpoint_failure"] = dict(endpoint_failure)

    return metrics


def save_metrics(metrics):
    OUTPUT_DIR.mkdir(exist_ok=True)

    with open(OUTPUT_DIR / "metrics_report.json", "w") as f:
        json.dump(metrics, f, indent=2)

    with open(OUTPUT_DIR / "metrics_report.csv", "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Metric", "Value"])
        for k, v in metrics.items():
            if isinstance(v, dict):
                for subk, subv in v.items():
                    writer.writerow([f"{k}.{subk}", subv])
            else:
                writer.writerow([k, v])


def main():
    OUTPUT_DIR.mkdir(exist_ok=True)

    test_cases = load_test_cases()
    results = []

    print(f"Running {len(test_cases)} test cases...\n")

    for idx, tc in enumerate(test_cases, 1):
        print(f"[{idx}] {tc['method']} {tc['endpoint']} ({tc['type']})")
        response = execute_test_case(tc)
        result = {
            "test_case": tc,
            "status_code": response.status_code if response else None,
            "response_time_ms": response.elapsed.total_seconds() * 1000 if response else None,
            "response_body": response.text if response else None,
        }
        results.append(result)

    with open(OUTPUT_DIR / "test_results.json", "w") as f:
        json.dump(results, f, indent=2)

    print("\n✅ Test execution complete. Results saved to outputs/test_results.json")

    metrics = compute_metrics(test_cases, results)
    save_metrics(metrics)

    print("\n📊 Metrics:")
    print(f"- Total endpoints: {metrics['total_endpoints']}")
    print(f"- Total test cases: {metrics['total_test_cases']}")
    print(f"- Success rate: {metrics['success_rate_percent']:.2f}%")
    print(f"- Failure rate: {metrics['failure_rate_percent']:.2f}%")
    print(f"- Diversity (unique params): {metrics['diversity_score']}")
    print("\n📁 Metrics report written to outputs/metrics_report.json and outputs/metrics_report.csv")


if __name__ == "__main__":
    main()
