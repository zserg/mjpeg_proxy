"""
Motion Proxy Server
"""
from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse

PORT = 8002
class GetHandler(BaseHTTPRequestHandler):
    """
    GetHandler
    """

    def do_GET(self):
        parsed_path = urlparse(self.path)
        message_parts = [
            'CLIENT VALUES:',
            'client_address=%s (%s)' % (self.client_address,
            self.address_string()),
            'command=%s' % self.command,
            'path=%s' % self.path,
            'real path=%s' % parsed_path.path,
            'query=%s' % parsed_path.query,
            'request_version=%s' % self.request_version,
            '',
            'SERVER VALUES:',
            'server_version=%s' % self.server_version,
            'sys_version=%s' % self.sys_version,
            'protocol_version=%s' % self.protocol_version,
            '',
            'HEADERS RECEIVED:',
        ]
        for name, value in sorted(self.headers.items()):
            message_parts.append('%s=%s' % (name, value.rstrip()))
        message_parts.append('')
        message = '\r\n'.join(message_parts)
        self.send_response(200)
        self.end_headers()
        self.wfile.write(bytes(message, encoding='utf-8'))
        return

if __name__ == '__main__':
    from http.server import BaseHTTPRequestHandler
    from http.server import HTTPServer
    server = HTTPServer(('', PORT), GetHandler)
    print('Starting server, use <Ctrl-C> to stop')
    server.serve_forever()
