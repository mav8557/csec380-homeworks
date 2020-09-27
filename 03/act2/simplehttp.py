import socket
import ssl
import urllib.parse
from pprint import pprint
from typing import List
import threading
import time
from multiprocessing import Process, Manager
import sys 
from urllib.parse import urlparse as up
from bs4 import BeautifulSoup
import re # not using bs4 for emails, nope
import queue
from io import StringIO

"""
Notes:

HOPEFULLY DONE: Need to support relative links (/somethingelse, etc) 
"""
class SimpleHTTPRequest:
      def __init__(
                  self,
                  *args,
                  method="GET",
                  port=443,
                  resource = "/",
                  useragent = "richardgill",
                  content_type="application/x-www-form-urlencoded",
                  hostname="www.rit.edu",
                  https=True,
                  url="",
                  body='',
                  filename=None,
                  mode=None
      ):
            self.method = method
            #self.hostname = url.split("/")[2]
            self.hostname = hostname
            self.port = port
            self.resource = resource
            self.useragent = useragent
            self.content_type = content_type
            self.url = url
            self.headers = {}
            self.https = https
            self.filename = filename # optional filename to save to
            self.mode = mode         # mode to write file in
            self.body = body # tokens, stuff like that
            self.fullreq = "" # the full request to be sent
            self.resp = None # respose is None until we recv from the server
            self.recursion_count = 0 # how many times we have redirected
            #print(self.hostname, self.port, self.https, self.resource)

      @staticmethod
      def encodeurl(url: str) -> str:
            """
            Encode a URL's parameters correctly
            """
            return url.replace("&", "%26").replace("=", "%3D")

      @staticmethod
      def urlparser(url: str) -> dict:
            """
            Given a URL, split it into a hostname, port, etc to be
            converted into a request later 

            keys -> values:

            hostname is the hostname
            port is the port of the server
            https is boolean True if https
            resource is a list of every part of the route to the resource
            """
            parsed = {}
            if url.startswith("https://"):
                  parsed["https"] = True
                  url = url.lstrip("https://")
            elif url.startswith("http://"):
                  parsed["https"] = False
                  url = url.lstrip("http://")
            
            parsed["hostname"] = url.split('/')[0]
            hostandport = parsed["hostname"].split(":") # hostname and port
            if len(hostandport) == 2:
                  parsed["hostname"], parsed["port"] = hostandport
            
            # "/" + "/".join(resource) to get string form
            parsed["resource"] = url.split('/')[1:] 
            return parsed

      
      def add_header(self, header: str, value: str):
            """
            Add a custom header and value to the request
            """
            self.headers[header] = value

      def add_param(self, param: str, value: str):
            """
            Add a parameter to the request body

            ex: token=<token>
            """
            self.body[param] = value

      def request(self):
            """
            Send our request to the server, and return the full response
            """
            self.render()
            
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

            # self.sock.settimeout(10)

            if self.https:
                  # wrap encryption around socket if using https
                  self.sock = ssl.wrap_socket(self.sock, ssl_version=ssl.PROTOCOL_TLS)
            
            self.sock.settimeout(5)

            try:
                  self.sock.connect((self.hostname, self.port))
            except:
                  print(f"[-] Error connecting to {self.hostname}:{self.port}")
            

            # print("Connected to:", self.hostname, self.port)

            try:
                  self.sock.sendall(self.fullreq.encode())
            except:
                  print(f"[-] Machine Broke on {self.hostname}:{self.port}{self.resource}")
                  self.respbody = ""
                  self.respheaders = None
                  self.respheadersdict = None
                  return # we're done here
            

            resp = b""
            try:
                  while chunk := self.sock.recv(4096):
                        resp += chunk #.decode("utf-8")
            except socket.timeout:
                  print(f"[-] Timed out on {self.hostname}:{self.port}{self.resource}")
                  self.respbody = ""
                  self.respheaders = None
                  self.respheadersdict = None
                  return # we're done here
            except:
                  print("[-] Error reading from site:", self.hostname)
                  self.respbody = ""
                  self.respheaders = None
                  self.respheadersdict = None
                  return # we're done here

            self.sock.close()

            self.resp = resp # full response
            #print(f"[-] Pulled {self.hostname}:{self.port}{self.resource}")
            # headers
            thing = resp.split(b"\r\n\r\n", maxsplit=1)
            if len(thing) < 2:
                  print("[-] Broken response.", thing)
                  self.respbody = ""
                  self.respheaders = None
                  self.respheadersdict = None
                  return
            self.respheaders, self.respbody = resp.split(b"\r\n\r\n", maxsplit=1)

            #print(type(self.respheaders), self.respheaders)
            self.respheaders = self.respheaders.split(b"\r\n")

            #print(self.respheaders)

            # create response headers dictionary
            self.respheadersdict = {}
            self.respheadersdict["status_code"] = int(self.respheaders[0].split(b" ")[1])
            for header in self.respheaders[1:]:
                  s = header.split(b":", maxsplit=1)
                  if len(s) != 2:
                        print("sus header:", s)
                        continue
                  s[0], s[1] = s[0].decode(), s[1].decode()
                  self.respheadersdict[s[0].strip()] = s[1].strip()
                  # if self.respheadersdict.get("Content-Length", None) is not None:
                  #       self.respheadersdict["Content-Length"] = int(self.respheadersdict["Content-Length"].decode().strip())
            #pprint(self.respheadersdict)

            if self.respheadersdict["status_code"] in {301, 302}:
                  # follow redirect
                  #print("REDIRECTED!")
                  #newpath = self.resource.split("/")
                  #print(newpath[1:len(newpath)-1])
                  #finalpath = "/" + "/".join(newpath[1:len(newpath)-1]) + "/" + self.respheadersdict["Location"]
                  #print("NEW RESOURCE:", finalpath)

                  loc = self.respheadersdict["Location"]
                  results = up(loc)
                  #print(loc, results, self.resource)

                  if results.path == self.resource:
                        # don't redirect to ourselves
                        # this should be fixed because sometimes a parameter that would get cut off by up()
                        # could cause the server to redirect us somewhere else. 
                        pass

                  if results.scheme == "":
                        # relative path. create new path

                        oldpath = self.resource.split("/")
                        old = "/" + "/".join(oldpath[1:-1])
                        newpath = old + results.path
                        self.resource = newpath
                  else:
                        # grab port if present
                        s = results.netloc.split(":")
                        if len(s) == 1:
                              self.hostname = results.netloc
                        else:
                              self.hostname = results.netloc
                              self.port = s[1]
                        self.https = (results.scheme == "https")
                        if self.https and self.port == 80:
                              #print("tripping")
                              self.port = 443
                              #print(self.port)
                        self.resource = results.path

                  if results.query != "":
                        self.resource += "?" + results.query
                        #print("[+] ADDED Queries!", self.resource)
                  
                  if self.recursion_count < 25:
                        self.recursion_count += 1
                        self.request()
            
                  # print(results)
                  #self.resource = finalpath
                  #self.request()
                  
            
            # print(len(self.respbody))
            # print("ATTEMPTING TO DOWNLOAD:", self.filename, self.mode)
            # print("ATTEMPTING TO DOWNLOAD:", self.filename, self.mode)
            if self.filename is not None and self.mode is not None and len(self.respbody) > 0:
                  with open(self.filename, self.mode) as f:
                        f.write(self.respbody)
                  #print(self.filename, "saved!")

            return resp

      def render(self):
            """
            Render the entire response, called just before sending it.
            """
            if len(self.fullreq) > 0:
                  # if rendered already, start from scratch
                  self.fullreq = ""
            self.fullreq += f"{self.method} {self.resource} HTTP/1.1\r\n"
            # add Host header
            if self.port not in {80, 443}:
                  self.fullreq += f"Host: {self.hostname}:{self.port}\r\n"
            else:
                  self.fullreq += f"Host: {self.hostname}\r\n"
            # add user agent
            self.fullreq += f"User-Agent: {self.useragent}\r\n"
            # accept header
            self.fullreq += f"Accept: */*\r\n"
            #self.fullreq += f"Vary: Accept-Encoding\r\n"
            #self.fullreq += f"Accept-Encoding: gzip, deflate\r\n"

            # language
            #self.fullreq += f"Accept-Language: en-us\r\n"

            # encoding
            #self.fullreq += f"Accept-Encoding: text/html\r\n"

            # content-type
            if self.method == "POST":
                  self.fullreq += f"Content-Type: {self.content_type}\r\n"
            # content-length
            if len(self.body) > 0:
                  # if self.body.count('&') > 1:
                  #       self.fullreq += f"Content-Length: {len(urllib.parse.quote_plus(self.body))}\r\n"
                  # else:
                  self.fullreq += f"Content-Length: {len(self.body)}\r\n"


            # set up other headers
            # FIXME self.headers is empty after adding headers, for some reason
            # print("ITEMS!", self.headers)
            # for header, value in self.headers.items():
            #       print(f"Adding header {header}")
            #       self.fullreq += f"{header}: {value}\r\n"

            self.fullreq += "\r\n"
            # set up body
            if len(self.body) > 0:
                  # if self.body.count('&') > 1:
                  #       self.fullreq += f"{urllib.parse.quote_plus(self.body)}\r\n"
                  # else:
                  self.fullreq += f"{self.body}\r\n"
                  
            self.fullreq += "\r\n"

           
            #print("[+] Rendered request...")
            #print(repr(self.fullreq))
            #print()
            #print(self.fullreq)


      @staticmethod
      def create_run_thread_group(requests: List):
            """
            Convert a list of requests to threads and run each thread.
            
            :param: requests is a list of SimpleHTTPRequest objects
            """

            # convert to threads
            threads = [threading.Thread(target=req.request) for req in requests]
            #threads = [threading.Thread(target=req.request, kwargs={"filename": req.filename, "mode": req.mode}) for req in requests[:1]]
            #pprint(threads)
            for thread in threads:
                  thread.start()
                  #print("Waiting...")
                  #thread.join()

            for thread in threads:
                  thread.join()


# crawling functions

def crawl(start: str, domain: str, procs=6):
      """
      Call a specific domain, from a start

      :param: start is the starting page to look at, a full URL
      :param: domain is a domain to keep within
      :param: procs is the number of processes to spawn. default of 6
      """

      #sys.setrecursionlimit(50000)

      proclist = [None]*procs
      daboss = Manager()

      emails = daboss.dict() # email => depth ?
      # email => True for if we have visited. Manager doesn't appear to have a set()
      # still use .get() to avoid KeyError
      visited_links = daboss.dict()
      # tuple of (link => depth)
      # queue
      queued_links = queue.Queue()

      # add first link to spider on, depth of 0
      queued_links.put((start, 0))

      for i in range(procs):
            # proclist[i] = Process(
            #       target=worker_entrypoint, 
            #       args=(emails, visited_links, queued_links, domain, i,),
            # )
            proclist[i] = threading.Thread(
                  target=worker_entrypoint,
                  args=(emails, visited_links, queued_links, domain, i)
            )
            proclist[i].start()

      for proc in proclist:
            proc.join()

      depth0 = StringIO()
      depth1 = StringIO()
      depth2 = StringIO()
      depth3 = StringIO()
      depth4 = StringIO()

      
      for email, depth in emails.items():
            if depth == 0:
                  depth0.write(email + "\n")
            elif depth == 1:
                  depth1.write(email + "\n")
            elif depth == 2:
                  depth2.write(email + "\n")
            elif depth == 3:
                  depth3.write(email + "\n")
            elif depth == 4:
                  depth4.write(email + "\n")
      
      d0fd = open("depth0.txt", "w")
      d1fd = open("depth1.txt", "w")
      d2fd = open("depth2.txt", "w")
      d3fd = open("depth3.txt", "w")
      d4fd = open('depth4.txt', "w")

      d0fd.write(depth0.getvalue())
      d1fd.write(depth1.getvalue())
      d2fd.write(depth2.getvalue())
      d3fd.write(depth3.getvalue())
      d4fd.write(depth4.getvalue())

      d0fd.close()
      d1fd.close()
      d2fd.close()
      d3fd.close()
      d4fd.close()
      
      print("\n\n\n\nEmails counted:", len(emails))

def worker_entrypoint(emails: dict, visited_links: dict, queued_links: queue.Queue, domain: str, proc: int):
      """
      The entrypoint for worker processes.

      Methodology:
      1. Pull next link from "queue"
      2. Check if it is in visited links
      3. If not, request the page

      """
      print("Thread:", proc, "spinning up!")
      waitcounter = 0
      while not queued_links.empty() or waitcounter < 2:
            link = ""
            depth = 0

            # if len(emails) > 2000:
            #       break

            try:
                  thing = queued_links.get(block=True, timeout=4)
                  
                  link, depth = thing # didn't squash a bug here
                  #print(queued_links)
            except: # cannot pop() from empty list, as well as other Manager errors here
                  # let's wait and see if other processes add more links
                  print(f"THREAD {proc} : WAITING...", queued_links.qsize())
                  waitcounter += 1
                  #time.sleep(1)
                  continue

            waitcounter = 0
            

            print(f"THREAD {proc} || queue: {queued_links.qsize()} || depth: {depth} || waits: {waitcounter} || visited: {len(visited_links)} || emails: {len(emails)} || VISITING: {link} :D")

            # if link.endswith(".pdf"):
            #       # don't waste our time downloading PDFs
            #       continue

            # if depth is greater than 4, don't scan
            if depth > 4:
                  continue
            
            # ensure we haven't already been here before
            if link in visited_links:
                  #print(f"THREAD {proc}: {waitcounter}: emails: {len(emails)}: Already visited {link} :D")
                  continue

            visited_links[link] = True
            
            #
            # now that we have a link, we can parse and request it
            #print(link, depth)
            #parsed = SimpleHTTPRequest.urlparser(link)
            parsed = up(link)
            #print(parsed)
            https = True if parsed.scheme == "https" else False
            port = 443 if https else 80 # WARN: assumes 80 or 443
            #print("Port is:", port)
            r = SimpleHTTPRequest(
                  method="GET",
                  hostname=parsed.netloc,
                  resource=parsed.path if len(parsed.path) > 0 else "/",
                  https=https,
                  port=port
            )

            r.request()

            if None in (r.respbody, r.respheadersdict, r.respheaders):
                  print(f"[-] Request for link: {link} failed.")
                  #visited_links[link] = True
                  continue

            if "text/html" not in r.respheadersdict.get("Content-Type", ""):
                  #visited_links[link] = True
                  continue

            #print("After", parsed)
            #print(r.respbody)
            # after requesting, search with BeautifulSoup

            souptime = BeautifulSoup(r.respbody, "lxml")

            # grab all emails from the page
            #print(f"THREAD {proc}: waits: {waitcounter} || emails: {len(emails)} ||  Searching Emails!")
            find_emails(r.respbody, emails, depth)

            # grab all links and add them to queue with higher depth
            #print(f"THREAD {proc}: waits: {waitcounter} || emails: {len(emails)} ||  Grabbing HREFs!")
            links = souptime.find_all("a", href=True)
            for link in links:
                  href = link["href"].rstrip("/")
                  p = up(href)
                  #print("PATH:", p.path)
                  if p.scheme.startswith("http") and p.netloc.endswith("rit.edu"):
                        #print(href, p)
                        if href not in visited_links:
                              if href.endswith(".pdf") or "#" in href or depth+1 > 3:
                                    # we don't want to go here
                                    visited_links[href] = True
                                    continue
                              queued_links.put((href, depth+1))
                  elif len(p.path) > 0 and p.path[0] == "/" and "#" not in p.path:
                        newpath = p.path
                        hostname = domain
                        secure = "https://" if r.https else "http://"
                        url = secure + hostname + newpath
                        url = url.rstrip("/")
                        #print("UNDER CONSIDERATION:", url)
                        if url.endswith(".pdf") or "#" in url or depth+1 > 3:
                              # we don't want to go here
                              visited_links[url] = True
                              continue
                        if url not in visited_links:
                              queued_links.put((url, depth+1))


            
            # add current link to visited_links set
            # visited_links[link] = True
            
      queued_links.task_done()
      print(f"THREAD {proc}: Dismissed!")
      
def find_emails(html: str, emails: dict, depth: int):
      """
      Pull all emails out of a web page and add to dictionary
      """
      #print(type(html))
      toadd = set(re.findall(r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+", str(html), re.I))
      for email in toadd:
            if email[-3:] in {"org", "com", "gov", "edu", "net"}:
                  if email.lower() not in emails:
                        emails[email.lower()] = depth

