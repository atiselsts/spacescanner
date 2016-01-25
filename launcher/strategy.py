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

import os, sys, time, copy, itertools, random, math
import threading, shutil, atexit, tempfile

from util import *
import g
import copasifile
import job

# the hash is unique for jobs as each job has an unique set of parameters
def getParamSetHash(parameters, allParameters):
    paramState = [2**i for i,x in enumerate(allParameters) if x in parameters]
    return sum(paramState)

###############################################################
# Pool is a group of jobs without mutual dependencies
# which all can be executed simulataneously (but are not required to)

class JobPool:
    def __init__(self, strategy, parameterSets):
        self.strategy = strategy
        self.parameterSets = parameterSets
        self.currentParametersIndex = 0
        self.jobLock = threading.Lock()
        self.activeJobs = []
        numUsableCores = max(1, int(g.getConfig("optimization.maxConcurrentRuns")))
        numRunnersPerJob = max(1, int(g.getConfig("optimization.runsPerJob")))
        self.maxNumParallelJobs = int(math.ceil(float(numUsableCores) / numRunnersPerJob))
        self.bestOfValue = MIN_OF_VALUE
        self.bestParams = []

    def start(self):
        # try to start n jobs at once
        for _ in range(self.maxNumParallelJobs):
            self.nextJob()

    def nextJob(self):
        if self.currentParametersIndex >= len(self.parameterSets):
            return

        params = self.parameterSets[self.currentParametersIndex]
        self.currentParametersIndex += 1

        # check if a job with parameters has already been around
        hash = getParamSetHash(params, self.strategy.copasiConfig["params"])
        if hash in self.strategy.startedJobs:
            g.log(LOG_DEBUG, "skipping a job, parameter set already processed: {}".format(params))
            return
        self.strategy.startedJobs.add(hash)

        # setup a new job
        j = job.Job(self, params)

        # add it to the list of active jobs
        with self.jobLock:
            self.activeJobs.append(j)

        # execute the job
        if not j.execute(self.strategy.workDir, self.strategy.copasiFile):
            g.log(LOG_DEBUG, "failed to execute {}".format(self.getName()))
            self.finishJob(j)

            # while the number is not under the limit, wait for some job to terminate
#            while self.getNumJobs() >= self.maxNumParallelJobs:
#                self.idle(0.1)


    def finishJob(self, j):
        g.log(LOG_DEBUG, "finished {}".format(j.getName()))
        with self.jobLock:
            if j not in self.activeJobs:
                return
            self.activeJobs.remove(j)
            if self.bestOfValue < j.getBestOfValue():
                # improved on the OF value! Store the result now.
                self.bestOfValue = j.getBestOfValue()
                self.bestParams = copy.copy(j.params)
            self.strategy.finishJob(j)

    def refresh(self):
        with self.jobLock:
            # copy to avoid prolonged locking
            jobs = copy.copy(self.activeJobs)
        for j in jobs:
            j.checkReports()
        with self.jobLock:
            numToRun = self.maxNumParallelJobs - len(self.activeJobs)
        while numToRun > 0:
            numToRun -= 1
            self.nextJob()

    def isDepleted(self):
        with self.jobLock:
            if len(self.activeJobs):
                return False
        return self.currentParametersIndex >= len(self.parameterSets)

    def getJobLists(self):
        with self.jobLock:
            return [x.id for x in self.activeJobs]

    def cleanup(self):
        with self.jobLock:
            for j in self.activeJobs:
                if j.cleanup():
                    doWait = True

    def findJob(self, id):
        for x in self.activeJobs:
            if x.id == id:
                return x
        return None


###############################################################
# Parameter selections

PARAM_SEL_ALL        = 1
PARAM_SEL_EXPLICIT   = 2
PARAM_SEL_EXHAUSTIVE = 3
PARAM_SEL_GREEDY     = 4
PARAM_SEL_GREEDY_REVERSE = 5

class ParamSelection(object):
    def __init__(self, type, strategy, start, end):
        self.type = type
        self.allParameters = strategy.copasiConfig["params"]
        self.n = len(self.allParameters)
        self.strategy = strategy
        self.start = start
        self.end = end
        self.explicitParameters = []
        self.isReverse = start > end
        if self.start >= self.n:
            self.start = self.n - 1
        if self.end >= self.n:
            self.end = self.n - 1

    def getSortOrder(self):
        # first by type, the by lower bound
        return (self.type, self.start)

    @staticmethod
    def create(specification, strategy):
        if "type" not in specification:
            return None

        isReverse = False
        start = 0; end = 0
        if "range" in specification:
            numParams = len(strategy.copasiConfig["params"])
            range = specification["range"]
            start = range[0]
            if len(range) >= 2:
                end = range[1]
            else:
                end = start

            if start < 0: # negative range
                start = numParams - start
            if end < 0:
                end = numParams - end
            if start == 0 or end == 0:
                g.log(LOG_ERROR, "paremeter selection ranges must contain numbers in the range [1 .. n]")
                return None

        if specification["type"] == "all-parameters":
            x = ParamSelectionAll(strategy)
        elif specification["type"] == "explicit":
            x = ParamSelectionExplicit(strategy)
        elif specification["type"] == "exhaustive":
            x = ParamSelectionExhaustive(strategy, start, end)
        elif specification["type"] == "greedy":
            if start > end:
                x = ParamSelectionGreedyReverse(strategy, start, end)
            else:
                x = ParamSelectionGreedy(strategy, start, end)
        else:
            return None

        if "parameters" in specification:
            for p in specification["parameters"]:
                x.explicitParameters.append("'" + p + "'")

        return x


class ParamSelectionAll(ParamSelection):
    def __init__(self, strategy):
        super(ParamSelectionAll, self).__init__(PARAM_SEL_ALL, strategy, 0, 0)

    def getParameterSets(self):
        yield [self.allParameters]

    def getNumCombinations(self):
        return 1


class ParamSelectionExplicit(ParamSelection):
    def __init__(self, strategy):
        super(ParamSelectionExplicit, self).__init__(PARAM_SEL_EXPLICIT, strategy, 0, 0)

    def getParameterSets(self):
        yield [self.explicitParameters]

    def getNumCombinations(self):
        return 1


class ParamSelectionExhaustive(ParamSelection):
    def __init__(self, strategy, start, end):
        super(ParamSelectionExhaustive, self).__init__(PARAM_SEL_EXHAUSTIVE, strategy, start, end)

    def getParameterSets(self):
        # optimize all combinations of k parameters
        step = -1 if self.isReverse else 1
        for k in range(self.start, self.end + step, step):
            paramCombinations = []
            for it in itertools.combinations(self.allParameters, k):
                paramCombinations.append(list(it))
            yield paramCombinations

    def getNumCombinations(self):
        r = 0
        step = -1 if self.isReverse else 1
        for k in range(self.start, self.end + step, step):
            r += numCombinations(self.n, k)
        return r


class ParamSelectionGreedy(ParamSelection):
    def __init__(self, strategy, start, end):
        super(ParamSelectionGreedy, self).__init__(PARAM_SEL_GREEDY, strategy, start, end)

    def getParameterSets(self):
        # add one more parameter to the best current parameter combination
        for k in range(self.start, self.end + 1):
            if k <= 1:
                bestParams = []
            else:
                bestParams = self.strategy.getBestParameters(k - 1)
                if bestParams is None:
                    return # error occured
            paramCombinations = []
            for p in self.allParameters:
                if p not in bestParams:
                    paramCombinations.append(copy.copy(bestParams) + [p])
            yield paramCombinations

    def getNumCombinations(self):
        r = 0
        for k in range(self.start, self.end + 1):
            r += self.n - k + 1
        return r


class ParamSelectionGreedyReverse(ParamSelection):
    def __init__(self, strategy, start, end):
        super(ParamSelectionGreedyReverse, self).__init__(PARAM_SEL_GREEDY_REVERSE, strategy, start, end)

    def getParameterSets(self):
        # remove one more parameter from the best current parameter combination
        for k in range(self.start, self.end - 1, -1):
            if k >= self.n - 1:
                bestParams = self.allParameters
            else:
                bestParams = self.strategy.getBestParameters(k + 1)
                if bestParams is None:
                    return # error occured
            paramCombinations = []
            for p in bestParams:
                paramCombinations.append([x for x in bestParams if x != p])
            yield paramCombinations

    def getNumCombinations(self):
        r = 0
        for k in range(self.start, self.end + 1, -1):
            r += k
        return r


###############################################################
# Execution strategy

class StrategyManager:
    def __init__(self):
        pass
       
    def prepare(self):
        self.workDir = tempfile.mkdtemp()
        if isCygwin():
            self.workDir = os.path.normpath(os.path.join(CYGWIN_DIR, self.workDir[1:]))
        g.log(LOG_INFO, "<corunner>: working directory is " + self.workDir)
        atexit.register(self.cleanup, self)

        self.jobLock = threading.Lock()
        self.activeJobPool = None
        self.finishedJobs = {}
        self.startedJobs = set()

        self.lastNumJobsDumped = 0

        self.copasiConfig = {"params" : []}
        self.copasiFile = None

        self.copasiConfig = self.loadCopasiFile()
        if "params" not in self.copasiConfig or not self.copasiConfig["params"]:
            return False

        self.jobsByBestOfValue = [[] for _ in range(len(self.copasiConfig["params"]))]
        return True


    def cleanup(self, args):
        sys.stderr.write("<corunner>: quitting...\n")
        if "params" in self.copasiConfig and self.copasiConfig["params"]:
            self.dumpResults()
        doWait = False
        time.sleep(0.01)
        with self.jobLock:
            if self.activeJobPool is not None:
                self.activeJobPool.cleanup()
                self.activeJobPool = None
        if doWait:
            time.sleep(1.0)
        shutil.rmtree(self.workDir)


    def dumpResults(self):
        filename = g.getConfig("results.file")
        (name, ext) = os.path.splitext(filename)
        filename = name + "-" + g.corunnerStartTime + ext

        with self.jobLock:
            if len(self.finishedJobs) <= self.lastNumJobsDumped:
                # all finished jobs already were saved, nothing to do
                return
            self.lastNumJobsDumped = len(self.finishedJobs)

        allJobsByBestOfValue = []
        for joblist in self.jobsByBestOfValue:
            for job in joblist:
                allJobsByBestOfValue.append(job)
        allJobsByBestOfValue.sort(key=lambda x: x.getBestOfValue(), reverse=True)

        allParams = self.copasiConfig["params"]

        with open(filename, "w") as f:
            self.dumpCsvFileHeader(f)
            for job in allJobsByBestOfValue:
                job.dumpResults(f, allParams)
        g.log(LOG_INFO, '<corunner>: results of finished jobs saved in "' + filename + '"')

#        if int(g.getConfig("results.numBest")) > 0:
#            (name, ext) = os.path.splitext(filename)
#            bestResultsFilename = name + "-best" + ext
#            with open(bestResultsFilename, "w") as f:
#                self.dumpCsvFileHeader(f)
#                n = 0
#                for job in jobsByBestOfValue:
#                    job.dumpResults(f, allParams)
#                    n += 1
#                    if n >= int(g.getConfig("results.numBest")):
#                        break
#            g.log(LOG_INFO, '<corunner>: best results additionally saved in "' + bestResultsFilename + '"')


    def dumpCsvFileHeader(self, f):
        f.write("OF value,CPU time,Job ID,Stop reason,")
        f.write(",".join([x.strip("'") for x in self.copasiConfig["params"]] * 2))
        f.write("\n")


    def loadCopasiFile(self):
        result = {"params" : []}
        self.copasiFile = copasifile.CopasiFile()
        filename = g.getConfig("copasi.modelFile")
        filename = filename.replace("@SELF@", SELF_PATH)
        g.log(LOG_INFO, "<corunner>: opening COPASI model file {}".format(filename))
        if self.copasiFile.read(filename):
            g.log(LOG_DEBUG, "querying COPASI optimization parameters")
            result["params"] = self.copasiFile.getAllParameters()
        return result


    def finishJob(self, job):
        with self.jobLock:
#            if self.bestOfValue < job.getBestOfValue():
                # improved on the OF value! Store the result now.
#                self.bestOfValue = job.getBestOfValue()
#                self.bestParams = copy.copy(job.params)
            self.finishedJobs[job.id] = job
            numFinishedJobs = len(self.finishedJobs)

            # order the finished-jobs list by OF values.
            # (full re-sorting is suboptimal, but we do not expect *that* many jobs)
            self.jobsByBestOfValue[len(job.params)].append(job)
            self.jobsByBestOfValue[len(job.params)].sort(
                key=lambda x: x.getBestOfValue(), reverse=True)

        numSaveAfter = int(g.getConfig("results.numRunsBeforeSaving"))
        if numFinishedJobs % numSaveAfter == 0:
            # save intermediate result
            self.dumpResults()


    def getBestOfValue(self, minNumParameters):
        configValue = float(g.getConfig("optimization.bestOfValue"))
        calculatedValue = MIN_OF_VALUE
        for joblist in self.jobsByBestOfValue[minNumParameters:]:
            if joblist:
                calculatedValue = max(calculatedValue, joblist[0].getBestOfValue())
        result = max(configValue, calculatedValue)
        if result == MIN_OF_VALUE:
            return None
        return result


    def getBestParameters(self, k):
        joblist = self.jobsByBestOfValue[k]
        if not joblist:
            g.log(LOG_ERROR, "Parameter ranges are invalid: best value of {} parameters requested, but no jobs finished".format(k))
            return None
        return joblist[0].params


    def getJobLists(self):
        with self.jobLock:
            #finished = [x.id for x in self.jobsByBestOfValue]
            finished = self.finishedJobs.keys()
            if self.activeJobPool is None:
                active = []
            else:
                active = self.activeJobPool.getJobLists()
        return (active, finished)


    def getJobStats(self, id):
        job = None
        with self.jobLock:
            if id in self.finishedJobs:
                job = self.finishedJobs[id]
            else:
                if self.activeJobPool is not None:
                    job = self.activeJobPool.findJob(id)
        if job is None:
            return {"error" : "job with ID {} not found".format(id)}

        return job.getStats()


    def finishActivePool(self):
        with self.jobLock:
            self.activeJobPool = None
        self.dumpResults()


    def execute(self):
        parameterSelections = []
        for spec in g.getConfig("parameters"):
            x = ParamSelection.create(spec, self)
            if x is None:
                g.log(LOG_ERROR, "invalid parameter specification: {}".format(ENC.encode(spec)))
                continue
            parameterSelections.append(x)
        parameterSelections.sort(key = lambda x: x.getSortOrder())

        numCombinations = 0
        for sel in parameterSelections:
            numCombinations += sel.getNumCombinations()

        g.log(LOG_INFO, "total {} parameter combination(s) to try out, parameters: {}".format(numCombinations, " ".join(self.copasiConfig["params"])))
        g.log(LOG_INFO, "methods enabled: '" + "' '".join(g.getConfig("copasi.methods")) + "'")

        for sel in parameterSelections:
            for params in sel.getParameterSets():
                g.log(LOG_DEBUG, "made a new pool of {} jobs".format(len(params)))
                pool = JobPool(self, params)
                with self.jobLock:
                    self.activeJobPool = pool

                pool.start()
                while True:
                    time.sleep(1.0)
                    pool.refresh()
                    if pool.isDepleted():
                        self.finishActivePool()
                        break

        return True


####################################
manager = StrategyManager()
