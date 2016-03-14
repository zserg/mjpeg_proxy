# -*- coding: utf-8 -*-
"""
Motion Proxy Server
"""
import BaseHTTPServer
import urlparse
import socket
import sys 
import os

STREAM_PORT = 8081
PROXY_PORT = 8002
host = 'localhost'

def get_image(host, port):

  s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  s.connect((host, int(port)))

  fh = s.makefile()

  # Read in HTTP headers:
  line = fh.readline()
  while line.strip() != '': 
      parts = line.split(':')
      if len(parts) > 1 and parts[0].lower() == 'content-type':
          # Extract boundary string from content-type
          content_type = parts[1].strip()
          boundary = content_type.split(';')[1].split('=')[1]
      line = fh.readline()

  if not boundary:
      raise Exception("Can't find content-type")

  # Seek ahead to the first chunk
  while line.strip() != boundary:
      line = fh.readline()

  # Read in chunk headers
  while line.strip() != '': 
      parts = line.split(':')
      if len(parts) > 1 and parts[0].lower() == 'content-length':
          # Grab chunk length
          length = int(parts[1].strip())
      line = fh.readline()

  image = fh.read(length)

  with open('image.jpg', 'w') as out_fh:
      out_fh.write(image)

  s.close()

class GetHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    """
    GetHandler
    """

    def do_GET(self):
        parsed_path = urlparse.urlparse(self.path)
#        message_parts = [
#            'CLIENT VALUES:',
#            'client_address=%s (%s)' % (self.client_address,
#            self.address_string()),
#            'command=%s' % self.command,
#            'path=%s' % self.path,
#            'real path=%s' % parsed_path.path,
#            'query=%s' % parsed_path.query,
#            'request_version=%s' % self.request_version,
#            '',
#            'SERVER VALUES:',
#            'server_version=%s' % self.server_version,
#            'sys_version=%s' % self.sys_version,
#            'protocol_version=%s' % self.protocol_version,
#            '',
#            'HEADERS RECEIVED:',
#        ]
        if self.path.endswith(".jpg"):
            print(self.path)
            f=open('.'+self.path)
            self.send_response(200)
            self.send_header('Content-type',        'image/jpg')
            self.end_headers()
            self.wfile.write(f.read())
            f.close()
            return
        else:  
            get_image(host, STREAM_PORT)
            message = """     <!DOCTYPE html>
                     <html>
                     <body>
                     <meta charset="utf-8">
                     <meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1">
                     <h2>Гавриловцы</h2>
                     <img src="image.jpg" alt="Гавриловцы" >

                     </body>
                     </html>"""
              
            self.send_response(200)
            self.end_headers()
            self.wfile.write(message)
            return

if __name__ == '__main__':
    import BaseHTTPServer
    server = BaseHTTPServer.HTTPServer(('', PROXY_PORT), GetHandler)
    print('Starting server, use <Ctrl-C> to stop')
    server.serve_forever()
