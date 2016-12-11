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

import os, signal, select, json, traceback, cgi

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

import spacescanner

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
        self.strategyManager = None

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
    server_version = 'SpaceScanner web server ' + SPACESCANNER_VERSION

    # overrides base class function, because in some versions
    # it tries to resolve dns and fails...
    def log_message(self, format, *args):
        g.log(LOG_DEBUG, "%s - - [%s] %s" %
                         (self.client_address[0],
                          self.log_date_time_string(),
                          format % args))

    def end(self):
        self.wfile.close()

    def saveInFile(self, contents, filename):
        dirname = os.path.join(SELF_PATH, "tmpweb")
        try:
            os.mkdir(dirname)
        except:
            pass
        filename = os.path.join(dirname, filename)
        with open(filename, "w") as f:
            f.write(contents.encode("UTF-8"))
        return filename

    def sendDefaultHeaders(self, contents, isJSON = True, contentType = None):
        if isJSON:
            self.send_header('Content-Type', 'application/json')
        elif contentType:
            self.send_header('Content-Type', contentType)
        else:
            self.send_header('Content-Type', 'text/plain')
        # disable caching
        self.send_header('Cache-Control', 'no-store')
        self.send_header('Connection', 'close')
        if contents != None:
            self.send_header('Content-Length', len(contents))

    def serveError(self, qs, code=404, message=""):
        self.send_response(code)
        self.sendDefaultHeaders(message)
        self.end_headers()
        self.end()

    def serveBody(self, response, qs):
        self.wfile.write(toBytes(response))
        self.end()

    def do_GET(self):
        o = urlparse(self.path)
        qs = parse_qs(o.query)

        isJSON = True
        contentType = "text/plain"
        sm = InterruptibleHTTPServer.serverInstance.strategyManager
        if o.path == '/index.html' or o.path == "/":
            isJSON = False
            contentType = "text/html"
            try:
                with open(os.path.join(SELF_PATH, "web", "index.html")) as f:
                    response = f.read()
            except:
                self.serveError(qs)
                return
        elif o.path[-4:] == ".css":
            isJSON = False
            contentType = "text/css"
            try:
                with open(os.path.join(SELF_PATH, "web", o.path[1:])) as f:
                    response = f.read()
            except:
                self.serveError(qs)
                return
        elif o.path[-3:] == ".js":
            isJSON = False
            contentType = "application/js"
            try:
                with open(os.path.join(SELF_PATH, "web", o.path[1:])) as f:
                    response = f.read()
            except:
                self.serveError(qs)
                return
        elif o.path[-4:] == ".png":
            isJSON = False
            contentType = "image/png"
            try:
                with open(os.path.join(SELF_PATH, "web", o.path[1:])) as f:
                    response = f.read()
            except:
                self.serveError(qs)
                return
        elif o.path[-4:] == ".jpg":
            isJSON = False
            contentType = "image/jpg"
            try:
                with open(os.path.join(SELF_PATH, "web", o.path[1:])) as f:
                    response = f.read()
            except:
                self.serveError(qs)
                return
        elif "font" in o.path:
            isJSON = False
            contentType = "font/opentype"
            try:
                with open(os.path.join(SELF_PATH, "web", o.path[1:])) as f:
                    response = f.read()
            except:
                self.serveError(qs)
                return

        elif o.path == '/status':
            # active jobs
            response = {"isActive" : sm.isActive(),
                        "isExecutable" : sm.isExecutable,
                        "resultsPresent" : sm.getNumFinishedJobs() > 0}
        elif o.path == '/allstatus':
            response = sm.ioGetAllJobs(qs)
        elif o.path == '/activestatus':
            response = sm.ioGetActiveJobs(qs)
        elif o.path[:4] == '/job':
            # specific job
            response = sm.ioGetJob(qs, o.path[5:])
        elif o.path[:7] == '/config':
            response = sm.ioGetConfig(qs)
            print("config=", response)
        elif o.path[:8] == '/results':
            response = sm.ioGetResults(qs)
            isJSON = False # the results are in .csv format
            contentType = "text/csv"
        elif o.path == '/stopall':
            response = sm.ioStopAll(qs)
        elif o.path[:5] == '/stop':
            response = sm.ioStop(qs, o.path[6:])
        else:
            self.serveError(qs)
            return

        if isJSON:
            response = ENC.encode(response)

        self.send_response(200)
        self.sendDefaultHeaders(response, isJSON, contentType)
        self.end_headers()
        self.serveBody(response, qs)


    def postModel(self, qs):
        # error if running
        sm = InterruptibleHTTPServer.serverInstance.strategyManager
        if sm is not None and sm.isActive():
            return self.serveError(qs, 503, "Already running")

        contentLength = int(self.headers.get('content-length', 0))
        received = ""

        # Parse the form data posted
        form = cgi.FieldStorage(
            fp = self.rfile, 
            headers = self.headers,
            environ = {'REQUEST_METHOD' : 'POST',
                       'CONTENT_TYPE': self.headers['Content-Type'],
                   })
        for field in form.keys():
            field_item = form[field]
            if field_item.filename:
                # The field contains an uploaded file
                received = field_item.file.read(contentLength).decode("utf-8")
                break

        if not received:
            return self.serveError(qs, 400, "No valid file data received")

        # write the model
        filename = self.saveInFile(received, "model.cps")
        # check if the model is all right
        InterruptibleHTTPServer.serverInstance.strategyManager.prepare(isDummy = False)

        # self.respondToPost(200, filename, False) # these req/resp are not in json format
        self.respondToPost(200, {"filename" : filename})


    def postConfig(self, qs):
        contentLength = int(self.headers.get('content-length', 0))
        received = self.rfile.read(contentLength).decode("utf-8")

        # error if running
        sm = InterruptibleHTTPServer.serverInstance.strategyManager
        if sm is not None and sm.isActive():
            return self.serveError(qs, 503, "Already running")

        # else start running
        filename = self.saveInFile(received, "config.json")
        sm = spacescanner.startFromWeb(filename)
        if sm is None:
            return self.serveError(qs, 500, "Cannot start SpaceScanner optimizations")
        # set it only if not none
        InterruptibleHTTPServer.serverInstance.strategyManager = sm

        self.respondToPost(200, {"status" : "OK"})

    def respondToPost(self, code, response, isJSON = True):
        print("respond to post:")
        print(response)
        if isJSON:
            response = ENC.encode(response)
        self.send_response(200)
        self.sendDefaultHeaders(response, isJSON)
        self.end_headers()
        self.serveBody(response, qs = {})

    def do_POST(self):
        o = urlparse(self.path)
        qs = parse_qs(o.query)
   
        if o.path == "/model":
            self.postModel(qs)
        elif o.path == "/start":
            self.postConfig(qs)
        else:
            self.serveError(qs)
