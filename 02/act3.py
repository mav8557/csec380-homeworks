#!/usr/bin/env python3
from simplehttp import SimpleHTTPRequest
from time import sleep

print("POST 1: GRABBING TOKEN!")
req = SimpleHTTPRequest(method="POST", resource="/getSecure")
token = req.request().split("is: ")[-1][:-1]

print("TOKEN:", token)
print("POST 2: RETRIEVING CAPTCHA!")
req2 = SimpleHTTPRequest(method="POST", resource="/getFlag3Challenge", body=f"token={token}")

response = req2.request()
print(response)
captcha = response.split("following: ")[-1][:-1]
print(f'[+] Solving CAPTCHA: {captcha}')
solution = eval(captcha)

print(f"[+] Computed Solution: {solution}")
print("POST 3: SENDING SOLUTION!")
req3 = SimpleHTTPRequest(method="POST", resource="/getFlag3Challenge", body=f"token={token}&solution={solution}")
flag = req3.request().split("is ")[-1][:-1]
print(flag)
