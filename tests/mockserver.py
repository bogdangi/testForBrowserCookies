#!/usr/bin/env python

import BaseHTTPServer
import Cookie
import sys
import os
import ssl

COOKIES_PATHS = {
    '/set_cookie': 'cookie_monster=happy',
    '/set_cookie/rocket_launcher': 'Part_Number="Rocket_Launcher_0001"; Version=1; Path=/',
    '/set_cookie/path/riding_rocket': 'Part_Number="Riding_Rocket_0023"; Version=1; Path=/path',
    '/set_cookie/customer': 'Customer="WILE_E_COYOTE"; Version=1; Path=/',
    '/set_cookie/shipping': 'Shipping="FedEx"; Version=1; Path=/',
    }


class WebRequestHandler(BaseHTTPServer.BaseHTTPRequestHandler):

    def do_HEAD(self):
        self.send_response(200, "No payment required")
        self.send_header('x-powered-by', 'PHP')
        self.send_header('x-request-user-agent', self.headers.get(
            'user-agent', '(unknown)'))
        self.end_headers()

    def do_DELETE(self):
        self.send_response(200, "OK")
        self.end_headers()
        self.wfile.write(self.requestline)
        self.finish()

    def do_PATCH(self):
        self.send_response(200, "Patch request ok")
        self.end_headers()
        self.wfile.write("Got a patch request")
        self.finish()

    def do_GET(self):
        if self.path == '/200':
            self.send_response(200, "OK")
            self.end_headers()
            self.wfile.write("Everything is ok!")
            self.finish()
        elif self.path == '/200_with_location_header':
            self.send_response(200, "OK")
            self.send_header('Location', '/200')
            self.end_headers()
        elif self.path == '/301_no_location_header':
            self.send_response(301, "Redirect with no location header, hehe")
            self.end_headers()
        elif self.path == '/302':
            self.send_response(302, "Redirect")
            self.send_header('Location', '/200')
            self.end_headers()
        elif self.path == '/304':
            if 'If-Modified-Since' in self.headers:
                self.send_response(304, "Not Modified")
            else:
                self.send_response(200, "Modified")
            self.send_header('Last-Modified', 'February')
            self.end_headers()
        elif self.path == '/404':
            self.send_response(404, "Not Found")
        elif self.path == '/418':
            self.send_response(418, "I'm a teapot")
        elif self.path == '/503':
            self.send_response(503, "Some error")
        elif self.path == '/sesame':
            if 'Authorization' in self.headers and self.headers['Authorization'] == 'Basic QWxhZGRpbjpvcGVuIHNlc2FtZQ==':
                self.send_response(200, "Sesame open!")
                self.end_headers()
                self.wfile.write("Welcome to sesame street!")
                self.finish()
            else:
                self.send_response(401, "Sesame closed!")
                self.send_header(
                    'WWW-Authenticate', 'Basic realm="Secure Area"')
                self.end_headers()
        elif self.path == '/hostname':
            self.send_response(200, 'OK')
            self.end_headers()
            self.wfile.write("***%s***" % self.headers['Host'])
            self.finish()
        elif self.path == '/duplicate_header':
            self.send_response(200, 'OK')
            self.send_header('Duplicate', 'Yes')
            self.send_header('Duplicate', 'Si!')
            self.end_headers()
            self.finish()
# Start cookies section
        elif self.path in COOKIES_PATHS.keys():
            self.send_response(200, 'OK')
            self.send_header('Set-Cookie', COOKIES_PATHS[self.path])
            self.end_headers()
            self.wfile.write("The cookie <u>%s</u> has been set."%COOKIES_PATHS[self.path])
            self.finish()
        elif self.path.endswith('/all_cookies'):
            self.send_response(200, 'OK')
            self.end_headers()
            self.wfile.write("<h1>Cookies verification page</h1>")
            self.wfile.write("<p>%s</p>" % self.headers.get('Cookie', ''))
            self.finish()
        elif self.path == '/delete_cookies':
            cookies = Cookie.SimpleCookie()
            cookies.load(self.headers.get('Cookie', ''))
            self.send_response(200, 'OK')
            for cookie in cookies.values():
                cookie['expires'] = 0
                self.send_header(
                    'Set-Cookie',
                    str(cookie).split('Set-Cookie: ')[-1])
            self.end_headers()
            self.wfile.write("The cookies has been expired.")
            self.finish()
# End cookies section
        else:
            self.send_error(500)

    def do_POST(self, *args, **kwargs):
        if self.path == '/echo':
            data = self.rfile.read(int(self.headers['Content-Length']))
            self.rfile.close()
            self.send_response(200, "OK")
            self.send_header('Content-Type', 'text/plain; charset=utf-8')
            self.end_headers()
            self.wfile.write(data)
            self.finish()
        elif self.path == '/content_type':
            self.send_response(200, "OK")
            self.wfile.write(self.rfile.read)
            self.end_headers()
            self.wfile.write(self.headers['Content-Type'])
            self.finish()
        elif self.path == '/kill':
            global server
            self.send_response(201, "Killing myself")
            server.socket.close()
            sys.exit(0)
        else:
            self.send_error(500)

    do_PUT = do_POST

PORT = int(sys.argv[1])
server = BaseHTTPServer.HTTPServer(('localhost', PORT), WebRequestHandler)
scheme = 'http'

if '--ssl' in sys.argv:
    scheme = 'https'

    cert = os.path.abspath(
        os.path.join(os.path.dirname(__file__), 'rfhttplibmockserver.pem'))

    server.socket = ssl.wrap_socket(
        server.socket,
        certfile=cert,
        keyfile=cert,
        server_side=True,
    )

print 'Starting server on %s://localhost:%d/' % (scheme, PORT)

server.serve_forever()
