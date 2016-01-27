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

import os, sys, time, copy, math, threading

from util import *
import g
import job


#####################################################################
# the hash is unique as long as each job has unique set of parameters
def getParamSetHash(parameters, allParameters):
    paramState = [2**i for i,x in enumerate(allParameters) if x in parameters]
    return sum(paramState)

#####################################################################
# Pool is a group of jobs without mutual dependencies
# which all can be executed simulataneously (but are not required to)
class JobPool:
    def __init__(self, strategy, parameterSets):
        self.strategy = strategy
        self.parameterSets = parameterSets
        self.currentParametersIndex = 0
        self.jobLock = threading.Lock()
        self.activeJobs = []
        self.numUsableCores = max(1, int(g.getConfig("optimization.maxConcurrentRuns")))
        self.numRunnersPerJob = max(1, int(g.getConfig("optimization.runsPerJob")))
        self.maxNumParallelJobs = int(math.ceil(float(self.numUsableCores) / self.numRunnersPerJob))
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

        with self.jobLock:
            numFreeCores = max(1, self.numUsableCores - len(self.activeJobs) * self.numRunnersPerJob)

        # setup a new job
        j = job.Job(self, params, numFreeCores)

        # add it to the list of active jobs
        with self.jobLock:
            self.activeJobs.append(j)

        # execute the job
        if not j.execute(self.strategy.workDir, self.strategy.copasiFile):
            g.log(LOG_DEBUG, "failed to execute {}".format(j.getName()))
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

