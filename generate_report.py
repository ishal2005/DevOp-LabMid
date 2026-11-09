
import json
import os
from datetime import datetime, timezone
from pathlib import Path

source = Path("pytest-results.json")

if not source.exists():
    raise SystemExit("Pytest report missing")

data = json.loads(source.read_text(encoding="utf-8"))

tests = []

for test in data.get("tests", []):
    outcome = test.get("outcome", "unknown")
    failure = None

    for phase in ("setup", "call", "teardown"):
        details = test.get(phase, {})
        if details.get("outcome") == "failed":
            failure = details.get("longrepr", "Test failed")
            outcome = "failed"
            break

    tests.append({
        "name": test.get("nodeid"),
        "result": outcome,
        "failure_message": failure
    })

passed = sum(t["result"] == "passed" for t in tests)
failed = sum(t["result"] == "failed" for t in tests)
total = len(tests)

summary = data.get("summary", {})
overall_success = (
    failed == 0
    and total >= 3
    and summary.get("failed", 0) == 0
    and summary.get("errors", 0) == 0
    and summary.get("collected", 0) == total
    and all(t["result"] == "passed" for t in tests)
)

report = {
    "repository": os.getenv("GITHUB_REPOSITORY", "local"),
    "branch": os.getenv("GITHUB_REF_NAME", "local"),
    "commit_sha": os.getenv("GITHUB_SHA", "local"),
    "run_id": os.getenv("GITHUB_RUN_ID", "local"),
    "timestamp": datetime.now(timezone.utc).isoformat(),
    "tests": tests,
    "total": total,
    "passed": passed,
    "failed": failed,
    "status": "passed" if overall_success else "failed"
}

Path("ci-test-report.json").write_text(
    json.dumps(report, indent=4),
    encoding="utf-8"
)

print(json.dumps(report, indent=2))
