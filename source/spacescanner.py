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
# determine the minimal subset of parameters that gives "good enough" result.
#
# Supports greedy and exhaustive search strategies.
# "Smarter" search strategies are planned as future additions.
#

#
# Author: Atis Elsts, 2016-2017
#

import os, sys, traceback

# local files
from util import *
import g
import webserver
import process
import strategy

################################################
# Execute the web server (in a separate thread)

def executeWebserver(strategyManager):
    try:
        port = int(g.getConfig("web.port"))
        g.log(LOG_INFO, "<spacescanner>: starting webserver, port: " + str(port))
        server = webserver.InterruptibleHTTPServer(('', port), webserver.HttpServerHandler)
        server.strategyManager = strategyManager
        # report ok and enter the main loop
        g.log(LOG_DEBUG, "<spacescanner>: webserver started, listening to port {}".format(port))
        server.serve_forever()
    except Exception as e:
        g.log(LOG_ERROR, "<spacescanner>: exception occurred in webserver:")
        g.log(LOG_ERROR, str(e))
        g.log(LOG_ERROR, traceback.format_exc())
        sys.exit(1)
    sys.exit(0)


################################################

def start(configFileName):
    if not g.prepare(configFileName):
        return

    # read COPASI model file etc.
    strategyManager = strategy.StrategyManager()
    if not strategyManager.prepare(isDummy = False):
        return

    # start the web server
    if bool(g.getConfig("web.enable")):
        process.createBackgroundThread(executeWebserver, strategyManager)

    # start the selected parameter sweep strategy
    strategyManager.execute()

################################################

def startFromWeb(configFileName):
    if not g.prepare(configFileName):
        g.log(LOG_ERROR, "Preparing from config file failed: " + configFileName)
        return None

    # read COPASI model file etc.
    strategyManager = strategy.StrategyManager()
    if not strategyManager.prepare(isDummy = False):
        g.log(LOG_ERROR, "Preparing for execution failed")
        return None

    # start the selected parameter sweep strategy asynchronously
    process.createBackgroundThread(lambda s: s.execute(), strategyManager)

    return strategyManager


################################################
# Should replace this with daemonization?

def wait():
    while not g.doQuit:
        time.sleep(1)

################################################
# Execute the application

def main():
    if len(sys.argv) > 1 and sys.argv[1] == "web":
        # web-only mode; load the last saved web config, if present
        g.loadConfig(os.path.join(SELF_PATH, "tmpweb", "config.json"), isQuiet = True)
        # create an empty strategy and wait for input commands
        strategyManager = strategy.StrategyManager()
        strategyManager.prepare(isDummy = True)
        # start the web server
        process.createBackgroundThread(executeWebserver, strategyManager)
        wait()
    else:
        # normal mode
        if not start(sys.argv[1] if len(sys.argv) > 1 else None):
            return -1

        # if "hang" mode is configured, do not quit until Ctrl+C is pressed
        if bool(g.getConfig("hangMode")):
            wait()

    return 0

################################################

if __name__ == '__main__':
    main()
