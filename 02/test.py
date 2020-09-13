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


def pretty_print_POST(req):
    """
    At this point it is completely built and ready
    to be fired; it is "prepared".

    However pay attention at the formatting used in 
    this function because it is programmed to be pretty 
    printed and may differ from the actual request.
    """
    print('{}\n{}\r\n{}\r\n\r\n{}'.format(
        '-----------START-----------',
        req.method + ' ' + req.url,
        '\r\n'.join('{}: {}'.format(k, v) for k, v in req.headers.items()),
        req.body,
    ))

pretty_print_POST(r.request)

print(r.text)