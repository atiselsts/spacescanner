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

###############################################################
# Pool is a group of jobs without mutual dependencies:
# all can be executed simulateneouly (but are not required to)

class JobPool:
    def __init__(self, strategy, parameterSets):
        self.strategy = strategy
        self.parameterSets = parameterSets
        self.currentParametersIndex = 0
        self.jobLock = threading.Lock()
        self.activeJobs = []
        numUsableCores = max(1, int(g.getConfig("runtime.maxConcurrentRuns")))
        numRunnersPerJob = max(1, int(g.getConfig("runtime.runsPerJob")))
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

        self.bestOfValue = MIN_OF_VALUE
        self.bestParams = []
        self.allParamOptimizationDone = False
        self.copasiConfig = {"params" : []}
        self.copasiFile = None

        self.lastNumJobsDumped = 0

        self.copasiConfig = self.loadCopasiFile()
        if "params" not in self.copasiConfig or not self.copasiConfig["params"]:
            return False
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

        # order the finished-jobs list by OF values.
        # (full re-sorting is suboptimal, but we do not expect *that* many jobs)
        with self.jobLock:
            if len(self.finishedJobs) <= self.lastNumJobsDumped:
                # all finished jobs already were saved, nothing to do
                return
            self.lastNumJobsDumped = len(self.finishedJobs)
            jobsByBestOfValue = list(self.finishedJobs.values())
        jobsByBestOfValue.sort(key=lambda x: x.getBestOfValue(), reverse=True)

        allParams = self.copasiConfig["params"]

        with open(filename, "w") as f:
            self.dumpCsvFileHeader(f)
            for job in jobsByBestOfValue:
                job.dumpResults(f, allParams)
        g.log(LOG_INFO, '<corunner>: results of finished jobs saved in "' + filename + '"')

        if int(g.getConfig("results.numBest")) > 0:
            (name, ext) = os.path.splitext(filename)
            bestResultsFilename = name + "-best" + ext
            with open(bestResultsFilename, "w") as f:
                self.dumpCsvFileHeader(f)
                n = 0
                for job in jobsByBestOfValue:
                    job.dumpResults(f, allParams)
                    n += 1
                    if n >= int(g.getConfig("results.numBest")):
                        break
            g.log(LOG_INFO, '<corunner>: best results additionally saved in "' + bestResultsFilename + '"')


    def dumpCsvFileHeader(self, f):
        f.write("OF value,CPU time,Job ID,Stop reason,")
        f.write(",".join([x.strip("'") for x in self.copasiConfig["params"]]))
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



#    def getNumJobs(self):
#        with self.jobLock:
#            return len(self.activeJobs)



#    def idle(self, idleTime):
#        with self.jobLock:
#            # copy to avoid prolonged locking
#            jobs = copy.copy(self.activeJobs)
#        for j in jobs:
#            j.checkReports()
#        time.sleep(idleTime)


    def finishJob(self, job):
        with self.jobLock:
            if self.bestOfValue < job.getBestOfValue():
                # improved on the OF value! Store the result now.
                self.bestOfValue = job.getBestOfValue()
                self.bestParams = copy.copy(job.params)
            self.finishedJobs[job.id] = job
            numFinishedJobs = len(self.finishedJobs)

        numSaveAfter = int(g.getConfig("results.numRunsBeforeSaving"))
        if numFinishedJobs % numSaveAfter == 0:
            # save intermediate result
            self.dumpResults()


    def getBestOfValue(self):
        candidate1 = None
        if self.allParamOptimizationDone and self.bestOfValue != MIN_OF_VALUE:
            candidate1 = self.bestOfValue
        candidate2 = float(g.getConfig("optimization.bestOfValue"))
        if candidate2 == MIN_OF_VALUE:
            candidate2 = None
        if candidate1 is None or candidate2 is None:
            return candidate1 if candidate2 is None else candidate2
        return max(candidate1, candidate2)


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


    def activePoolFinished(self):
        with self.jobLock:
            self.activeJobPool = None
        self.dumpResults()


    def numParameterCombinations(self):
        total = 0
        numParams = len(self.copasiConfig["params"])
        if not bool(g.getConfig("runtime.parameterSweep")):
            return 1
        if bool(g.getConfig("runtime.optimizeWithAllParameters")):
            total += 1
        currentNumParams = 1
        exhaustiveMax = int(g.getConfig("runtime.maxParametersExhaustive"))
        greedyMax = int(g.getConfig("runtime.maxParametersGreedy"))
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
    def nextParameterSets(self):
        exhaustiveMax = int(g.getConfig("runtime.maxParametersExhaustive"))
        greedyMax = int(g.getConfig("runtime.maxParametersGreedy"))

        params = self.copasiConfig["params"]

        if not bool(g.getConfig("runtime.parameterSweep")):
            yield [params]
            return

        if bool(g.getConfig("runtime.optimizeWithAllParameters")):
            # optimize all parameters first
            yield [params]
            # must finish the overall optimization before evaluating any other parameter subset
            self.allParamOptimizationDone = True

        currentNumParams = 1
        while currentNumParams <= exhaustiveMax and currentNumParams < len(params):
            # optimize all combinations of k parameters
            paramSet = []
            for it in itertools.combinations(params, currentNumParams):
                paramSet.append(list(it))
            yield paramSet

            # TODO: this will give "all parameters as the best in some cases, which may not be what the user wants.
            # TODO: also, this may be printed before all are finished (as multiple jobs can be done in parallel)
            g.log(LOG_INFO, "best set of parameters after trying all combinations of {} parameters: {}".format(currentNumParams, ",".join(self.bestParams)))
            currentNumParams += 1

        while currentNumParams <= greedyMax and currentNumParams < len(params):
            # add one more parameter to the best combination of the params
            paramSet = []
            bestParams = copy.copy(self.bestParams)
            for p in params:
                if p not in bestParams:
                    paramSet.append(copy.copy(self.bestParams) + [p])
            yield paramSet

            # check if actually find better parameters; if not, stop the optimization
#            if len(bestParams) == len(self.bestParams):
#                g.log(LOG_INFO, "after trying out {} parameters OF value did not improve, giving".format(currentNumParams))
#                break
            g.log(LOG_INFO, "best set of parameters after trying greedy combinations of {} parameters: {}".format(currentNumParams, ",".join(self.bestParams)))
            currentNumParams += 1

        g.log(LOG_INFO, "final best set of parameters: {}".format(",".join(self.bestParams)))

    def execute(self):
        g.log(LOG_INFO, "total {} parameter combinations to try out, parameters:".format(self.numParameterCombinations()))
        g.log(LOG_INFO, "  " + " ".join(self.copasiConfig["params"]))
        g.log(LOG_INFO, "methods enabled: '" + "' '".join(g.getConfig("copasi.methods")) + "'")

        for params in self.nextParameterSets():
            g.log(LOG_DEBUG, "made a new pool of {} jobs".format(len(params)))
            pool = JobPool(self, params)
            with self.jobLock:
                self.activeJobPool = pool

            pool.start()
            while True:
                time.sleep(1.0)
                pool.refresh()
                if pool.isDepleted():
                    self.activePoolFinished()
                    break

        return True

####################################
manager = StrategyManager()
