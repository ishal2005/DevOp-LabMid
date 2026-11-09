# Introduces the defect for the failing demo: registration number no longer required.
(Get-Content app.py) -replace 'all\(\[name, reg_no, title, url\]\)', 'all([name, title, url])' | Set-Content app.py
git add app.py; git commit -m "Introduce defect: skip reg_no validation"; git push
