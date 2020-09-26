#!/usr/bin/env python3
from simplehttp import SimpleHTTPRequest
from pprint import pprint
import bs4, os
from unicodedata import normalize
import urllib.parse


req = SimpleHTTPRequest(
    method="GET", 
    # useragent="curl/7.68.0",
    resource="/computing/directory?term_node_tid_depth=4919"
)

# make the request
req.request()

# soup time
souptime = bs4.BeautifulSoup(req.respbody, "lxml")

img = souptime.find_all("img", {"class":"card-img-top"})

imglinks = set()

for tag in img:
    imglinks.add(tag["data-src"].strip())

#pprint(imglinks)


# url = imglinks.pop()
# print()
# print(url)

os.mkdir("./staff")
i = 0
for url in imglinks:
    parsed = SimpleHTTPRequest.urlparser(url)

    print(parsed)
    newresource = "/" + "/".join(parsed["resource"])
    #newresource = SimpleHTTPRequest.encodeurl("/" + "/".join(parsed["resource"]))
    print(newresource)

    print(parsed["hostname"], newresource)

    req2 = SimpleHTTPRequest(
        method="GET",
        hostname=parsed["hostname"],
        resource=newresource
    )

    req2.request(filename=f"./staff/{i}.png", mode="wb")
    i+=1

#print(len(req2.resp))
#print(req2.resp)