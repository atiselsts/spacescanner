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

import os, sys, shutil, json, multiprocessing
from util import *

################################################
# Global variables

# configuration settings
DEFAULT_CONFIG = {
    "copasi" : {
        "modelFile" : os.path.join(SELF_PATH, "models", "simple-6params.cps"),
        "methods" : ["ParticleSwarm", "GeneticAlgorithm", "GeneticAlgorithmSR", "EvolutionaryProgram", "EvolutionaryStrategySR"],
        "fallbackMethods" : ["GeneticAlgorithmSR", "EvolutionaryStrategySR"],
        "randomizeMethodSelection" : False,
        "methodParametersFromFile" : False,
        "parameters": [] # all from copasi file
    },
    "optimization" : {
        "timeLimitSec" : 600,
        "consensusRelativeError" : 0.01,
        "consensusAbsoluteError" : 1e-6,
        "consensusMinDurationSec" : 300,
        "consensusMinProportionalDuration" : 0.15, # 15% of total run's time
        "optimalityRelativeError" : 0.1, # set to None to disable this
        "bestOfValue" : float("-inf"),
        "restartFromBestValue" : True, # if yes, each next method will start from the best parameter values so far
        "maxConcurrentRuns" : 4,
        "runsPerJob" : 2
    },
    "parameters" : [
        {"type" : "all"}, # include all parameters
        {"type" : "exhaustive", "range" : [1, 3]}, # from 1 to 3
        {"type" : "greedy", "range" : [4, 8]}    # from 4 to 8
    ],
    "web" : {
	"enable" : True,
        "port" : 19000
    },
    "output" : {
        "filename" : "results.csv",
        "loglevel" : 2,
        "logfile" : None, # default "corunner.log" in the results directory
        "numberOfBestCombinations" : 0
    },
    "restartOnFile" : None,
    "taskName" : None,
    # the rest are undocumented, for testing only
    "testMode" : False,
    "hangMode" : False
}

config = DEFAULT_CONFIG
configFileName = DEFAULT_CONFIG_FILE
corunnerStartTime = None
workDir = None
taskName = None
logFileName = None

################################################
# Configuration file management

def get(path, compartment):
    for elem in path[:-1]:
        compartment = compartment.get(elem, None)
        if compartment is None:
            break
    if compartment is not None and path[-1] in compartment:
        return (compartment[path[-1]], True)
    return (None, False)

def getConfig(name, default = None, useHardcodedConfig = True):
    path = name.split(".")
    value, ok = get(path, config)
    if not ok and useHardcodedConfig:
        value, ok = get(path, DEFAULT_CONFIG)
    return value if ok else default

def loadConfig(filename):
    global config
    global configFileName

    if filename:
        configFileName = filename

    print("load config from file " + configFileName)

    # load configuration
    try:
        with open(configFileName, "r") as f:
            config = json.load(f)
    except IOError as e:
        config = DEFAULT_CONFIG
        log(LOG_ERROR, "<corunner>: exception occurred while loading configuration file: " + str(e))
        log(LOG_ERROR, "going to use the default configuration!\n")

    # see if the number of runners is below the number of CPU cores
    numCores = multiprocessing.cpu_count()
    numMaxRuns = int(getConfig("optimization.maxConcurrentRuns", numCores))
    if numMaxRuns > numCores:
        log(LOG_INFO, "warning: reducing the number of maximal concurrent optimizations rune to the number of CPU cores: {}".format(numCores))
        config["optimization"]["maxConcurrentRuns"] = numCores

################################################
# Logging

def log(loglevel, msg):
    if loglevel <= int(getConfig("output.loglevel", 2)):
        msg += "\n"
        sys.stderr.write(msg)
        if logFileName is not None:
            with open(logFileName, "a+") as f:
                f.write(msg)

################################################
# Startup

def prepare(configFileName):
    global workDir
    global taskName
    global corunnerStartTime
    global logFileName

    corunnerStartTime = getCurrentTime()

    loadConfig(configFileName)

    if not getConfig("copasi.methods"):
        log(LOG_ERROR, "cannot execute optimizations: no methods defined in CoRunner configuration file")
        return False

    dirname = os.path.join(SELF_PATH, "results")
    try:
        os.mkdir(dirname)
    except:
        pass

    taskName = getConfig("taskName")
    if not taskName:
        taskName = os.path.splitext(os.path.basename(getConfig("copasi.modelFile")))[0]
    taskName += "-" + corunnerStartTime

    workDir = os.path.join(dirname, taskName)
    try:
        os.mkdir(workDir)
    except:
        pass

    if getConfig("output.logfile", None):
        logFileName = getConfig("output.logfile")
    else:
        logFileName = os.path.join(workDir, "corunner.log")

    # update the log file
    with open(logFileName, "a+") as f:
        f.write("============= ")
        f.write(corunnerStartTime)
        f.write("\n")

    try:
        # copy the used configuration file as a reference
        shutil.copyfile(configFileName, os.path.join(workDir, "config.json"))
    except:
        # the file probably does not exist; print a warning
        log(LOG_INFO, "failed to copy CoRunner configuration file to " + workDir)

    if isCygwin():
        # remove the first part from the path and normalize it to make Copasi happy
        workDir = os.path.normpath(os.path.join(CYGWIN_DIR, workDir[1:]))

    log(LOG_INFO, "<corunner>: working directory is " + workDir)
    return True
