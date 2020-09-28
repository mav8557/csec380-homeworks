import simplehttp
import sys
import time
import threading
from multiprocessing import Manager
from urllib.parse import urlparse as up
import queue

try:
    open("something.txt")
except FileNotFoundError:
    links = [x.split(",")[1].strip() for x in open("companies.csv").readlines()][:25]

    man = Manager()

    visited_links = man.dict()
    tovisit = queue.Queue()

    threads = [None] * 60 # number of threads

    # populate tovisit queue with starting links
    for link in links:
        # depth of 0
        tovisit.put((link, 0))

    for i in range(len(threads)):
        threads[i] = threading.Thread(
            target=simplehttp.worker_entrypoint, args=({}, visited_links, tovisit, "ignoreddomain", i)
        )
        threads[i].start()


    for thread in threads:
        thread.join()


    # dump populated visited_links to disk

    with open("something.txt", "w") as f:
        for key, value in visited_links.items():
            f.write(f"{key},{value}\n")



paths = set()
with open("something.txt", "r") as f:
    for line in f:
        s = line.split(",")
        if len(s) != 2:
            continue
        path = up(s[0]).path
        if len(path) > 1:
            p = path.split("/")
            for part in p[:-1]:
                paths.add(part + "/")
            paths.add(p[-1])

with open("paths.list", "w") as f:
    for path in paths:
        f.write(path + "\n")



print("Done!")