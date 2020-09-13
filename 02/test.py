import requests

url = "http://csec380-core.csec.rit.edu:82/"

token = requests.post(url + "getSecure").text.split("is: ")[-1][:-1]
print(token)

r = requests.request("POST", url + "getFlag3Challenge", data={
    'token': token
})

captcha = r.text.split("following: ")[-1][:-1]

solution = eval(captcha)

r = requests.request("POST", url + "getFlag3Challenge", data={
    'token': token,
    'solution': solution
})

print(r.text)
