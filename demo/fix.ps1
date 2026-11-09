# Reverts the defect for the corrected demo.
(Get-Content app.py) -replace 'all\(\[name, title, url\]\)', 'all([name, reg_no, title, url])' | Set-Content app.py
git add app.py; git commit -m "Fix: require reg_no again"; git push
