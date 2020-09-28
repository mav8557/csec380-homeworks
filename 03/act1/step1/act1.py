#!/usr/bin/env python3
from simplehttp import SimpleHTTPRequest
from pprint import pprint
import bs4
from unicodedata import normalize
import os


req = SimpleHTTPRequest(
    method="GET", 
    url="https://www.rit.edu/study/computing-security-bs", 
    # useragent="curl/7.68.0",
    resource="/study/computing-security-bs"
)

# make the request
req.request()

# soup time
souptime = bs4.BeautifulSoup(req.respbody, "lxml")

# get all courses and course titles
courses = souptime.find_all("tr", {"class": "hidden-row"})

coursetitles = {}
for c in courses:
    title = c.contents[1].contents[0]
    fulltitle = (c.contents[3].find_all("div", {"class":"course-name"})[0].contents[0])
    if title is not None:
        # apparently we get Nones here
        if "<em>" in str(title):
            continue
        #coursetitles.append(normalize("NFKD", str(title)).strip())
        title = title.replace("\xa0", "")
        fulltitle = fulltitle.replace("\xa0", "")
        if len(title) > 6:
            coursetitles[title.strip()] = fulltitle.strip()

if not os.path.exists("./ih8docker"):
    os.mkdir("./ih8docker")

with open("./ih8docker/courses.csv", "w") as fd:
    for key, value in coursetitles.items():
        fd.write(f"{key},{value}\n")

