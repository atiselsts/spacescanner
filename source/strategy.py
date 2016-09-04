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
import threading, atexit, tempfile

from util import *
import g
import copasifile
import jobpool


###############################################################
# Parameter selections

PARAM_SEL_FULL_SET   = 1
PARAM_SEL_EXPLICIT   = 2
PARAM_SEL_EXHAUSTIVE = 3
PARAM_SEL_GREEDY     = 4
PARAM_SEL_GREEDY_REVERSE = 5
PARAM_SEL_ZERO       = 6

class ParamSelection(object):
    instanceOfExplicit = None

    def __init__(self, type, strategy, start, end):
        self.type = type
        self.allParameters = strategy.copasiConfig["params"]
        self.n = len(self.allParameters)
        self.strategy = strategy
        self.start = start
        self.end = end
        self.isReverse = start > end
        if self.start > self.n:
            self.start = self.n
        if self.end > self.n:
            self.end = self.n

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
                g.log(LOG_ERROR, "parameter selection ranges must contain numbers in the range [1 .. n]")
                return None

        if specification["type"] == "full-set":
            x = ParamSelectionFullSet(strategy)
        elif specification["type"] == "zero":
            x = ParamSelectionZero(strategy)
        elif specification["type"] == "explicit":
            # use a singleton instance
            if ParamSelection.instanceOfExplicit is None:
                ParamSelection.instanceOfExplicit = ParamSelectionExplicit(strategy)
            x = ParamSelection.instanceOfExplicit
            if specification.get("parameters"):
                names = []
                for p in specification["parameters"]:
                    p = "'" + p + "'"
                    if p not in strategy.copasiConfig["params"]:
                        g.log(LOG_ERROR, "'explicit' parameter range contains nonexistent parameter name {}".format(p))
                        return None
                    names.append(p)
                x.explicitParameterSets.append(names)
            else:
                g.log(LOG_ERROR, "'explicit' parameter range must contain a list of parameter names")
                return None
        elif specification["type"] == "exhaustive":
            x = ParamSelectionExhaustive(strategy, start, end)
        elif specification["type"] == "greedy":
            newstart = min(start, end)
            newend = max(start, end)
            x = ParamSelectionGreedy(strategy, newstart, newend)
        elif specification["type"] == "greedy-reverse":
            newstart = max(start, end)
            newend = min(start, end)
            x = ParamSelectionGreedyReverse(strategy, newstart, newend)
        else:
            return None

        return x


class ParamSelectionFullSet(ParamSelection):
    def __init__(self, strategy):
        super(ParamSelectionFullSet, self).__init__(PARAM_SEL_FULL_SET, strategy, 0, 0)

    def getParameterSets(self):
        yield [self.allParameters]

    def getNumCombinations(self):
        return 1


class ParamSelectionZero(ParamSelection):
    def __init__(self, strategy):
        super(ParamSelectionZero, self).__init__(PARAM_SEL_ZERO, strategy, 0, 0)

    def getParameterSets(self):
        # return all params; will set the boundary conditions to the start value anyway
        yield [self.allParameters]

    def getNumCombinations(self):
        return 1


class ParamSelectionExplicit(ParamSelection):
    def __init__(self, strategy):
        super(ParamSelectionExplicit, self).__init__(PARAM_SEL_EXPLICIT, strategy, 0, 0)
        self.explicitParameterSets = []

    def getParameterSets(self):
        yield self.explicitParameterSets

    def getNumCombinations(self):
        return len(self.explicitParameterSets)

    def __str__(self):
        return "[{" + "}, {".join([str(x) for x in self.explicitParameterSets]) + "}]"

    def __repr__(self):
        return str(self)


class ParamSelectionExhaustive(ParamSelection):
    def __init__(self, strategy, start, end):
        super(ParamSelectionExhaustive, self).__init__(PARAM_SEL_EXHAUSTIVE, strategy, start, end)

    def getParameterSets(self):
        # optimize all combinations of k parameters
        step = -1 if self.isReverse else 1
        paramCombinations = []
        for k in range(self.start, self.end + step, step):
            # terminate if good enough value already found
            if self.strategy.totalOptimizationPotentialReached(k):
                return
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
            # terminate if good enough value already found
            if self.strategy.totalOptimizationPotentialReached(k):
                return
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
        atexit.register(self.cleanup, self)

    def prepare(self, isDummy):
        self.jobLock = threading.Lock()
        self.activeJobPool = None
        self.finishedJobs = {}
        self.startedJobs = set()
        self.doQuitFlag = False
        self.isExecutable = False

        self.lastNumJobsDumped = 0
        # job counter, starting from 1
        self.nextJobID = itertools.count(1)

        self.copasiConfig = {"params" : []}
        self.jobsByBestOfValue = []

        self.topBaseline = 0.0

        self.copasiFile = self.loadCopasiFile()
        if not self.copasiFile:
            return False

        g.log(LOG_DEBUG, "querying COPASI optimization parameters")
        self.copasiConfig["params"] = self.copasiFile.queryParameters()
        if not self.copasiConfig["params"]:
            return False

        self.jobsByBestOfValue = [[] for _ in range(1 + len(self.copasiConfig["params"]))]
        if not isDummy:
            self.isExecutable = True
        return True

    def isActive(self):
        with self.jobLock:
            return self.activeJobPool is not None

    def cleanup(self, args):
        sys.stderr.write("<spacescanner>: quitting...\n")
        self.doQuitFlag = True
        if self.copasiConfig is not None and self.copasiConfig.get("params"):
            self.dumpResults()
        time.sleep(0.01)
        isUnfinished = False
        with self.jobLock:
            if self.activeJobPool is not None:
                isUnfinished = self.activeJobPool.cleanup()
                self.activeJobPool = None
        if isUnfinished:
            sys.stderr.write("<spacescanner>: some jobs still running, waiting for cleanup...\n")
            time.sleep(2.0)


    def dumpResults(self, totalLimit = 0, perParamLimit = 0):
        if g.workDir is None:
            return None
        filename = g.getConfig("output.filename")
        # do not allow put the results in other directories because of security reasons
        if filename != os.path.basename(filename):
            g.log(LOG_INFO, "output file name should not include path, ignoring all but the last element in it")
            filename = os.path.basename(filename)
        (name, ext) = os.path.splitext(filename)
        if not ext:
            ext = ".csv" # default
        filename = os.path.join(g.workDir, "{}-{}{}".format(name, "-", g.taskName, ext))

        with self.jobLock:
            if len(self.finishedJobs) <= self.lastNumJobsDumped:
                # all finished jobs already were saved, nothing to do
                return filename
            self.lastNumJobsDumped = len(self.finishedJobs)

        allJobsByBestOfValue = []
        if perParamLimit == 0:
            numberOfBestCombinations = int(g.getConfig("output.numberOfBestCombinations"))
        else:
            numberOfBestCombinations = perParamLimit
        for joblist in self.jobsByBestOfValue:
            if numberOfBestCombinations:
                lst = joblist[:numberOfBestCombinations]
            else:
                lst = joblist
            for job in lst:
                allJobsByBestOfValue.append(job)
        allJobsByBestOfValue.sort(key=lambda x: x.getBestOfValue(), reverse=True)

        allParams = self.copasiConfig["params"]

        cnt = 0
        with open(filename, "w") as f:
            self.dumpCsvFileHeader(f)
            for job in allJobsByBestOfValue:
                job.dumpResults(f, allParams)
                cnt += 1
                if totalLimit and cnt >= totalLimit:
                    break

        g.log(LOG_INFO, '<spacescanner>: results of finished jobs saved in "' + filename + '"')
        return filename

    def dumpCsvFileHeader(self, f):
        f.write("OF value,CPU time,Job ID,Method,Number of parameters,Stop reason,")
        paramNames = [x.strip("'") for x in self.copasiConfig["params"]]
        f.write(",".join([x + " included" for x in paramNames]))
        f.write("," + ",".join(paramNames))
        f.write("\n")


    def loadCopasiFile(self):
        copasiFile = copasifile.CopasiFile()
        filename = g.getConfig("copasi.modelFile")
        filename = filename.replace("@SELF@", SELF_PATH)
        g.log(LOG_INFO, "<spacescanner>: opening COPASI model file {}".format(filename))
        if not copasiFile.read(filename):
            return None
        return copasiFile


    def finishJob(self, job):
        with self.jobLock:
            self.finishedJobs[job.id] = job

            # if this is a zero-parameter job, use the result as a baseline
            if not job.areParametersChangeable:
                self.topBaseline = job.getBestOfValue()

            # order the finished-jobs list by OF values.
            # (full re-sorting is suboptimal, but we do not expect *that* many jobs)
            self.jobsByBestOfValue[len(job.params)].append(job)
            self.jobsByBestOfValue[len(job.params)].sort(
                key=lambda x: x.getBestOfValue(), reverse=True)

        # save the intermediate results after each finished job
        self.dumpResults()


    def getNumFinishedJobs(self):
        with self.jobLock:
            return len(self.finishedJobs)

    def isTOPEnabled(self):
        optimality = g.getConfig("optimization.optimalityRelativeError")
        if optimality is None or optimality == 0.0:
            # TOP is disabled
            return False
        # TOP is enabled
        return True

    def totalOptimizationPotentialReached(self, numParameters):
        if not self.isTOPEnabled():
            return False

        optimality = g.getConfig("optimization.optimalityRelativeError")

        # calculate the target value, looking at both config and at the job with all parameters, if any
        try:
            configTarget = float(g.getConfig("optimization.bestOfValue"))
        except:
            g.log(LOG_INFO, "Bad bestOfValue in config: {}".format(g.getConfig("optimization.bestOfValue")))
            return False
        joblist = self.jobsByBestOfValue[-1]
        if joblist:
            calculatedTarget = joblist[0].getBestOfValue()
        else:
            calculatedTarget = MIN_OF_VALUE
        targetValue = max(configTarget, calculatedTarget)
        if targetValue == MIN_OF_VALUE:
            return False

        achievedValue = MIN_OF_VALUE
        for joblist in self.jobsByBestOfValue[:numParameters + 1]:
            if joblist:
                achievedValue = max(achievedValue, joblist[0].getBestOfValue())

        proportion = 1.0 - float(optimality)
        isReached = False
        if self.topBaseline > targetValue:
            isReached = True
        else:
            isReached = (achievedValue - self.topBaseline) >= (targetValue - self.topBaseline) * proportion

        if isReached:
            g.log(LOG_INFO, "terminating optimization at {} parameters: good-enough-value criteria reached (required {})".format(numParameters, targetValue * proportion))
            return True
        return False


    def getBestParameters(self, k):
        joblist = self.jobsByBestOfValue[k]
        if not joblist:
            g.log(LOG_ERROR, "Parameter ranges are invalid: best value of {} parameters requested, but no jobs finished".format(k))
            return None
        return joblist[0].params


    def ioGetAllJobs(self, qs):
        response = []
        with self.jobLock:
            for id in self.finishedJobs:
                response.append(self.finishedJobs[id].getStatsBrief())
            if self.activeJobPool:
                with self.activeJobPool.jobLock:
                    for job in self.activeJobPool.activeJobs:
                        response.append(job.getStatsBrief())
        return response


    def ioGetActiveJobs(self, qs):
        response = []
        with self.jobLock:
            if bool(g.getConfig("webTestMode")):
                for id in self.finishedJobs:
                    if id < 4:
                        response.append(self.finishedJobs[id].getStatsFull())
            if self.activeJobPool:
                with self.activeJobPool.jobLock:
                    for job in self.activeJobPool.activeJobs:
                        response.append(job.getStatsFull())
        return response


    def ioGetJob(self, qs, name):
        try:
            id = int(name)
        except:
            return {"error" : "invalid job ID"}
        job = None
        with self.jobLock:
            if id in self.finishedJobs:
                job = self.finishedJobs[id]
            else:
                if self.activeJobPool is not None:
                    job = self.activeJobPool.findJob(id)
        if job is None:
            return {"error" : "job with ID {} not found".format(id)}

        return job.getStatsFull()


    def ioGetConfig(self, qs):
        cfg = g.getAllConfig()
        # XXX hack to avoid infinities in the generated JSON output
        # as jQuery decoding fails to deal with them
        bestOfValue = cfg["optimization"]["bestOfValue"]
        if isinstance(bestOfValue, float) and math.isinf(bestOfValue):
            if "optimization" in cfg:
                cfg["optimization"]["bestOfValue"] = 0.0
        return cfg


    def ioGetResults(self, qs):
        totalLimit = int(qs.get("totallimit", 0))
        perParamLimit = int(qs.get("perparamlimit", 0))
        filename = self.dumpResults(totalLimit, perParamLimit)
        contents = ""
        try: 
            with open(filename) as f:
                contents = f.read()
        except IOError as e:
            g.log(LOG_DEBUG, "failed to read result .csv file {}".format(filename))
        except Exception as e:
            g.log(LOG_INFO, "failed to read result .csv file {}: {}".format(filename, e))

        return contents


    def ioStop(self, qs, name):
        try:
            id = int(name)
        except:
            return {"error" : "invalid job ID"}

        job = None
        with self.jobLock:
            if id in self.finishedJobs:
                job = self.finishedJobs[id]
            else:
                if self.activeJobPool is not None:
                    job = self.activeJobPool.findJob(id)
        if job is None:
            return {"error" : "job with ID {} not found".format(id)}
        job.cleanup()
        return {"status" : "OK"}


    def ioStopAll(self, qs):
        self.doQuitFlag = True
        with self.jobLock:
            if self.activeJobPool is not None:
                self.activeJobPool.cleanup()
                self.activeJobPool = None
        return {"status" : "OK"}


    def finishActivePool(self):
        with self.jobLock:
            self.activeJobPool = None
        self.dumpResults()


    def execute(self):
        parameterSelections = []
        if g.getConfig("restartOnFile"):
            # Guess which parameters have not been optimized yet based on the .csv result file
            filename = g.getConfig("restartOnFile").replace("@SELF@", SELF_PATH)
            parameterSets = getNonconvergedResults(filename)
            for ps in parameterSets:
                spec = {"type" : "explicit", "parameters" : ps}
                x = ParamSelection.create(spec, self)
                if x not in parameterSelections:
                    parameterSelections.append(x)

        elif g.getConfig("parameters"):

            # Deal with TOP, if required
            if self.isTOPEnabled():
                # add the "zero" at the start
                g.log(LOG_INFO, "optimizing for zero parameters initially to find the baseline")
                spec = {"type" : "zero"}
                parameterSelections.append(ParamSelection.create(spec, self))

            # The take the other sets from the file
            for spec in g.getConfig("parameters"):
                x = ParamSelection.create(spec, self)
                if x is None:
                    g.log(LOG_ERROR, "invalid parameter specification: {}".format(ENC.encode(spec)))
                    continue
                if x not in parameterSelections:
                    parameterSelections.append(x)

        else:
            # add the default optimization target: all parameters
            g.log(LOG_INFO, "optimizing only for all parameters")
            spec = {"type" : "full-set"}
            parameterSelections.append(ParamSelection.create(spec, self))

        numCombinations = 0
        for sel in parameterSelections:
            numCombinations += sel.getNumCombinations()

        g.log(LOG_INFO, "total {} parameter combination(s) to try out, parameters: {}".format(numCombinations, " ".join(self.copasiConfig["params"])))
        g.log(LOG_INFO, "methods enabled: '" + "' '".join(g.getConfig("copasi.methods")) + "'")

        parameterSelections.sort(key = lambda x: x.getSortOrder())
        for sel in parameterSelections:
            areParametersChangeable = sel.type != PARAM_SEL_ZERO
            for params in sel.getParameterSets():
                g.log(LOG_DEBUG, "made a new pool of {} jobs".format(len(params)))
                pool = jobpool.JobPool(self, params, areParametersChangeable)
                with self.jobLock:
                    self.activeJobPool = pool

                pool.start()
                while True:
                    time.sleep(1.0)
                    if self.doQuitFlag:
                        return True
                    pool.refresh()
                    if pool.isDepleted():
                        self.finishActivePool()
                        break               

        return True
