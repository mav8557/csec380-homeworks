import requests

# Activity 2
url = "http://csec380-core.csec.rit.edu:82/"

def getToken():
    token = requests.post(url + "getSecure").text.split(':')[1].strip()[:-1]
    return(token)

token = getToken()
print(f"[+] Connecting to getFlag2 with token: {token}")
flag2 = requests.post(url + "getFlag2", data= {
    'token': token
})

print(flag2.text)

# Activity 3
p3 = requests.post(url + "getFlag3Challenge", data={
    'token': token
})
print(p3.text)
captcha = p3.text.split(':')[1].strip()[:-1]
response = input(f"Safe to eval? {captcha} ")

# type fast here, eval over http is a struggle
if response == "Y":
    result = eval(captcha) # security 100
print(result)
solution = requests.post(url + "getFlag3Challenge", data={
    'token': token,
    'solution': result
})

print(solution.text)

# Activity 4
headers = {
#    'User-Agent': 'Windows NT 6.1 .NET'
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko'
    #"User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; AS; rv:11.0) like Gecko"
    #"User-Agent": "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; Media Center PC 6.0; InfoPath.3; MS-RTC LM 8; Zune 4.7)"
    #"User-Agent": "Mozilla/5.0 CK={} (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko",
}


data = {
    'username': 'mav8557',
    'token': token
}


p4 = requests.post(url + "/createAccount", data=data, headers=headers)
print(p4.headers, p4.text)
