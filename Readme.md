# MJPEG Proxy Server

This is a simple MJPEG proxy server. Server connects to MJPEG stream, recevies HTTP request from client (browser) and sends back the response as a html page with one frame grabbed from stream. The purpose of the server is to provide access to MJPEG server (е.g. motion) from some mobile browsers, that don't support a live MJPEG stream.

## Usage
`python mjpeg_proxy.py host:port proxy_port`

where:

`host:port` - mjpeg stream host address and port

`proxy_port` - port of proxy server

### Acknowledgments
Part of the code is based on https://gist.github.com/russss/1143799
