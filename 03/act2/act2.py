import simplehttp
import sys
import time

sys.setrecursionlimit(50000)

start = time.time()
simplehttp.crawl("http://www.rit.edu", "rit.edu", procs=40)
print(f"Total time: {time.time() - start}")

# r = simplehttp.SimpleHTTPRequest(
#     method="GET",
#     hostname="www.rit.edu",
#     https=True,
#     port=443,
#     resource="/"
# )

# r.request()
# print(r.respheaders)
