#!/usr/bin/env python
# import CGIHTTPServer
#
# def main():
#
#     server_address = ('', 8000)
#     handler = CGIHTTPServer.CGIHTTPRequestHandler
#     handler.cgi_directories = ['/cgi']
#     server = CGIHTTPServer.BaseHTTPServer.HTTPServer(server_address, handler)
#     try:
#         server.serve_forever()
#     except KeyboardInterrupt:
#         server.socket.close()
# 
# if __name__ == '__main__':
#     main()

import SimpleHTTPServer
import SocketServer

PORT = 8000

Handler = SimpleHTTPServer.SimpleHTTPRequestHandler

httpd = SocketServer.TCPServer(("", PORT), Handler)

print "serving at port", PORT
httpd.serve_forever()
