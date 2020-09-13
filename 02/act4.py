#!/usr/bin/env python3
from simplehttp import SimpleHTTPRequest

req = SimpleHTTPRequest(method="POST", resource="/getSecure")
token = req.request().split("is: ")[-1][:-1]

req2 = SimpleHTTPRequest(
    method="POST", 
    resource="/createAccount",
    body=f"token={token}&username=richardgill", 
    useragent="Mozilla/5.0 (compatible, MSIE 11, Windows NT 6.3; Trident/7.0; rv:11.0) like Gecko"
)

response = req2.request()
print(response)

password = response.split("is ")[-1]
password = password.translate(str.maketrans({'&': '%26', '=': '%3D'}))

req3 = SimpleHTTPRequest(
    method="POST", 
    resource="/login",
    body=f'username=richardgill&password={password}&token={token}', 
    useragent="Mozilla/5.0 (compatible, MSIE 11, Windows NT 6.3; Trident/7.0; rv:11.0) like Gecko"
)

flag = req3.request().split("is ")[-1][:-1]
print(flag)
