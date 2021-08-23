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

import os, sys, time, copy, itertools, random, math
import threading, atexit, tempfile

from util import *
import g
import copasifile
import jobpool


###############################################################
# Parameter selections

PARAM_SEL_ZERO       = 0
PARAM_SEL_FULL_SET   = 1
PARAM_SEL_EXPLICIT   = 2
PARAM_SEL_EXHAUSTIVE = 3
PARAM_SEL_GREEDY     = 4
PARAM_SEL_GREEDY_REVERSE = 5

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

    def areParametersChangeable(self):
        return self.type != PARAM_SEL_ZERO

    def getAllJobHashes(self, alwaysParams, neverParams):
        hashes = set()
        for paramSet in self.getParameterSets(alwaysParams, neverParams):
            for params in paramSet:
                hash = getParamSetHash(params, self.strategy.copasiConfig["params"],
                                       not self.areParametersChangeable())
                hashes.add(hash)
        return hashes

    @staticmethod
    def create(specification, strategy, numAlwaysIncludeParams):
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

        # if always-on parameters are named, adjust the range to always optimize for them
        start += numAlwaysIncludeParams
        end += numAlwaysIncludeParams

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

    def getParameterSets(self, alwaysParams, neverParams):
        # XXX: ignore the "always" and "never" params
        yield [self.allParameters]

    def getNumCombinations(self):
        return 1


class ParamSelectionZero(ParamSelection):
    def __init__(self, strategy):
        super(ParamSelectionZero, self).__init__(PARAM_SEL_ZERO, strategy, 0, 0)

    def getParameterSets(self, alwaysParams, neverParams):
        # return all params; will set the boundary conditions to the start value anyway
        # XXX: ignore the "always" and "never" params
        yield [self.allParameters]

    def getNumCombinations(self):
        return 1


class ParamSelectionExplicit(ParamSelection):
    def __init__(self, strategy):
        super(ParamSelectionExplicit, self).__init__(PARAM_SEL_EXPLICIT, strategy, 0, 0)
        self.explicitParameterSets = []

    def getParameterSets(self, alwaysParams, neverParams):
        # XXX: ignore the "always" and "never" params
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

    def getParameterSets(self, alwaysParams, neverParams):
        # optimize all combinations of k parameters
        step = -1 if self.isReverse else 1
        for k in range(self.start, self.end + step, step):
            # terminate if good enough value already found
            if self.strategy.totalOptimizationPotentialReached(k - 1):
                return
            paramCombinations = []
            for it in itertools.combinations(self.allParameters, k):
                paramSelection = list(it)
                if selectionMatches(paramSelection, alwaysParams, neverParams):
                    paramCombinations.append(paramSelection)
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

    def getParameterSets(self, alwaysParams, neverParams):
        # add one more parameter to the best current parameter combination
        for k in range(self.start, self.end + 1):
            # terminate if good enough value already found
            if self.strategy.totalOptimizationPotentialReached(k - 1):
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
                    paramSelection = copy.copy(bestParams) + [p]
                    if selectionMatches(paramSelection, alwaysParams, neverParams):
                        paramCombinations.append(paramSelection)
            yield paramCombinations

    def getNumCombinations(self):
        r = 0
        for k in range(self.start, self.end + 1):
            r += self.n - k + 1
        return r


class ParamSelectionGreedyReverse(ParamSelection):
    def __init__(self, strategy, start, end):
        super(ParamSelectionGreedyReverse, self).__init__(PARAM_SEL_GREEDY_REVERSE, strategy, start, end)

    def getParameterSets(self, alwaysParams, neverParams):
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
                paramSelection = [x for x in bestParams if x != p]
                if selectionMatches(paramSelection, alwaysParams, neverParams):
                    paramCombinations.append(paramSelection)
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
        self.totalNumJobs = -1

    def prepare(self, isDummy, taskType = None):
        self.jobLock = threading.Lock()
        self.activeJobPool = None
        self.finishedJobs = {}
        self.startedJobs = set()
        self.doQuitFlag = False
        self.isExecutable = False
        self.lastError = ""

        self.updateLockFile(enable=False, isInitialization=True)

        self.lastNumJobsDumped = 0
        # job counter, starting from 0
        self.nextJobID = 0

        self.copasiConfig = {"params" : []}
        self.jobsByBestOfValue = []

        self.topBaseline = None

        # if no task type passed, use the globally configured value
        if taskType is None:
            taskType = g.getConfig("copasi.taskType")

        # check if the configured task type is valid and if it is, store it in `self`
        if taskType not in [COPASI_TASK_OPTIMIZATION, COPASI_TASK_PARAM_ESTIMATION]:
            s = "bogus task type: {}".format(taskType)
            g.log(LOG_ERROR, s)
            return False, s
        self.taskType = taskType

        # try to load the file
        self.copasiFile, error = self.loadCopasiFile()
        if not self.copasiFile:
            if not isDummy:
                self.lastError = error
            return False

        g.log(LOG_DEBUG, "querying COPASI optimization parameters")
        self.copasiConfig["params"] = self.copasiFile.queryParameters()
        if not self.copasiConfig["params"]:
            if not isDummy:
                self.lastError = "failed to get task parameters from the COPASI model"
            return False

        self.jobsByBestOfValue = [[] for _ in range(1 + len(self.copasiConfig["params"]))]
        if not isDummy:
            self.isExecutable = True
        return True

    # Returns true if `a` is better than `b`.
    # For maximization tasks: if a > b
    # For minimization tasks: if a < b
    def isOfValueBetter(self, a, b):
        if self.taskType == COPASI_TASK_OPTIMIZATION:
            return a > b
        return a < b

    def getOfValueSelectionFn(self):
        if self.taskType == COPASI_TASK_OPTIMIZATION:
            return max
        return min

    def isOfValueSortReverse(self):
        if self.taskType == COPASI_TASK_OPTIMIZATION:
            # sort from biggest to smallest
            return True
        # sort from smallest to biggest
        return False

    def getInitialOfValue(self):
        if self.taskType == COPASI_TASK_OPTIMIZATION:
            return MIN_OF_VALUE
        return MAX_OF_VALUE

    def isActive(self):
        with self.jobLock:
            return self.activeJobPool is not None

    def getTotalNumJobs(self):
        return max(max(self.nextJobID - 1, self.totalNumJobs), 0)

    def getTotalNumParams(self):
        if self.copasiConfig is None:
            return 0
        if not self.copasiConfig.get("params"):
            return 0
        return len(self.copasiConfig.get("params"))

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
                self.updateLockFile(enable=False)
        if isUnfinished:
            sys.stderr.write("<spacescanner>: some jobs still running, waiting for cleanup...\n")
            time.sleep(2.0)

    def updateLockFile(self, enable, isInitialization=False):
        myPid = os.getpid()
        filename = "lockfile.{}".format(myPid)
        fullname = os.path.join(SELF_PATH, "results", filename)

        if enable:
            try:
                with open(fullname, "w") as f:
                    pass
            except Exception as ex:
                g.log(LOG_ERROR, "Failed to create lock file {}: {}".format(fullname, ex))
        else:
            try:
                os.remove(fullname)
            except Exception as ex:
                if not isInitialization:
                    g.log(LOG_ERROR, "Failed to remove lock file {}: {}".format(fullname, ex))

        return False

    def dumpResults(self, totalLimit = 0):
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
        # `numberOfBestCombinations` defines how many of the best parameter combinations
        # to include in results for each number of parameters; 0 means unlimited (default: unlimited)
        numberOfBestCombinations = int(g.getConfig("output.numberOfBestCombinations"))

        for joblist in self.jobsByBestOfValue:
            if numberOfBestCombinations:
                lst = joblist[:numberOfBestCombinations]
            else:
                lst = joblist
            for job in lst:
                allJobsByBestOfValue.append(job)
        allJobsByBestOfValue.sort(key=lambda x: x.getBestOfValue(),
                                  reverse=self.isOfValueSortReverse())

        allParams = self.copasiConfig["params"]

        rank = 1
        try:
            with open(filename, "w") as f:
                self.dumpCsvFileHeader(f)
                for job in allJobsByBestOfValue:
                    job.dumpResults(f, rank, allParams)
                    if totalLimit and rank >= totalLimit:
                        break
                    rank += 1
        except Exception as ex:
            g.log(LOG_ERROR, "cannot save results to {}: {}".format(filename, ex))

        g.log(LOG_INFO, '<spacescanner>: results of finished jobs saved in "' + filename + '"')
        return filename


    def dumpCsvFileHeader(self, f):
        evaluationResultName = "OF value" if self.taskType == COPASI_TASK_OPTIMIZATION else "Difference"
        f.write("Rank,")
        f.write(evaluationResultName + ",")
        f.write("Max CPU time,Total CPU time,Job ID,Method,Number of parameters,Stop reason,")
        paramNames = [x.strip("'").strip('"') for x in self.copasiConfig["params"]]
        if False:
            # don't do this anymore: takes too much space?
            f.write(",".join([x + " included" for x in paramNames]) + ",")
        f.write(",".join(paramNames))
        f.write("\n")


    def loadCopasiFile(self):
        copasiFile = copasifile.CopasiFile(self.taskType)
        if not copasiFile.isValid():
            return None, "the COPASI file is not valid"

        filename = g.getConfig("copasi.modelFile")
        filename = filename.replace("@SELF@", SELF_PATH)
        g.log(LOG_INFO, "<spacescanner>: opening COPASI model file {}".format(filename))
        ok, s = copasiFile.read(filename)
        if not ok:
            return None, s
        return copasiFile, "load ok"


    def finishJob(self, job):
        with self.jobLock:
            self.finishedJobs[job.id] = job

            if self.taskType == COPASI_TASK_OPTIMIZATION:
                # optimization; if this is the zero-parameter job, use the result as a baseline
                if not job.areParametersChangeable:
                    self.topBaseline = job.getBestOfValue()
                    g.log(LOG_INFO, "  set baseline={}".format(self.topBaseline))
                    # do no include the result of this job in the "normal" results
                    return
            else:
                # parameter estimation; use the value of the full-parameter job after 3 sec as the baseline
                if job.isFullSet:
                    if job.bestOfValueAfter3Sec is None or math.isinf(job.bestOfValueAfter3Sec):
                        g.log(LOG_INFO, "Cannot set TOP baseline: value at evaluation point is {}, using best value {} instead".format(
                            job.bestOfValueAfter3Sec, job.getBestOfValue()))
                        self.topBaseline = job.getBestOfValue()
                    else:
                        self.topBaseline = job.bestOfValueAfter3Sec

            # order the finished-jobs list by OF values.
            # (full re-sorting is suboptimal, but we do not expect *that* many jobs)
            self.jobsByBestOfValue[len(job.params)].append(job)
            self.jobsByBestOfValue[len(job.params)].sort(
                key=lambda x: x.getBestOfValue(), reverse=self.isOfValueSortReverse())

        # save the intermediate results after each finished job
        self.dumpResults()


    def getNumFinishedJobs(self):
        with self.jobLock:
            return len(self.finishedJobs)

    def isTOPEnabled(self):
        targetFraction = g.getConfig("optimization.targetFractionOfTOP")
        g.log(LOG_INFO, "isTOPEnabled? targetFraction={}".format(targetFraction))
        if targetFraction is None or targetFraction == 0.0:
            # TOP is disabled
            return False
        # TOP is enabled
        return True

    def totalOptimizationPotentialReached(self, numParameters):
        if not self.isTOPEnabled():
            return False

        targetFraction = float(g.getConfig("optimization.targetFractionOfTOP"))
        g.log(LOG_INFO, "top is enabled, targetFraction={}".format(targetFraction))

        # calculate the target value, looking at both config and at the job with all parameters, if any
        try:
            configTargetS = g.getConfig("optimization.bestOfValue")
            if configTargetS is None:
                # this effectively disables it
                configTarget = self.getInitialOfValue()
            else:
                configTarget = float(configTargetS)
        except:
            g.log(LOG_INFO, "Bad bestOfValue in config: {}".format(
                  g.getConfig("optimization.bestOfValue")))
            return False

        g.log(LOG_INFO, "  configTarget={}".format(configTarget))

        # get the joblist describing the execution with "full-set" parameters
        joblist = self.jobsByBestOfValue[-1]
        if joblist:
            calculatedTarget = joblist[0].getBestOfValue()
        else:
            calculatedTarget = self.getInitialOfValue()

        targetValue = calculatedTarget
        if self.isOfValueBetter(configTarget, targetValue):
            # the configured value is better, use it
            targetValue = configTarget

        g.log(LOG_INFO, "  targetValue={}".format(targetValue))

        if targetValue == self.getInitialOfValue():
            g.log(LOG_DEBUG, "TOP: no target value: {} {}".format(configTarget, calculatedTarget))
            return False

        achievedValue = self.getInitialOfValue()
        for joblist in self.jobsByBestOfValue[:numParameters + 1]:
            if joblist:
                joblistOfValue = joblist[0].getBestOfValue()
                if self.isOfValueBetter(joblistOfValue, achievedValue):
                    achievedValue = joblistOfValue

        if self.topBaseline is None:
            g.log(LOG_DEBUG, "TOP: no baseline value: {} {}".format(configTarget, calculatedTarget))
            return False

        isReached = False
        if self.taskType == COPASI_TASK_OPTIMIZATION:
            # Optimization; maximize

            requiredValue = targetValue

            if self.isOfValueBetter(self.topBaseline, targetValue):
                # a corner case: the baseline value is already better than the target!
                isReached = True
            else:
                # the normal case; stop if the current value is close enough to the target
                requiredValue = (targetValue - self.topBaseline) * targetFraction + self.topBaseline
                isReached = achievedValue >= requiredValue

        else:
            # Parameter estimation; minimize

            requiredValue = targetValue

            if self.topBaseline <= targetValue:
                # a corner case: the baseline value is already better than the target
                isReached = achievedValue <= self.topBaseline # is current better than the baseline?
            elif achievedValue > self.topBaseline:
                # corner case: the baseline has not been reached yet
                isReached = False
            else:
                # normal case
                normalizationFactor = self.topBaseline - targetValue # always strictly positive
                # e.g. for target fraction 0.9 the condition 90% of the interval between baseline and target must be covered
                requiredValue = (1.0 - targetFraction) * normalizationFactor + targetValue
                isReached = achievedValue <= requiredValue


        g.log(LOG_DEBUG, "TOP: {} parameters, {} achieved, {} required, {} target, {} configTarget, {} calculatedTarget\n".format(numParameters, achievedValue, requiredValue,
                                                                                                                                targetValue, configTarget, calculatedTarget))


        if isReached:
            g.log(LOG_INFO, "Terminating optimization at {} parameters: good-enough-value criteria reached (required {})".format(numParameters, requiredValue))
            return True
        return False


    def getBestParameters(self, k):
        joblist = self.jobsByBestOfValue[k]
        if not joblist:
            if 0:
                g.log(LOG_ERROR, "Parameter ranges are invalid: best value of {} parameters requested, but no jobs finished".format(k))
                return None
            else:
                # this is fine and expected for preliminary calculations
                return self.copasiConfig["params"][:k]
        return joblist[0].params


    def ioGetAllJobs(self, qs):
        response = {
            "taskType" : self.taskType,
            "baseline" : jsonFixInfinity(self.topBaseline,
                                         getTaskDefaultValue(self.taskType)),
            "stats" : []
        }
        with self.jobLock:
            for id in self.finishedJobs:
                response["stats"].append(self.finishedJobs[id].getStatsBrief())
            if self.activeJobPool:
                with self.activeJobPool.jobLock:
                    for job in self.activeJobPool.activeJobs:
                        if job.areParametersChangeable:
                            response["stats"].append(job.getStatsBrief())
        return response


    def ioGetActiveJobs(self, qs):
        response = {
            "taskType" : self.taskType,
            "baseline" : jsonFixInfinity(self.topBaseline,
                                         getTaskDefaultValue(self.taskType)),
            "stats" : []
        }
        with self.jobLock:
            if bool(g.getConfig("webTestMode")):
                for id in self.finishedJobs:
                    if id < 4:
                        response["stats"].append(self.finishedJobs[id].getStatsFull())
            if self.activeJobPool:
                with self.activeJobPool.jobLock:
                    for job in self.activeJobPool.activeJobs:
                        if job.areParametersChangeable:
                            response["stats"].append(job.getStatsFull())
        return response


    def ioGetJob(self, qs, name):
        try:
            id = int(name)
        except:
            return {"error" : "invalid job ID"}
        job = None
        response = {
            "taskType" : self.taskType,
            "baseline" : jsonFixInfinity(self.topBaseline,
                                         getTaskDefaultValue(self.taskType)),
            "stats" : []
        }
        with self.jobLock:
            if id in self.finishedJobs:
                job = self.finishedJobs[id]
            else:
                if self.activeJobPool is not None:
                    job = self.activeJobPool.findJob(id)
        if job is None:
            return {"error" : "job with ID {} not found".format(id)}

        response["stats"].append(job.getStatsFull())
        return response


    def ioGetConfig(self, qs):
        cfg = g.getAllConfig()
        # XXX hack to avoid infinities in the generated JSON output
        # as jQuery decoding fails to deal with them
        bestOfValue = cfg["optimization"]["bestOfValue"]
        if isinstance(bestOfValue, float) and math.isinf(bestOfValue):
            if "optimization" in cfg:
                cfg["optimization"]["bestOfValue"] = 0.0
        return cfg


    def ioGetResults(self, qs, totalLimit):
        filename = self.dumpResults(totalLimit)
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
                self.updateLockFile(enable=False)
        return {"status" : "OK"}


    def finishActivePool(self):
        with self.jobLock:
            self.activeJobPool = None
            self.updateLockFile(enable=False)
        self.dumpResults()


    def updateErrorMsg(self, pool):
        if pool.errorMsg:
            if self.lastError == "":
                self.lastError = pool.errorMsg
            elif pool.errorMsg != "":
                self.lastError += "\n" + pool.errorMsg
                pool.errorMsg = ""


    def getSpecialParams(self):
        alwaysParams = []
        neverParams = []
        if type(g.getConfig("named_parameters")) is list:
            for spec in g.getConfig("named_parameters"):
                if "name" not in spec or "included" not in spec:
                    g.log(LOG_ERROR, "invalid config file named parameters specification: {}".format(spec))
                    continue
                # convert the names to lower case and strip starting/tailing quotes
                name = spec["name"].strip("'").strip('"').lower()
                if spec["included"] == "never":
                    neverParams.append(name)
                elif spec["included"] == "always":
                    alwaysParams.append(name)
        g.log(LOG_DEBUG, "getSpecialParams: always={} never={}".format(alwaysParams, neverParams))
        return alwaysParams, neverParams


    def execute(self):
        parameterSelections = []

        alwaysParams, neverParams = self.getSpecialParams()
        numAlwaysParams = len(alwaysParams)

        if self.taskType == COPASI_TASK_OPTIMIZATION:
            # always add the zero'th job at start, needed to show baseline in graphs and for TOP
            g.log(LOG_INFO, "optimizing for zero parameters initially to find the baseline")
            spec = {"type" : "zero"}
            parameterSelections.append(ParamSelection.create(spec, self, numAlwaysParams))
            hasZerothJob = True
        else:
            hasZerothJob = False

        if self.isTOPEnabled():
            # add all parameters: will define the target value
            spec = {"type" : "full-set"}
            parameterSelections.append(ParamSelection.create(spec, self, numAlwaysParams))

        if g.getConfig("restartOnFile"):
            # Guess which parameters have not been optimized yet based on the .csv result file
            filename = g.getConfig("restartOnFile").replace("@SELF@", SELF_PATH)
            parameterSets = getNonconvergedResults(filename)
            for ps in parameterSets:
                spec = {"type" : "explicit", "parameters" : ps}
                x = ParamSelection.create(spec, self, numAlwaysParams)
                if x not in parameterSelections:
                    parameterSelections.append(x)

        elif g.getConfig("parameters"):
            # Take the paramter sets from the file
            for spec in g.getConfig("parameters"):
                x = ParamSelection.create(spec, self, numAlwaysParams)
                if x is None:
                    g.log(LOG_ERROR, "invalid parameter specification: {}".format(ENC.encode(spec)))
                    continue
                if x not in parameterSelections:
                    parameterSelections.append(x)

        else:
            # add the default optimization target: all parameters
            g.log(LOG_INFO, "optimizing only for all parameters")
            spec = {"type" : "full-set"}
            parameterSelections.append(ParamSelection.create(spec, self, numAlwaysParams))

        hashes = set()
        for sel in parameterSelections:
            hashes = hashes.union(sel.getAllJobHashes(alwaysParams, neverParams))
        self.totalNumJobs = len(hashes)
        # if the extra "dummy" job0 is scheduled, do not include it in this number
        if hasZerothJob and self.totalNumJobs > 0:
            self.totalNumJobs -= 1
        else:
            # start from job1, not job0 (which is ignored by the web interface)
            self.nextJobID = 1

        g.log(LOG_INFO, "total {} parameter combination(s) to try out, parameters: {}".format(
            self.totalNumJobs, " ".join(self.copasiConfig["params"])))
        g.log(LOG_INFO, "methods enabled: '" + "' '".join(g.getConfig("copasi.methods")) + "'")

        parameterSelections.sort(key = lambda x: x.getSortOrder())
        for sel in parameterSelections:
            g.log(LOG_DEBUG, "processing parameter selection of type {}".format(sel.type))
            for params in sel.getParameterSets(alwaysParams, neverParams):
                g.log(LOG_DEBUG, "made a new pool of {} jobs".format(len(params)))
                pool = jobpool.JobPool(self, params, sel.areParametersChangeable())
                with self.jobLock:
                    self.activeJobPool = pool
                    self.updateLockFile(enable=True)

                pool.start()
                self.updateErrorMsg(pool)

                while True:
                    time.sleep(1.0)
                    if self.doQuitFlag:
                        return True

                    self.updateErrorMsg(pool)

                    try:
                        pool.refresh()
                    except Exception as e:
                        g.log(LOG_INFO, "exception while refreshing active joob pool status, terminating the pool: {}".format(e))
                        self.finishActivePool()
                        break

                    if pool.isDepleted():
                        self.finishActivePool()
                        break               

        return True
