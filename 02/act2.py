#!/usr/bin/env python3

from simplehttp import SimpleHTTPRequest

req = SimpleHTTPRequest(method="POST", resource="/getSecure")

token = req.request().split("is: ")[-1][:-1]

req2 = SimpleHTTPRequest(method="POST", resource="/getFlag2", body=f"token={token}")

flag = req2.request().split("is ")[-1][:-1]

print(flag)