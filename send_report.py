
import json
import os
from pathlib import Path
import requests

report = json.loads(
    Path("ci-test-report.json").read_text(encoding="utf-8")
)

token = os.environ["REPORT_TOKEN"]

response = requests.post(
    "http://127.0.0.1:5001/report",
    json=report,
    headers={"X-Report-Token": token},
    timeout=15
)

response.raise_for_status()
print("Report successfully delivered to localhost!")
