# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#  * Redistributions of source code must retain the above copyright notice,
#    this list of  conditions and the following disclaimer.
#  * Redistributions in binary form must reproduce the above copyright
#   notice, this list of conditions and the following disclaimer in the
#   documentation and/or other materials provided with the distribution.
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS OR
# CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
# EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
# PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS;
# OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
# WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR
# OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF
# ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

#
# Author: Atis Elsts, 2016
#

import os, signal, select, json, traceback

from util import *
import g

if isPython3():
    from http.server import *
    from socketserver import *
    from urllib.parse import *
else:
    from BaseHTTPServer import *
    from SocketServer import *
    from urlparse import *

################################################

# Note: this is a single-threaded server, to keep things simple!
class InterruptibleHTTPServer(HTTPServer):
    serverInstance = None

    def __init__(self, address, handler):
        HTTPServer.__init__(self, address, handler)
        # for Python 2.6 compatibility
        if not hasattr(self, '_BaseServer__shutdown_request'):
            self._BaseServer__shutdown_request = False
        InterruptibleHTTPServer.serverInstance = self

    # Overrides BaseServer function to get a better control over interrupts
    def serve_forever(self, poll_interval = 0.5):
        """Handle one request at a time until shutdown.

        Polls for shutdown every poll_interval seconds. Ignores
        self.timeout. If you need to do periodic tasks, do them in
        another thread.
        """
        self._BaseServer__is_shut_down.clear()
        try:
            while not self._BaseServer__shutdown_request:
                # XXX: Consider using another file descriptor or
                # connecting to the socket to wake this up instead of
                # polling. Polling reduces our responsiveness to a
                # shutdown request and wastes cpu at all other times.
                r, w, e = select.select([self], [], [], poll_interval)
                if self in r:
                    self._handle_request_noblock()
        except Exception as e:
            g.log(LOG_ERROR, "base server exception:")
            g.log(LOG_ERROR, str(e))
            g.log(LOG_ERROR, traceback.format_exc())
        finally:
            self._BaseServer__shutdown_request = False
            self._BaseServer__is_shut_down.set()
            if os.name == "posix":
                # kill the process to make sure it exits
                os.kill(os.getpid(), signal.SIGKILL)

    def close(self):
        self._BaseServer__shutdown_request = True

################################################

class HttpServerHandler(BaseHTTPRequestHandler):
    server_version = 'CoRunner Web Server ' + CORUNNER_VERSION

    # overrides base class function, because in some versions
    # it tries to resolve dns and fails...
    def log_message(self, format, *args):
        g.log(LOG_DEBUG, "%s - - [%s] %s" %
                         (self.client_address[0],
                          self.log_date_time_string(),
                          format % args))

    def end(self):
        self.wfile.close()

    def sendDefaultHeaders(self, contents, isJSON = True):
        if isJSON:
            self.send_header('Content-Type', 'application/json')
        else:
            self.send_header('Content-Type', 'text/plain')
        # disable caching
        self.send_header('Cache-Control', 'no-store')
        self.send_header('Connection', 'close')
        if contents != None:
            self.send_header('Content-Length', len(contents))

    def serveError(self, qs):
        contents = ""
        self.send_response(404)
        self.sendDefaultHeaders(contents)
        self.end_headers()
        self.end()

    def serveBody(self, response, qs):
        self.wfile.write(toBytes(response))
        self.end()

    def processGet(self, path, qs):
        isJSON = True
        sm = InterruptibleHTTPServer.serverInstance.statsManager
        if path == '/status' or path == "/":
            response = sm.getResourceList(qs)
        elif path[:7] == '/latest':
            response = sm.getResource(qs, None)
        elif path[:5] == '/jobs':
            response = sm.getResource(qs, path[6:])
        else:
            self.serveError(qs)
            return

        if isJSON:
            response = ENC.encode(response)

        self.send_response(200)
        self.sendDefaultHeaders(response, isJSON)
        # to enable cross-site scripting
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.serveBody(response, qs)

    def do_GET(self):
        o = urlparse(self.path)
        qs = parse_qs(o.query)

        self.processGet(o.path, qs)

    def do_POST(self):
        o = urlparse(self.path)
        qs = parse_qs(o.query)
        self.serveError(qs)

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Headers", "content-type")
        self.send_header("Content-Type", "text/plain")
        self.send_header("Content-Length", "0")
        self.end_headers()
        self.end()
