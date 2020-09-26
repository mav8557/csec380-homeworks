import socket
import ssl
import urllib.parse
from pprint import pprint
from typing import List
import threading

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

            if self.https:
                  # wrap encryption around socket if using https
                  self.sock = ssl.wrap_socket(self.sock, ssl_version=ssl.PROTOCOL_TLS)
            

            self.sock.connect((self.hostname, self.port))
            try:
                  self.sock.sendall(self.fullreq.encode())
            except:
                  raise
            
            resp = b""
            while chunk := self.sock.recv(4096):
                  resp += chunk #.decode("utf-8")

            self.resp = resp # full response
            # headers
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
            #print(self.respheadersdict)

            if self.respheadersdict["status_code"] in {301, 302}:
                  # follow redirect
                  newpath = self.resource.split("/")
                  #print(newpath[1:len(newpath)-1])
                  finalpath = "/" + "/".join(newpath[1:len(newpath)-1]) + "/" + self.respheadersdict["Location"]
                  #print("NEW RESOURCE:", finalpath)
                  self.resource = finalpath
                  self.request()
                  
            
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

           
            print("[+] Rendered request...")
            #print(repr(self.fullreq))
            print()
            print(self.fullreq)


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
