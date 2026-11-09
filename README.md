
# DevOps Lab Mid - Assignment Submission Portal

## Technologies
- Python
- Flask
- SQLite
- Pytest
- GitHub Actions

## Install dependencies
pip install -r requirements.txt

## Run the application
python app.py

Open http://127.0.0.1:5000

## Run tests
python -m pytest tests/ -v

## Start local report receiver
Set the REPORT_TOKEN environment variable.

Windows PowerShell:
$env:REPORT_TOKEN = "your-secret"
python receiver.py

Receiver address:
http://127.0.0.1:5001/report

## CI/CD
GitHub Actions runs automated tests on each push.

A self-hosted Windows runner sends the report
to the local receiver after passing and failing tests.

## Test cases
1. Valid submission
2. Missing registration number
3. Invalid submission URL

## Bonus: GitHub Pages deployment
The `deploy` job publishes `site/` (static demo) to GitHub Pages only when the `test` job passes, on `main`.
Enable once: Repo -> Settings -> Pages -> Source: **GitHub Actions**.
Deployed URL: `https://<your-username>.github.io/<repo-name>/`

## Bonus: Email report
`send_email.py` emails the report after every run (pass or fail). Add these repository secrets:
`SMTP_HOST` (e.g. smtp.gmail.com), `SMTP_PORT` (587), `SMTP_USER`, `SMTP_PASSWORD` (Gmail app password), `REPORT_EMAIL_TO`.

## Demo
1. Push a passing commit, screenshot the green run and `test-report.json`.
2. `powershell demo/break.ps1` -> red run, report shows `failed`.
3. `powershell demo/fix.ps1` -> green run again.
