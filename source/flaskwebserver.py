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
# Author: Atis Elsts, 2016-2019
#

import os
import threading
import copy
from flask import Flask, Response, jsonify, request, send_from_directory, abort
from gevent.pywsgi import WSGIServer
        
from util import *
import g

import start

################################################

WEB_CONTENT_DIRECTORY = os.path.join(SELF_PATH, "web")
WEB_UPLOAD_DIRECTORY = os.path.join(SELF_PATH, "tmpweb")
CONFIG_FILE_NAME = os.path.join(WEB_UPLOAD_DIRECTORY, "config.json")
MODEL_FILE_NAME = os.path.join(WEB_UPLOAD_DIRECTORY, "model.cps")

################################################

flask = Flask(__name__,
              static_url_path='',
              static_folder=WEB_CONTENT_DIRECTORY)

################################################

class Logger:
    # wrapper call to redirect WSGIServer output to the common logger
    @staticmethod
    def write(s):
        g.log(LOG_DEBUG, s[:-1])

################################################

class Server(WSGIServer):
    serverInstance = None

    def __init__(self, address, strategyManager):
        WSGIServer.__init__(self, address, flask, log=Logger)
        self.strategyManager = strategyManager
        Server.serverInstance = self
       
################################################
def doQuit():
    g.log(LOG_ERROR, "Terminating...")
    g.doQuit = True

################################################

def saveInFile(contents, filename):
    # make sure the directory exists
    try:
        os.mkdir(WEB_UPLOAD_DIRECTORY)
    except:
        pass

    if not os.path.isabs(filename):
        filename = os.path.join(WEB_UPLOAD_DIRECTORY, filename)

    # write file in that directory
    try:
        with open(filename, "wb") as f:
            if type(contents) is not bytes:
                contents = contents.encode("UTF-8")
            f.write(contents)
    except Exception as ex:
        g.log(LOG_ERROR, "webserver: cannot save to file {}: {}".format(filename, ex))

################################################

@flask.before_request
def sanitize_request():
    if request.method == "POST":
        if Server.serverInstance \
           and Server.serverInstance.strategyManager \
           and Server.serverInstance.strategyManager.isActive():
            return jsonify({"error" : "already running"})
    else:
        if Server.serverInstance is None \
           or Server.serverInstance.strategyManager is None:
            return jsonify({"error" : "not initialized"})

################################################

@flask.after_request
def disable_caching(response):
    response.headers["Cache-Control"] = "no-store"
    del response.headers["Date"]
    del response.headers["ETag"]
    del response.headers["Expires"]
    del response.headers["Last-Modified"]
    return response

################################################

@flask.route("/", methods=["GET"])
def index1():
    return send_from_directory(WEB_CONTENT_DIRECTORY, "index.html")

@flask.route("/index.html", methods=["GET"])
def index2():
    return send_from_directory(WEB_CONTENT_DIRECTORY, "index.html")

@flask.route("/status", methods=["GET"])
def status():
    sm = Server.serverInstance.strategyManager
    # active jobs
    response = {"isActive" : sm.isActive(),
                "isExecutable" : sm.isExecutable,
                "totalNumJobs" : sm.getTotalNumJobs(),
                "totalNumParams" : sm.getTotalNumParams(),
                "resultsPresent" : sm.getNumFinishedJobs() > 0,
                "error" : sm.lastError }
    # XXX: perhaps resetting this should be timer based?
    sm.lastError = ""
    return jsonify(response)

@flask.route("/allstatus", methods=["GET"])
def allstatus():
    response = Server.serverInstance.strategyManager.ioGetAllJobs(request.query_string)
    return jsonify(response)

@flask.route("/activestatus", methods=["GET"])
def activestatus():
    response = Server.serverInstance.strategyManager.ioGetActiveJobs(request.query_string)
    return jsonify(response)

@flask.route("/job", methods=["GET"])
def job():
    jobid = request.args.get('jobid')
    response = Server.serverInstance.strategyManager.ioGetJob(request.query_string, jobid)
    return jsonify(response)

@flask.route("/config", methods=["GET"])
def config():
    response = Server.serverInstance.strategyManager.ioGetConfig(request.query_string)
    return jsonify(response)

@flask.route("/results.csv", methods=["GET"])
def results():
    try:
        totalLimit = int(request.args.get('totallimit', 0))
    except:
        totalLimit = 0
    response = Server.serverInstance.strategyManager.ioGetResults(request.query_string, totalLimit)
    # this is csv, not json!
    return Response(response, mimetype='text/csv')

@flask.route("/stopall", methods=["GET"])
def stopall():
    response = Server.serverInstance.strategyManager.ioStopAll(request.query_string)
    return jsonify(response)

@flask.route("/stop", methods=["GET"])
def stop():
    jobid = request.args.get('jobid')
    response = Server.serverInstance.strategyManager.ioStop(request.query_string, jobid)
    return jsonify(response)

@flask.route("/terminate", methods=["GET"])
def terminate():
    g.log(LOG_ERROR, "Terminating upon user request")
    response = {"status" : "ok"}
    threading.Timer(1.0, doQuit).start()
    return jsonify(response)

@flask.route('/modelfile', methods = ['POST'])
def postModel():
    receivedModel = ""
    receivedExperimentalData = []

    if request.headers.get('Content-Type') == "application/json":
        # JSON object
        try:
            contents = request.get_json()
            receivedModel = contents.get("model", "")
            receivedExperimentalData = contents.get("experiment", "")
        except Exception as ex:
            g.log(LOG_INFO, "Failed to parse the model as JSON data: {}".format(ex))
    else:
        # form data
        try:
            for k in request.files:
                fs = request.files[k]
                received = fs.read().decode("utf-8")
                if startsWith(received, "<?xml") and ("<COPASI" in received):
                    receivedModel = received
                else:
                    # assume that all other files are experiment files.
                    # if other types of files are present, saving them
                    # will not harm the system in any case.
                    filename = fs.filename
                    g.log(LOG_INFO, "got filename: {}".format(filename))
                    receivedExperimentalData.append((filename, received))
        except TypeError as te:
            # the TypeError "not indexable" happens when trying the web test
            g.log(LOG_INFO, "Failed to parse CGI form: {}".format(te))

    if not receivedModel:
        abort(Response("No valid model file received\n", 400))

    # write the model and data files
    saveInFile(receivedModel, MODEL_FILE_NAME)
    for filename, data in receivedExperimentalData:
        saveInFile(data, os.path.basename(filename))

    # XXX: this is a hack that allows to guess the task type asking the web server for it.
    # This assumes that exp data is only set for parameter estimation tasks.
    if len(receivedExperimentalData):
        taskType = COPASI_TASK_PARAM_ESTIMATION
    else:
        taskType = COPASI_TASK_OPTIMIZATION

    # check if the model is all right
    sm = Server.serverInstance.strategyManager
    if sm.prepare(isDummy = False, taskType = taskType):
        response = {"filename" : MODEL_FILE_NAME}
    else:
        # report errors if any happened while loading the model file
        response = {"error" : sm.lastError}
    return jsonify(response)


@flask.route('/start', methods = ['POST'])
def postConfig():
    saveInFile(request.data, CONFIG_FILE_NAME)
    sm = start.startFromWeb(CONFIG_FILE_NAME)
    if sm is None:
        abort("Cannot start SpaceScanner optimizations", 500)

    # set the SM
    Server.serverInstance.strategyManager = sm

    # wait for the execution to start
    end = time.time() + 10
    while time.time() < end:
        if sm.getTotalNumJobs() >= 0:
            break

    response = {"status" : "OK", "totalNumJobs" : sm.getTotalNumJobs()}
    return jsonify(response)
