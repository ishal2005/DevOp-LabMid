
from flask import Flask, request, jsonify
from pathlib import Path
import json
import os

receiver = Flask(__name__)

REPORT_PATH = Path(__file__).resolve().parent / "test-report.json"


@receiver.route("/report", methods=["POST"])
def receive_report():
    expected_token = os.environ.get("REPORT_TOKEN")

    if not expected_token:
        return jsonify({"error": "Receiver token not configured"}), 503

    supplied_token = request.headers.get("X-Report-Token")

    if supplied_token != expected_token:
        return jsonify({"error": "Unauthorized"}), 401

    report = request.get_json(silent=True)

    if not isinstance(report, dict):
        return jsonify({"error": "Invalid JSON"}), 400

    required = [
        "repository", "branch", "commit_sha",
        "run_id", "timestamp", "tests",
        "total", "passed", "failed", "status"
    ]

    if not all(field in report for field in required):
        return jsonify({"error": "Missing report fields"}), 400

    temp_path = REPORT_PATH.with_suffix(".tmp")
    temp_path.write_text(
        json.dumps(report, indent=4),
        encoding="utf-8"
    )
    temp_path.replace(REPORT_PATH)

    print("Test report received and saved!")
    return jsonify({"message": "Report saved"}), 200


if __name__ == "__main__":
    receiver.run(host="127.0.0.1", port=5001)
