import socket
import ssl
import urllib.parse

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
                  body=''
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
            self.body = body # tokens, stuff like that
            self.fullreq = "" # the full request to be sent
            self.resp = None # respose is None until we recv from the server

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
            
            resp = ""
            while chunk := self.sock.recv(4096):
                  resp += chunk.decode("utf-8")

            self.resp = resp
            bits = resp.split("\r\n")
            bodyindex = bits.index('')
            self.respheaders = bits[:bodyindex]
            self.respbody = "".join(bits[bodyindex+1:])
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
            print(repr(self.fullreq))
            print()
            print(self.fullreq)
