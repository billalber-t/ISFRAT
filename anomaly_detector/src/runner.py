import json
from pathlib import Path
from statistics import mean, stdev
from collections import defaultdict

# Paths
BASE_DIR = Path(__file__).resolve().parent.parent
TCG_OUTPUTS = BASE_DIR.parent / "test_case_generator" / "outputs"
AD_OUTPUTS = BASE_DIR / "outputs"

TEST_RESULTS_FILE = TCG_OUTPUTS / "test_results.json"
ANOMALIES_FILE = AD_OUTPUTS / "anomalies.json"

def load_test_results(filepath=TEST_RESULTS_FILE):
    if not filepath.exists():
        raise FileNotFoundError(f"Test results file not found: {filepath}")
    with open(filepath) as f:
        return json.load(f)

def detect_anomalies(results):
    anomalies = []
    endpoint_times = defaultdict(list)

    for res in results:
        tc = res["test_case"]
        endpoint = tc["endpoint"]
        rt = res["response_time_ms"]
        if rt is not None:
            endpoint_times[endpoint].append(rt)

    endpoint_stats = {}
    for ep, times in endpoint_times.items():
        if len(times) >= 2:
            endpoint_stats[ep] = {"mean": mean(times), "stddev": stdev(times)}
        else:
            endpoint_stats[ep] = {"mean": times[0], "stddev": 0}

    for res in results:
        tc = res["test_case"]
        endpoint = tc["endpoint"]
        status = res["status_code"]
        response_time = res["response_time_ms"]
        reason = None

        if status is not None and status >= 500:
            reason = f"Server error {status}"
        if status is not None and 400 <= status < 500 and tc["type"] == "valid":
            reason = f"Client error {status} on valid input"

        stats = endpoint_stats.get(endpoint, {"mean": 0, "stddev": 0})
        if response_time is not None and stats["stddev"] > 0:
            if response_time > stats["mean"] + 2 * stats["stddev"]:
                reason = f"High latency: {response_time:.2f}ms"

        if reason:
            anomalies.append({
                "test_case": tc,
                "status_code": status,
                "response_time_ms": response_time,
                "anomaly_reason": reason
            })

    return anomalies

def save_anomalies(anomalies):
    AD_OUTPUTS.mkdir(exist_ok=True)
    with open(ANOMALIES_FILE, "w") as f:
        json.dump(anomalies, f, indent=2)

def summarize(anomalies):
    print("\n📊 Anomaly Summary:")
    reasons = defaultdict(int)
    for anomaly in anomalies:
        reasons[anomaly["anomaly_reason"]] += 1
    for reason, count in reasons.items():
        print(f"- {reason}: {count} occurrences")

def main():
    print("🚀 Running Anomaly Detection Runner...")
    results = load_test_results()
    anomalies = detect_anomalies(results)
    save_anomalies(anomalies)

    print(f"✅ Anomaly detection complete. Found {len(anomalies)} anomalies.")
    print(f"📁 Results saved to: {ANOMALIES_FILE}")

    if anomalies:
        summarize(anomalies)
    else:
        print("🎉 No anomalies detected.")

if __name__ == "__main__":
    main()
