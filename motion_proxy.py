# -*- coding: utf-8 -*-
"""
MJPEG Proxy Server
"""
import BaseHTTPServer
import urlparse
import socket
import datetime

STREAM_HOST = 'localhost'
STREAM_PORT = 8081
PROXY_PORT = 8002


def grab_mjpeg_frame(host, port):
    """
    Function is getting one frame from MJPEG stream
    The base of this code was taken from https://gist.github.com/russss/1143799
    """

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
        return None

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
    s.close()
    return image


class GetHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    """
    GetHandler
    """

    def do_GET(self):
        # parsed_path = urlparse.urlparse(self.path)
        if self.path.endswith(".jpg"):
            print(self.path)
            self.send_response(200)
            self.send_header('Content-type', 'image/jpg')
            self.send_header('Cache-Control', 'no-cache')
            self.end_headers()
            self.wfile.write(grab_mjpeg_frame(STREAM_HOST, STREAM_PORT))
            return
        else:
            message = """
            <!DOCTYPE html>
               <html>
               <body>
                   <meta charset="utf-8">
                   <meta name="viewport"
                     content="width=device-width,
                              initial-scale=1, maximum-scale=1">
                   <div id="core" align="center">
                     <h2>%s</h2>
                     <a href="./"><img src="image.jpg" alt="Motion Server"></a>
                   </div>
               </body>
               </html>""" % datetime.datetime.now().strftime('%c')

            self.send_response(200)
            self.end_headers()
            self.wfile.write(message)
            return

if __name__ == '__main__':
    import BaseHTTPServer
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('stream_host_port', metavar = 'host:port',help='MJPEG stream host:port')
    parser.add_argument('proxy_port', help='proxy port')
    args = parser.parse_args()
    STREAM_HOST,STREAM_PORT = args.stream_host_port.split(':')
    STREAM_PORT = int(STREAM_PORT)
    PROXY_PORT = int(args.proxy_port)

    server = BaseHTTPServer.HTTPServer(('', PROXY_PORT), GetHandler)
    print('Starting MJPEG proxy server at port %d)'%(PROXY_PORT))
    server.serve_forever()
