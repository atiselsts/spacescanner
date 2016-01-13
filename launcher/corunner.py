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

import os, sys, time, re, json, copy, itertools, random
import threading, traceback, multiprocessing, shutil, atexit, tempfile

from util import *
import webserver
import copasifile

################################################
# Constants

# paths
DEFAULT_CONFIG_FILE = "config.json"
SELF_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# note that just 64-bit Win and Linux Copasi binaries are included out-of-the-box
if isWindows():
    PLATFORM_DIR = "WIN64"
    COPASI_EXECUTABLE = "CopasiSE.exe"
    if isCygwin():
        CYGWIN_DIR = getCygwinDir()
elif isMac():
    PLATFORM_DIR = "Darwin"
    COPASI_EXECUTABLE = "CopasiSE"
else:
    PLATFORM_DIR = "Linux64"
    COPASI_EXECUTABLE = "CopasiSE"

COPASI_DIR = os.environ.get('COPASIDIR')
if not COPASI_DIR:
    COPASI_DIR = os.path.join(SELF_PATH, "copasi", PLATFORM_DIR)
else:
    COPASI_DIR = os.path.join(COPASI_DIR, "bin")

# configuration settings
DEFAULT_CONFIG = {
    "httpPort" : 19000,
    "copasiModelFile" : os.path.join(SELF_PATH, "models", "simple-6params.cps"),
    "dummyMode" : False,
    "optimizationMaxTimeSec" : 60,
    "optimizationConvergenceEpsilon" : 1e-6,
    "optimizationGuardTimeSec" : 60,
    "optimizationOptimalityProportion" : 0.9,
    "periodicReportIntervalSec" : 1.0,
    "paramSweepExhaustiveMax" : 3,
    "paramSweepGreedyMax" : 8,
    "paramSweepAllFirst" : True,
    "paramSweepExecute" : True,
    "maxConcurrentOptimizations" : 16,
    "methods" : ["ParticleSwarm", "ParticleSwarm"],
    "logLevel" : 2,
    "logFile" : "corunner.log",
    "resultsFile" : "results.csv",
    "numBestResults" : 10,
    "numRunsBeforeSaveResults" : 10
}

# possible reasons why a copasi run was stopped
TERMINATION_REASON_COPASI_FINISHED    = 0
TERMINATION_REASON_CPU_TIME_LIMIT     = 1
TERMINATION_REASON_CONVERGED          = 2
TERMINATION_REASON_GOOD_VALUE_REACHED = 3
TERMINATION_REASON_PROGRAM_QUITTING   = 4

# how often to check if the report file has been modified
MIN_REPORT_CHECK_INTERVAL = 1.0

MIN_OF_VALUE = -1.0 # minimal objective function value

################################################
# Global variables

config = DEFAULT_CONFIG

strategyManager = None


################################################
# Configuration file management

def getConfigSetting(name, default = None, useHardcodedConfig = True):
    if name in config:
        return config[name]
    if useHardcodedConfig:
        return DEFAULT_CONFIG.get(name, default)
    return default

################################################
# Logging

def log(loglevel, msg):
    if loglevel <= int(getConfigSetting("logLevel", 1)):
        msg += "\n"
        sys.stderr.write(msg)
        with open(getConfigSetting("logFile"), "a+") as f:
            f.write(msg)

################################################
# Helper function for executing Copasi binary

def executeCopasi(runner):
    # a pseudo-loop for simpler error handling
    while True:
        if bool(getConfigSetting("dummyMode")):
            time.sleep(1.0)
            runner.ofValue = random.random() * 100
            break

        copasiExe = os.path.join(COPASI_DIR, COPASI_EXECUTABLE)
        if not isExecutable(copasiExe):
            log(LOG_ERROR, 'COPASI binary is not executable or does not exist under "' + copasiExe + '"')
            runner.isError = True
            break

        args = [copasiExe, "--nologo", runner.inputFilename]
        log(LOG_DEBUG, "executing " + " ".join(args))

        runner.isActive = True
        runner.isError = runSubprocess(args, runner)

        # check report in order to update OF value (even if nonzero return value)
        runner.checkReport(hasTerminated = True, now = time.time())

        # exit the loop without an error
        break

    # check termination conditions at the global run level
    runner.isActive = False
    runner.job.checkIfHasTerminated()

def reasonToStr(reason):
    if reason == TERMINATION_REASON_COPASI_FINISHED:
        return "COPASI finished"
    if reason == TERMINATION_REASON_CPU_TIME_LIMIT:
        return "CPU time limit"
    if reason == TERMINATION_REASON_CONVERGED:
        return "Runs converged"
    if reason == TERMINATION_REASON_GOOD_VALUE_REACHED:
        return "Good value reached"
    if reason == TERMINATION_REASON_PROGRAM_QUITTING:
        return "CoRunner interrupted"
    return "?"

################################################
# Runner: manages execution of single COPASI instance
# with specific parameters and with a single specific method.

class Runner:
    def __init__(self, job, methodID):
        self.job = job
        self.methodID = methodID
        self.ofValue = MIN_OF_VALUE
        self.stats = []
        self.isError = False
        self.isActive = False
        self.terminationReason = TERMINATION_REASON_COPASI_FINISHED
        self.lastReportCheckTime = None
        self.lastReportModificationTime = None
        self.startTime = None

    def getFullName(self):
        return self.job.getFullName() + "/{} (method '{}')".format(
            self.methodID + 1, self.job.methods[self.methodID], )

    def getName(self):
        return self.job.getName() + "/{} (method '{}')".format(
            self.methodID + 1, self.job.methods[self.methodID])

    def prepare(self, workDir, copasiFile):
        filename = "job{}_method{}".format(self.job.id, self.methodID)

        # Use separate directory for each run to avoid too many files per directory
        # or at least not hit this issue too early:
        # there are just 65535 max files per directory on FAT32.
        dirname = os.path.join(workDir, "job{}".format(self.job.id))
        try:
            os.mkdir(dirname)
        except:
            pass # may already exist, that's fine

        self.inputFilename = os.path.join(dirname, "input_" + filename + ".cps")
        self.reportFilename = os.path.join(dirname, "output_" + filename + ".log")
        if not copasiFile.createCopy(self.inputFilename, self.reportFilename,
                                     self.job.params, [self.job.methods[self.methodID]]):
            return False

        # clean up the report file
        try:
            os.remove(self.reportFilename)
        except:
            pass # may not exist, that's fine

        return True

    def execute(self):
        self.startTime = time.time()
        t = threading.Thread(target=executeCopasi, args=(self,))
        # keep it in daemon mode, in order to able to kill the app with Ctrl+C
        t.daemon = True
        t.start()
        return True

    def shouldTerminate(self):
        return self.terminationReason != 0

    def getLastStats(self):
        if not self.stats:
            return StatsItem("")
        return self.stats[-1]

    def cleanup(self):
        # XXX: return a bit of memory to the system by deleting old statistics?
        #if self.stats:
        #    self.stats = [self.stats[-1]]
        pass

    def checkReport(self, hasTerminated, now):

        assert self.isActive

        if not hasTerminated:
            if self.lastReportCheckTime is not None \
                 and now - self.lastReportCheckTime < MIN_REPORT_CHECK_INTERVAL:
                # too soon, skip
                return
            if now - self.startTime < 3.0:
                # too soon after start (copasi may not be launched yet), return
                return

        log(LOG_DEBUG, "checking {}".format(self.getName()))
        self.lastReportCheckTime = now

        try:
            st = os.stat(self.reportFilename)
            if self.lastReportModificationTime is None \
                    or st.st_mtime > self.lastReportModificationTime:
                self.lastReportModificationTime = st.st_mtime
                with open(self.reportFilename, "r") as f:
                    inValues = False
                    for line in f:
                        if startsWith(line, "CPU time"):
                            self.stats = []
                            inValues = True
                            continue
                        if not inValues: continue

                        if startsWith(line, "Optimization result"):
                            break

                        si = StatsItem(line)
                        if si.isValid:
                            self.stats.append(si)

                if len(self.stats):
                    self.ofValue = self.getLastStats().ofValue
                    log(LOG_INFO, "{}: new OF value {}".format(self.getName(), self.ofValue))

                    if not hasTerminated:
                        # Check for CPU time end condition
                        maxCpuTime = float(getConfigSetting("optimizationMaxTimeSec"))
                        if self.getLastStats().cpuTime >= maxCpuTime:
                            log(LOG_INFO, "terminating {}: CPU time limit exceeded ({} vs. {})".format(self.getName(), self.stats[-1].cpuTime, maxCpuTime))
                            self.terminationReason = TERMINATION_REASON_CPU_TIME_LIMIT

        except OSError as e:
            log(LOG_ERROR, "accessing report file {} failed: {}".format(
                self.reportFilename, os.strerror(e.errno)))
        except IOError as e:
            log(LOG_ERROR, "parsing report file {} failed: {}".format(
                self.reportFilename, os.strerror(e.errno)))


################################################
# Job: manages execution of COPASI instances with a single specific set of parameters.
# May include multiple methods, creates a runner for each method.

class Job:
    nextJobID = 1

    def __init__(self, params):
        self.id = Job.nextJobID
        Job.nextJobID += 1
        self.params = params
        self.methods = getConfigSetting("methods")
        assert len(self.methods)
        self.runners = []
        self.convergenceTime = None
        self.convergenceValue = None

    def getFullName(self):
        return "job {} (optimization parameters: ".format(self.id) + " ".join(self.params) + ")"

    def getName(self):
        return "job {}".format(self.id)

    def execute(self, workDir, copasiFile):
        log(LOG_INFO, "starting " + self.getFullName())

        for methodIndex in range(len(self.methods)):
            r = Runner(self, methodIndex)
            if not r.prepare(workDir, copasiFile):
                return False
            self.runners.append(r)

        # XXX: this may create more processes than the number of CPU cores!
        for r in self.runners:
            r.execute()

        return True

    def checkReports(self):
        now = time.time()

        for r in self.runners:
            if r.isActive:
                r.checkReport(hasTerminated = False, now = now)

        if all([r.terminationReason for r in self.runners]):
            return

        # check if the runs have converged
        assert len(self.runners)
        if self.convergenceTime is not None:
            ofValue = self.convergenceValue
        else:
            ofValue = self.runners[0].ofValue
        if ofValue == MIN_OF_VALUE:
            isConvergedNow = False
        else:
            epsilon = float(getConfigSetting("optimizationConvergenceEpsilon"))
            isConvergedNow = all([floatEqual(r.ofValue, ofValue, epsilon) for r in self.runners])
        if isConvergedNow:
            log(LOG_DEBUG, self.getName() + ": all methods converged, waiting for guard time before termination")
            if self.convergenceTime is None:
                self.convergenceTime = now
                self.convergenceValue = ofValue

            # if the runners have converged for long enough time, quit
            elif time.time() - self.convergenceTime >= float(getConfigSetting("optimizationGuardTimeSec")):
                log(LOG_INFO, "terminating {}: method convergence criteria reached".format(self.getName()))
                for r in self.runners:
                    if r.isActive:
                        r.terminationReason = TERMINATION_REASON_CONVERGED
                self.convergenceTime = now
                return
        else:
            # reset the timer
            self.convergenceTime = None

        if strategyManager.allParamOptimizationDone and strategyManager.bestOfValue != MIN_OF_VALUE:
            requiredMinOfValue = strategyManager.bestOfValue * float(getConfigSetting("optimizationOptimalityProportion"))
            if self.getBestOfValue() >= requiredMinOfValue:
                log(LOG_INFO, "terminating {}: good-enough-value criteria reached".format(self.getName()))
                for r in self.runners:
                    if r.isActive:
                        r.terminationReason = TERMINATION_REASON_GOOD_VALUE_REACHED
                return

    def checkIfHasTerminated(self):
        # if no runners are active, quit
        if all([not r.isActive for r in self.runners]):
            strategyManager.finishJob(self)
            for r in self.runners:
                r.cleanup()

    def getBestOfValue(self):
        if not self.runners:
            return MIN_OF_VALUE
        return max([r.ofValue for r in self.runners])

    def cleanup(self):
        isUnfinished = False
        for r in self.runners:
            if r.isActive:
                r.terminationReason = TERMINATION_REASON_PROGRAM_QUITTING
                isUnfinished = True
        return isUnfinished

    def dumpResults(self, f):
        cpuTime = 0
        terminationReason = TERMINATION_REASON_PROGRAM_QUITTING
        for r in self.runners:
            s = r.getLastStats()
            if s.isValid:
                cpuTime += s.cpuTime
            # XXX: how much sense does this make?
            terminationReason = min(terminationReason, r.terminationReason)

        # OF value,CPU time,Job ID,Stop reason
        f.write("{},{},{},{},".format(
            self.getBestOfValue(), cpuTime, self.id, reasonToStr(terminationReason)))

        paramState = ['1' if x in self.params else '0' \
                      for x in strategyManager.copasiConfig["params"]]
        f.write(",".join(paramState))
        f.write("\n")

################################################
# Parsing statistics

class StatsItem:
    def __init__(self, line):
        # input example:
        # CPU time [Best Value] [Function Evaluations] [Best Parameters] maximum real part
        # 0.043704 3.24353 1 (	74.248	2.27805	) -1.81914
        self.isValid = True
        self.params = []
        self.cpuTime = 0.0
        self.ofValue = 0.0
        self.numOfEvaluations = 0
        self.maxRealPart = 0.0
        line = line.strip()
        if not line:
            self.isValue = False
            return
        if "\t" in line:
            numbers = line.split("\t")
        else:
            numbers = line.split(" ")
        try:
            self.cpuTime = float(numbers[0])
            self.ofValue = float(numbers[1])
            self.numOfEvaluations = int(numbers[2])
            self.maxRealPart = float(numbers[-1])
            # param value list starts with "(", finishes with ")"
            params = numbers[3].lstrip("(").rstrip(")").strip(" ")
            for n in params.split():
                self.params.append(float(n))
        except ValueError as e:
            log(LOG_DEBUG, "value error {} in line".format(e))
            log(LOG_DEBUG, line)
        except:
            log(LOG_DEBUG, "unexpected error {} in line".format(sys.exc_info()[0]))
            log(LOG_DEBUG, line)
            self.isValid = False

    def __str__(self):
        paramStr = " ".join([str(x) for x in self.params])
        return "{}: {} {} {} ({}) {}".format(self.isValid, self.cpuTime, self.ofValue, self.numOfEvaluations, paramStr, self.maxRealPart)

################################################

class StatsManager:
    @staticmethod
    def getResourceList(qs):
        reply = {}
        reply["methods"] = getConfigSetting("methods")
        reply["parameters"] = strategyManager.copasiConfig["params"]
        (active, finished) = strategyManager.getJobLists()
        reply["activeJobs"] = active
        reply["finishedJobs"] = finished
        return reply

    @staticmethod
    def getResource(qs, resourceName):
        try:
            id = int(resourceName)
        except:
            return {"error" : "invalid resource ID"}

        return strategyManager.getJobStats(id)


################################################
# Execution strategy

class StrategyManager:
    def __init__(self):
        self.workDir = tempfile.mkdtemp()
        if isCygwin():
            self.workDir = os.path.normpath(os.path.join(CYGWIN_DIR, self.workDir[1:]))
        log(LOG_INFO, "<corunner>: working directory is " + self.workDir)
        atexit.register(self.cleanup, self)

        self.jobLock = threading.Lock()

        self.activeJobs = []
        self.finishedJobs = {}
        self.latestJob = None
        numRunnersPerJob = len(getConfigSetting("methods"))
        self.maxNumParallelJobs = max(1, int(getConfigSetting("maxConcurrentOptimizations")) / numRunnersPerJob)

        self.bestOfValue = MIN_OF_VALUE
        self.bestParams = []
        self.allParamOptimizationDone = False
        self.copasiConfig = {"params" : []}
        self.copasiFile = None


    def cleanup(self, args):
        sys.stderr.write("<corunner>: quitting...\n")
        if "params" in self.copasiConfig and self.copasiConfig["params"]:
            with self.jobLock:
                self.dumpResults()
        doWait = False
        time.sleep(0.01)
        with self.jobLock:
            for r in self.activeJobs:
                if r.cleanup():
                    doWait = True
        if doWait:
            time.sleep(1.0)
        shutil.rmtree(self.workDir)


    def dumpResults(self):
        filename = getConfigSetting("resultsFile")

        # order the finished-jobs list by OF values.
        # (full re-sorting is suboptimal, but we do not expect *that* many jobs)
        jobsByBestOfValue = list(self.finishedJobs.values())
        jobsByBestOfValue.sort(key=lambda x: x.getBestOfValue(), reverse=True)

        with open(filename, "w") as f:
            self.dumpCsvFileHeader(f)
            for job in jobsByBestOfValue:
                job.dumpResults(f)
        log(LOG_INFO, '<corunner>: results of finished jobs saved in "' + filename + '"')

        if int(getConfigSetting("numBestResults")) > 0:
            (name, ext) = os.path.splitext(filename)
            bestResultsFilename = name + "-best" + ext
            with open(bestResultsFilename, "w") as f:
                self.dumpCsvFileHeader(f)
                n = 0
                for job in jobsByBestOfValue:
                    job.dumpResults(f)
                    n += 1
                    if n >= int(getConfigSetting("numBestResults")):
                        break
            log(LOG_INFO, '<corunner>: best results additionally saved in "' + bestResultsFilename + '"')


    def dumpCsvFileHeader(self, f):
        f.write("OF value,CPU time,Job ID,Stop reason,")
        f.write(",".join([x.strip("'") for x in self.copasiConfig["params"]]))
        f.write("\n")


    def loadCopasiFile(self):
        result = {"params" : []}
        self.copasiFile = copasifile.CopasiFile()
        filename = getConfigSetting("copasiModelFile")
        filename = filename.replace("@SELF@", SELF_PATH)
        log(LOG_INFO, "<corunner>: opening COPASI model file {}".format(filename))
        if self.copasiFile.read(filename):
            log(LOG_DEBUG, "querying COPASI optimization parameters")
            result["params"] = self.copasiFile.getAllParameters()
        return result


    def numParameterCombinations(self):
        total = 0
        numParams = len(self.copasiConfig["params"])
        if bool(getConfigSetting("paramSweepAllFirst")):
            total += 1
        currentNumParams = 1
        exhaustiveMax = int(getConfigSetting("paramSweepExhaustiveMax"))
        greedyMax = int(getConfigSetting("paramSweepGreedyMax"))
        while currentNumParams <= exhaustiveMax and currentNumParams < numParams:
            total += numCombinations(numParams, currentNumParams)
            currentNumParams += 1
        while currentNumParams <= greedyMax and currentNumParams < numParams:
            total += numParams - currentNumParams + 1
            currentNumParams += 1
        return total


    # This implements a simple sweep strategy:
    # 1) first do an optimization using all parameters;
    # 2) then exhaustive search on all combinations using a few parameters;
    # 3) then continue search using the result of the previous step and greedily
    #    adding parameters one-by-one until no further improvement is detected.
    def nextSetOfParams(self):
        exhaustiveMax = int(getConfigSetting("paramSweepExhaustiveMax"))
        greedyMax = int(getConfigSetting("paramSweepGreedyMax"))

        params = self.copasiConfig["params"]

        if bool(getConfigSetting("paramSweepAllFirst")):
            # optimize all parameters first
            yield params
            # must finish the overall optimization before evaluating any other parameter subset
            while self.getNumJobs():
                self.idle(1.0)

            self.allParamOptimizationDone = True

        currentNumParams = 1
        while currentNumParams <= exhaustiveMax and currentNumParams < len(params):
            # optimize all combinations of k parameters
            for it in itertools.combinations(params, currentNumParams):
                yield it

            # TODO: this will give "all parameters as the best in some cases, which may not be what the user wants.
            # TODO: also, this may be printed before all are finished  (as multiple jobs can be done in parallel)
            log(LOG_INFO, "best set of parameters after trying all combinations of {} parameters: {}".format(currentNumParams, ",".join(self.bestParams)))
            currentNumParams += 1

        if currentNumParams <= greedyMax \
           and currentNumParams < len(params) \
           and exhaustiveMax > 0:
            # let all the current jobs to finish
            # (need this to ensure bestParams have a correct value)
            while self.getNumJobs():
                self.idle(1.0)

        while currentNumParams <= greedyMax and currentNumParams < len(params):
            # add one more parameter to the best combination of the params
            bestParams = copy.copy(self.bestParams)
            for p in params:
                if p not in bestParams:
                    yield bestParams + [p]

            # let all the current jobs to finish (need this for the bestParams check)
            while self.getNumJobs():
                self.idle(1.0)

            # check if actually find better parameters; if not, stop the optimization
            if len(bestParams) == len(self.bestParams):
                log(LOG_INFO, "after trying out {} parameters OF value did not improve, giving".format(currentNumParams))
                break
            log(LOG_INFO, "best set of parameters after trying greedy combinations of {} parameters: {}".format(currentNumParams, ",".join(self.bestParams)))
            currentNumParams += 1

        log(LOG_INFO, "final best set of parameters: {}".format(",".join(self.bestParams)))


    def getNumJobs(self):
        with self.jobLock:
            return len(self.activeJobs)


    def idle(self, idleTime):
        with self.jobLock:
            # copy to avoid prolonged locking
            jobs = copy.copy(self.activeJobs)
        for j in jobs:
            j.checkReports()
        time.sleep(idleTime)


    def finishJob(self, job):
        log(LOG_DEBUG, "finished {}".format(job.getName()))
        with self.jobLock:
            if job not in self.activeJobs:
                return
            self.activeJobs.remove(job)
            if self.bestOfValue < job.getBestOfValue():
                # improved on the OF value! Store the result now.
                self.bestOfValue = job.getBestOfValue()
                self.bestParams = copy.copy(job.params)
            self.finishedJobs[job.id] = job

            numSaveAfter = int(getConfigSetting("numRunsBeforeSaveResults"))
            if len(self.finishedJobs) % numSaveAfter == 0:
                # save intermediate result
                self.dumpResults()

            # check if the latest run should be changed
            if self.latestJob == job:
                if len(self.activeJobs):
                    # XXX: just picks *some* run from the still active ones
                    self.latestJob = self.activeJobs[0]
                else:
                    self.latestJob = None

    def getJobLists(self):
        with self.jobLock:
            active = [x.id for x in self.activeJobs]
        #finished = [x.id for x in self.jobsByBestOfValue]
        finished = self.finishedJobs.keys()
        return (active, finished)


    def getJobStats(self, id):
        job = None
        if id in self.finishedJobs:
            job = self.finishedJobs[id]
        else:
            with self.jobLock:
                for x in self.activeJobs:
                    if x.id == id:
                        job = x; break
        if job is None:
            return {"error" : "job with ID {} not found".format(id)}

        reply = []
        for methodID in range(len(job.runners)):
            runner = job.runners[methodID]
            cpuTimes = []
            ofValues = []
            for s in runner.stats:
                cpuTimes.append(s.cpuTime)
                if math.isnan(s.ofValue) or math.isinf(s.ofValue):
                    ofValues.append(0.0)
                else:
                    ofValues.append(s.ofValue)
            reply.append({"id" : methodID, "values" : ofValues, "time" : cpuTimes})

        return {"data" : reply, "methods" : getConfigSetting("methods")}


    def execute(self):
        self.copasiConfig = self.loadCopasiFile()
        if "params" not in self.copasiConfig or not self.copasiConfig["params"]:
            return

        log(LOG_INFO, "total {} parameter combinations to try out, parameters:".format(self.numParameterCombinations()))
        log(LOG_INFO, "  " + " ".join(self.copasiConfig["params"]))
        log(LOG_INFO, "methods enabled: '" + "' '".join(getConfigSetting("methods")) + "'")

        for params in self.nextSetOfParams():
            # setup a new job
            job = Job(list(params))

            # add it to the list of active jobs
            with self.jobLock:
                self.activeJobs.append(job)
                self.latestJob = job

            # execute the job
            if not job.execute(self.workDir, self.copasiFile):
                self.finishJob(job)

            # while the number is not under the limit, wait for some job to terminate
            while self.getNumJobs() >= self.maxNumParallelJobs:
                self.idle(0.1)


################################################
# Execute the web server (in a separate thread)

def executeWebserver(args):
    try:
        port = int(getConfigSetting("httpPort"))
        log(LOG_INFO, "<corunner>: starting webserver, port: " + str(port))
        server = webserver.InterruptibleHTTPServer(('', port), webserver.HttpServerHandler)
        server.statsManager = StatsManager()
        # report ok and enter the main loop
        log(LOG_DEBUG, "<corunner>: webserver started, listening to port {}".format(port))
        server.serve_forever()
    except Exception as e:
        log(LOG_ERROR, "<corunner>: exception occurred in webserver:")
        log(LOG_ERROR, str(e))
        log(LOG_ERROR, traceback.format_exc())
        sys.exit(1)
    sys.exit(0)


################################################
# Execute the application

def main():
    global config
    global strategyManager

    webserver.log = log
    copasifile.log = log

    configFileName = DEFAULT_CONFIG_FILE
    if len(sys.argv) > 1:
        configFileName = sys.argv[1]

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

    methods = getConfigSetting("methods")
    if not methods:
        log(LOG_ERROR, "cannot execute optimizations: no methods defined in CoRunner configuration file")
        return 0

    # update log file
    with open(getConfigSetting("logFile"), "a+") as f:
        f.write("============= ")
        f.write(getCurrentTime())
        f.write("\n")

    strategyManager = StrategyManager()

    # start the web server
    createBackgroundThread(executeWebserver, None)

    # start the selected parameter sweep strategy
    strategyManager.execute()
    return 0

################################################

if __name__ == '__main__':
    main()
