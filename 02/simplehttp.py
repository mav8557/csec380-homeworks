import socket
import urllib.parse

class SimpleHTTPRequest:
      def __init__(
                  self,
                  *args,
                  method="GET",
                  hostname="csec380-core.csec.rit.edu",
                  port=82,
                  resource = "/",
                  useragent = "richardgill",
                  content_type="application/x-www-form-urlencoded",
                  body=''
      ):
            self.method = method
            self.hostname = hostname
            self.port = port
            self.resource = resource
            self.useragent = useragent
            self.content_type = content_type
            self.url = f"http://{hostname}:{port}/{resource}"
            self.headers = {}
            self.body = body # tokens, stuff like that
            self.fullreq = "" # the full request to be sent

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
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((self.hostname, self.port))
            try:
                  sock.sendall(self.fullreq.encode())
            except:
                  raise
            resp = sock.recv(8092).decode()
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
            if self.port != 80:
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
            self.fullreq += f"Accept-Language: en-us\r\n"

            # encoding
            self.fullreq += f"Accept-Encoding: text/html\r\n"

            # content-type
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
