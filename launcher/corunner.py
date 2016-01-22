#!/usr/bin/env python

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
# Copasi optimization run launcher.
#
# The idea in a nutshell: given a Copasi configuration file
# with an optimization task, optimization parameters, and methods,
# determine the minimal subset of parameters that give "good enough" result.
#
# Supports greedy and exhaustive search strategies.
# "Smarter" search strategies are planned as future additions.
#

#
# Author: Atis Elsts, 2016
#

import os, sys, traceback

# local files
from util import *
import g
import webserver
import process
import strategy

################################################

class StatsManager:
    @staticmethod
    def getResourceList(qs):
        reply = {}
        reply["methods"] = g.getConfig("copasi.methods")
        reply["parameters"] = strategy.manager.copasiConfig["params"]
        (active, finished) = strategy.manager.getJobLists()
        reply["activeJobs"] = active
        reply["finishedJobs"] = finished
        return reply

    @staticmethod
    def getResource(qs, resourceName):
        try:
            id = int(resourceName)
        except:
            return {"error" : "invalid resource ID"}
        return strategy.manager.getJobStats(id)

################################################
# Execute the web server (in a separate thread)

def executeWebserver(args):
    try:
        port = int(g.getConfig("web.port"))
        g.log(LOG_INFO, "<corunner>: starting webserver, port: " + str(port))
        server = webserver.InterruptibleHTTPServer(('', port), webserver.HttpServerHandler)
        server.statsManager = StatsManager()
        # report ok and enter the main loop
        g.log(LOG_DEBUG, "<corunner>: webserver started, listening to port {}".format(port))
        server.serve_forever()
    except Exception as e:
        g.log(LOG_ERROR, "<corunner>: exception occurred in webserver:")
        g.log(LOG_ERROR, str(e))
        g.log(LOG_ERROR, traceback.format_exc())
        sys.exit(1)
    sys.exit(0)


################################################
# Execute the application

def main():
    configFileName = DEFAULT_CONFIG_FILE
    if len(sys.argv) > 1:
        configFileName = sys.argv[1]

    g.loadConfig(configFileName)

    if not g.getConfig("copasi.methods"):
        g.log(LOG_ERROR, "cannot execute optimizations: no methods defined in CoRunner configuration file")
        return -1

    # update log file
    with open(g.getConfig("log.file"), "a+") as f:
        f.write("============= ")
        f.write(getCurrentTime())
        f.write("\n")

    # start the web server
    if bool(g.getConfig("web.enable")):
        process.createBackgroundThread(executeWebserver, None)

    # start the selected parameter sweep strategy
    if not strategy.manager.prepare():
        return -1
    strategy.manager.execute()
    if bool(g.getConfig("hangMode")):
        while True:
            time.sleep(1)
    return 0

################################################

if __name__ == '__main__':
    main()
