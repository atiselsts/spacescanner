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

import os, sys, json, multiprocessing
from util import *

################################################
# Global variables

# configuration settings
DEFAULT_CONFIG = {
    "copasi" : {
        "modelFile" : os.path.join(SELF_PATH, "models", "simple-6params.cps"),
        "methods" : ["ParticleSwarm", "GeneticAlgorithm", "GeneticAlgorithmSR", "EvolutionaryProgram", "EvolutionaryStrategySR", "ScatterSearch", "SimulatedAnnealing"],
        "fallbackMethods" : ["GeneticAlgorithmSR", "EvolutionaryStrategySR"],
        "methodsParametersFromFile" : False,
        "parameters": [] # all from copasi file
    },
    "optimization" : {
        "timeLimitSec" : 60,
        "consensusRelativeError" : 0.01,
        "consensusAbsoluteError" : 1e-6,
        "consensusMinDurationSec" : 60,
        "consensusMinProportionalDuration" : 0.15, # 15% of total run's time
        "optimalityRelativeError" : 0.1, # set to None to disable this
        "bestOfValue" : float("-inf"),
        "restartFromBestValue" : True, # if yes, each next method will start from the best parameter values so far
        "maxConcurrentRuns" : 4,
        "runsPerJob" : 2
    },
    "parameters" : [
        {"type" : "all-parameters"}, # include all parameters
        {"type" : "exhaustive", "range" : [1, 3]}, # from 1 to 3
        {"type" : "greedy", "range" : [4, 8]}    # from 4 to 8
    ],
    "web" : {
	"enable" : True,
        "port" : 19000
    },
    "log" : {
        "level" : 2,
        "file" : "corunner.log"
    },
    "results" : {
        "file" : "results.csv",
        "numBest" : 10,
        "numRunsBeforeSaving" : 10
    },
    # the rest are undocumented, for testing only
    "testMode" : False,
    "hangMode" : False
}

config = DEFAULT_CONFIG

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

def loadConfig(configFileName):
    global config

    # load configuration
    try:
        with open(configFileName, "r") as f:
            config = json.load(f)
    except IOError as e:
        config = DEFAULT_CONFIG
        log(LOG_ERROR, "<corunner>: exception occurred while loading configuration file: " + str(e))
        log(LOG_ERROR, "going to use the default configuration!\n")

    # limit the number of runners to the number of CPU cores
    numCores = multiprocessing.cpu_count()
    config["maxConcurrentOptimizations"] = \
        min(numCores, config.get("maxConcurrentOptimizations", numCores))

################################################
# Logging

def log(loglevel, msg):
    if loglevel <= int(getConfig("log.level", 1)):
        msg += "\n"
        sys.stderr.write(msg)
        with open(getConfig("log.file"), "a+") as f:
            f.write(msg)

################################################
# Other variables

corunnerStartTime = None
