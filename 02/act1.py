#!/usr/bin/env python3

from simplehttp import SimpleHTTPRequest
req = SimpleHTTPRequest(method="POST")
flag = req.request().split("\r\n")[-1].split("is ")[-1]
print(flag)
