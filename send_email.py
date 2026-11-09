"""Email the CI test report (bonus). Credentials come from environment variables / CI secrets."""
import json
import os
import smtplib
import sys
from email.message import EmailMessage
from pathlib import Path

report_path = Path("ci-test-report.json")
if not report_path.exists():
    sys.exit("ci-test-report.json missing - nothing to email")

report = json.loads(report_path.read_text(encoding="utf-8"))

host = os.environ["SMTP_HOST"]
port = int(os.environ.get("SMTP_PORT", "587"))
user = os.environ.get("SMTP_USER", "")
password = os.environ.get("SMTP_PASSWORD", "")
to_addr = os.environ["REPORT_EMAIL_TO"]
from_addr = os.environ.get("REPORT_EMAIL_FROM", user or "ci@localhost")

status = report["status"].upper()
sha = report["commit_sha"]

lines = [
    f"Overall result: {status}",
    f"Repository: {report['repository']}  Branch: {report['branch']}",
    f"Commit: {sha}",
    f"Run ID: {report['run_id']}  Time: {report['timestamp']}",
    f"Total: {report['total']}  Passed: {report['passed']}  Failed: {report['failed']}",
    "",
    "Individual results:",
]
for t in report["tests"]:
    lines.append(f"  [{t['result'].upper()}] {t['name']}")
    if t.get("failure_message"):
        lines.append("      " + str(t["failure_message"]).strip().replace("\n", "\n      "))

msg = EmailMessage()
msg["Subject"] = f"[CI {status}] {report['repository']} @ {sha[:7]}"
msg["From"] = from_addr
msg["To"] = to_addr
msg.set_content("\n".join(lines))
msg.add_attachment(
    report_path.read_bytes(), maintype="application", subtype="json",
    filename="test-report.json",
)

with smtplib.SMTP(host, port, timeout=30) as smtp:
    if os.environ.get("SMTP_STARTTLS", "1") == "1":
        smtp.starttls()
    if user:
        smtp.login(user, password)
    smtp.send_message(msg)

print(f"Report emailed to {to_addr}")
