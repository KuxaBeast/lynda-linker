#!/usr/bin/env python3
from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.parse
from linker import LyndaLinker

class LyndaHTTPRequestHandler(BaseHTTPRequestHandler):
  def do_GET(self):
    linker = LyndaLinker()
    #purl = linker.parseUrl(self.path[1:])

    query = urllib.parse.parse_qs(self.path[2:])

    response_addr = linker.get_link(query['courseid'][0], query['videoid'][0], query['qual'][0])

    if response_addr:
      self.send_response(302)
      self.send_header("Location", response_addr)
    else:
      self.send_response(400)
    self.end_headers()

  # def do_POST(self):
  #   content_length = int(self.headers['Content-Length'])
  #   post = urllib.parse.unquote(self.rfile.read(content_length).decode("UTF-8"))
  #   ppost = {}
  #   for param in post.split('&'):
  #     keyval = param.split('=')
  #     ppost[keyval[0]] = keyval[1]

  #   linker = LyndaLinker()
  #   purl = linker.parseUrl(ppost['lyndaurl'])
  #   response_addr = linker.get_link(purl[0], purl[1], ppost['quality'])
  #   print(ppost)

  #   if response_addr:
  #     self.send_response(302)
  #     self.send_header("Location", response_addr)
  #   else:
  #     self.send_response(400)
  #   self.end_headers()

if __name__ == "__main__":
  address = ("0.0.0.0", 8555)
  httpd = HTTPServer(address, LyndaHTTPRequestHandler)
  httpd.serve_forever()