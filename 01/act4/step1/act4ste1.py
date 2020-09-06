"""
Step 1
Request csec.rit.edu using the requests library

course: CSEC-380 Principles of Web Application Security
author: Michael Vaughan
"""

import requests

req = requests.get("https://csec.rit.edu")

if req.status_code == 200:
    print(req.text)
