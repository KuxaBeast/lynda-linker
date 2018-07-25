#!/usr/bin/env python3
from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.parse
from LyndaLinker import LyndaLinker

class LyndaHTTPRequestHandler(BaseHTTPRequestHandler):
  def do_GET(self):
    response_addr = LyndaLinker().get_link(self.path[1:])

    if response_addr:
      self.send_response(302)
      self.send_header("Location", response_addr)
    else:
      self.send_response(400)
    self.end_headers()

  def do_POST(self):
    content_length = int(self.headers['Content-Length'])
    post = urllib.parse.unquote(self.rfile.read(content_length).decode("UTF-8"))
    ppost = {}
    for param in post.split('&'):
      keyval = param.split('=')
      ppost[keyval[0]] = keyval[1]
    response_addr = LyndaLinker().get_link(ppost['lyndaurl'], ppost['quality'])
    print(ppost)

    if response_addr:
      self.send_response(302)
      self.send_header("Location", response_addr)
    else:
      self.send_response(400)
    self.end_headers()

if __name__ == "__main__":
  address = ("0.0.0.0", 8555)
  httpd = HTTPServer(address, LyndaHTTPRequestHandler)
  httpd.serve_forever()