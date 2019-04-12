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
# Author: Atis Elsts, 2016-2017
#

import os, sys, shutil, copy, json, multiprocessing
import numbers
from util import *

################################################
# Global variables

# configuration settings
config = {}
configFileName = DEFAULT_CONFIG_FILE
spacescannerStartTime = None
workDir = None
taskName = None
logFileName = None
doQuit = False

################################################

class ConfigFileField:
    def __init__(self, default, canBeNone = False):
        self.default = default
        self.canBeNone = canBeNone

    def validate(self, value):
        if value is None and not self.canBeNone:
            return False
        # if list, must be nonempty
        if isinstance(self.default, list) and len(value) == 0:
            return False
        return True

DEFCFG = {}

def defaultConfigInitialize():
    DEFCFG[("copasi", "modelFile")] = ConfigFileField(os.path.join(
        SELF_PATH, "models", "simple-6params.cps"))
    DEFCFG[("copasi", "methods")] = ConfigFileField(["ParticleSwarm", "GeneticAlgorithm", "GeneticAlgorithmSR", "EvolutionaryProgram", "EvolutionaryStrategySR"])
    DEFCFG[("copasi", "fallbackMethods")] = ConfigFileField (["GeneticAlgorithmSR", "EvolutionaryStrategySR"])
    DEFCFG[("copasi", "randomizeMethodSelection")] = ConfigFileField(False)
    DEFCFG[("copasi", "methodParametersFromFile")] = ConfigFileField(False)
    DEFCFG[("copasi", "parameters")] = ConfigFileField([]) # all from copasi file
    # "parameterFitting" is the alternative to "optimization"
    DEFCFG[("copasi", "taskType")] = ConfigFileField("optimization")

    DEFCFG[("optimization", "timeLimitSec")] = ConfigFileField(600)
    DEFCFG[("optimization", "consensusCorridor")] = ConfigFileField(0.01)
    DEFCFG[("optimization", "consensusAbsoluteError")] = ConfigFileField(1e-6)
    DEFCFG[("optimization", "consensusDelaySec")] = ConfigFileField(300)
    DEFCFG[("optimization", "consensusProportionalDelay")] = ConfigFileField(0.15) # 15% of total run's time
    DEFCFG[("optimization", "stagnationDelaySec")] = ConfigFileField(300)
    DEFCFG[("optimization", "stagnationProportionalDelay")] = ConfigFileField(0.15) # 15% of total run's time
    DEFCFG[("optimization", "targetFractionOfTOP")] = ConfigFileField(0.0) # set to 0.0 to disable this
    DEFCFG[("optimization", "bestOfValue")] = ConfigFileField(None)
    DEFCFG[("optimization", "restartFromBestValue")] = ConfigFileField( True) # if yes, each next method will start from the best parameter values so far
    DEFCFG[("optimization", "maxConcurrentRuns")] = ConfigFileField(4)
    DEFCFG[("optimization", "runsPerJob")] = ConfigFileField(2)
    DEFCFG[("optimization", "paramEstimationReferenceValueSec")] = ConfigFileField(3.0)

    DEFCFG[("parameters", )] = ConfigFileField([
        {"type" : "full-set"}, # include all parameters
        {"type" : "exhaustive", "range" : [1, 3]}, # from 1 to 3
        {"type" : "greedy", "range" : [4, 8]}    # from 4 to 8
    ])

    DEFCFG[("web","enable")] = ConfigFileField(True)
    DEFCFG[("web","port")] = ConfigFileField(19000)
    DEFCFG[("web","logxscale")] = ConfigFileField(False)
    DEFCFG[("web","logyscale")] = ConfigFileField(False)

    DEFCFG[("output", "filename")] = ConfigFileField("results.csv")
    DEFCFG[("output", "loglevel")] = ConfigFileField(2)
    DEFCFG[("output", "logfile")] = ConfigFileField(None, True) # default "spacescanner.log" in the results directory
    DEFCFG[("output", "numberOfBestCombinations")] = ConfigFileField( 0)
    DEFCFG[("restartOnFile",)] = ConfigFileField(None, True)
    DEFCFG[("taskName",)] = ConfigFileField(None, True)
    # the rest are undocumented, for testing only
    DEFCFG[("webTestMode",)] = ConfigFileField(False, True)
    DEFCFG[("hangMode",)] = ConfigFileField(False, True)

def defaultConfigGet(path):
    if tuple(path) not in DEFCFG:
        return None, False
    return DEFCFG[tuple(path)].default, True

def defaultConfigValidate(path, value):
    if tuple(path) not in DEFCFG:
        return False
    return DEFCFG[tuple(path)].validate(value)

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
    if ok:
        ok = defaultConfigValidate(path, value)
    if ok:
        return value
    if useHardcodedConfig:
        value, ok = defaultConfigGet(path)
    return value if ok else default

def setConfig(name, value):
    path = name.split(".")
    compartment = config
    # go to the right subdictionary
    for elem in path[:-1]:
        if elem not in compartment:
            # create a new section
            compartment[elem] = {}
        compartment = compartment[elem]
    compartment[path[-1]] = value


def loadConfig(filename, isQuiet = False):
    global config
    global configFileName

    defaultConfigInitialize()

    if filename:
        configFileName = filename

    if not isQuiet:
        print("loading config from file " + configFileName)

    # load configuration
    try:
        with open(configFileName, "r") as f:
            config = json.load(f)
    except Exception as ex:
        config = {} # use default config
        if not isQuiet:
            log(LOG_ERROR, "<spacescanner>: exception occurred while loading configuration file {}: ".format(configFileName))
            log(LOG_ERROR, "  {}".format(ex))
            log(LOG_ERROR, "going to use the default configuration!\n")

    # see if the number of runners is below the number of CPU cores
    numCores = multiprocessing.cpu_count()
    numMaxRuns = int(getConfig("optimization.maxConcurrentRuns", numCores))
    if numMaxRuns > numCores:
        log(LOG_INFO, "warning: reducing the number of maximal concurrent optimizations rune to the number of CPU cores: {}".format(numCores))
        setConfig("optimization.maxConcurrentRuns", numCores)

def getAllConfig():
    cfg = copy.copy(config)
    for k in DEFCFG:
        if len(k) > 1:
            if k[0] not in cfg:
                # add the section
                cfg[k[0]] = {}
            if k[1] not in cfg[k[0]]:
                # use default
                if isinstance(DEFCFG[k].default, list):
                    cfg[k[0]][k[1]] = copy.copy(DEFCFG[k].default)
                else:
                    cfg[k[0]][k[1]] = DEFCFG[k].default
        else:
            if k[0] not in cfg:
                # use default
                if isinstance(DEFCFG[k].default, list):
                    cfg[k[0]] = copy.copy(DEFCFG[k].default)
                else:
                    cfg[k[0]] = DEFCFG[k].default
    return cfg

################################################
# Logging

def log(loglevel, msg):
    if loglevel <= int(getConfig("output.loglevel", 2)):
        msg += "\n"
        sys.stderr.write(msg)
        if logFileName is not None:
            try:
                with open(logFileName, "a+") as f:
                    f.write(msg)
            except Exception as ex:
                print("Got an exception while trying to write to log file: {}".format(ex))

################################################
# Startup

def prepare(configFileName):
    global workDir
    global taskName
    global spacescannerStartTime
    global logFileName

    spacescannerStartTime = getCurrentTime()

    loadConfig(configFileName)

    if not getConfig("copasi.methods"):
        log(LOG_ERROR, "cannot execute optimizations: no methods defined in SpaceScanner configuration file")
        return False

    dirname = os.path.join(SELF_PATH, "results")
    try:
        os.mkdir(dirname)
    except:
        pass

    taskName = getConfig("taskName")
    if not taskName:
        taskName = os.path.splitext(os.path.basename(getConfig("copasi.modelFile")))[0]
    taskName += "-" + spacescannerStartTime

    workDir = os.path.join(dirname, taskName)
    try:
        os.mkdir(workDir)
    except:
        pass

    if getConfig("output.logfile", None):
        logFileName = getConfig("output.logfile")
    else:
        logFileName = os.path.join(workDir, "spacescanner.log")

    # update the log file
    try:
        with open(logFileName, "a+") as f:
            f.write("============= ")
            f.write(spacescannerStartTime)
            f.write("\n")
    except Exception as ex:
        print("Got an exception while preparing log file: {}".format(ex))

    referenceConfig = os.path.join(workDir, "config.json")
    try:
        # copy the used configuration file as a reference
        shutil.copyfile(configFileName, referenceConfig)
    except:
        # the file probably does not exist; print a warning
        log(LOG_INFO, "failed to copy SpaceScanner configuration file from {} to {}".format(
            configFileName, referenceConfig))

    if isCygwin():
        # remove the first part from the path and normalize it to make Copasi happy
        workDir = os.path.normpath(os.path.join(CYGWIN_DIR, workDir[1:]))

    log(LOG_INFO, "<spacescanner>: working directory is " + workDir)
    return True
