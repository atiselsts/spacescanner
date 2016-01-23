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

import os, sys, time, copy, random

from util import *
import g
import runner

################################################
# Job: manages execution of multiple COPASI instances with a single specific set of parameters.
# Schedules the instances as to ensure that each gets approximately the same amount of CPU time.
# May switch over to different optimization methods if the current method fails to converge.

class Job:
    nextJobID = 1

    def __init__(self, pool, params):
        self.pool = pool
        self.params = params
        self.id = Job.nextJobID
        Job.nextJobID += 1
        self.methods = g.getConfig("copasi.methods")
        assert len(self.methods)
        self.methodIndex = 0
        self.runners = []
        self.convergenceTime = None
        self.convergenceValue = None

    def getFullName(self):
        return "job {} (optimization parameters: ".format(self.id) + " ".join(self.params) + ")"

    def getName(self):
        return "job {}".format(self.id)

    def execute(self, workDir, copasiFile):
        g.log(LOG_INFO, "starting " + self.getFullName())

        for id in range(int(g.getConfig("runtime.runsPerJob"))):
            r = runner.Runner(self, id + 1, self.methods[self.methodIndex])
            if not r.prepare(workDir, copasiFile):
                return False
            self.runners.append(r)

        # note that this may create more processes than the number of free CPU cores!
        for r in self.runners:
            r.execute()

        return True

    @staticmethod
    def isConverged(v1, v2, epsilonAbs, epsilonRel):
        if floatEqual(v1, v2, epsilonAbs):
            return True
        if v2 == 0.0:
            return False
        return abs(1.0 - v1/v2) < epsilonRel

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
            epsilonAbs = float(g.getConfig("optimization.consensusAbsoluteError"))
            epsilonRel = float(g.getConfig("optimization.consensusRelativeError"))
            isConvergedNow = all([Job.isConverged(r.ofValue, ofValue, epsilonAbs, epsilonRel) \
                                  for r in self.runners])
        if isConvergedNow:
            g.log(LOG_DEBUG, self.getName() + ": all methods converged, waiting for guard time before termination")
            if self.convergenceTime is None:
                self.convergenceTime = now
                self.convergenceValue = ofValue

            # if the runners have converged for long enough time, quit
            elif time.time() - self.convergenceTime >= float(g.getConfig("optimization.consensusMinDurationSec")):
                g.log(LOG_INFO, "terminating {}: method convergence criteria reached".format(self.getName()))
                for r in self.runners:
                    if r.isActive:
                        r.terminationReason = TERMINATION_REASON_CONVERGED
                self.convergenceTime = now
                return
        else:
            # reset the timer
            self.convergenceTime = None

        totalBestOfValue = self.pool.strategy.getBestOfValue()
        if totalBestOfValue is not None:
            proportion = 1.0 - float(g.getConfig("optimization.optimalityRelativeError"))
            if self.getBestOfValue() >= totalBestOfValue * proportion:
                g.log(LOG_INFO, "terminating {}: good-enough-value criteria reached (required {})".format(self.getName(), totalBestOfValue * proportion))
                for r in self.runners:
                    if r.isActive:
                        r.terminationReason = TERMINATION_REASON_GOOD_VALUE_REACHED
                return

    def checkIfHasTerminated(self):
        # if no runners are active, quit
        if all([not r.isActive for r in self.runners]):
            g.log(LOG_DEBUG, "finished {}".format(self.getName()))
            self.pool.finishJob(self)

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

    def dumpResults(self, f, allParams):
        cpuTime = 0
        terminationReason = TERMINATION_REASON_MAX
        bestRunner = None
        bestOfValue = MIN_OF_VALUE

        for r in self.runners:
            terminationReason = min(terminationReason, r.terminationReason)
            cpuTime += r.currentCpuTime
            if bestOfValue < r.ofValue:
                bestOfValue = r.ofValue
                bestRunner = r

        bestStats = None
        if bestRunner is not None and bestRunner.getLastStats().isValid:
            bestStats = bestRunner.getLastStats()

        # OF value,CPU time,Job ID,Stop reason
        f.write("{},{},{},{},".format(
            bestOfValue, cpuTime, self.id, reasonToStr(terminationReason)))

        # which parameters included
        paramState = ['1' if x in self.params else '0' \
                      for x in allParams]
        f.write(",".join(paramState))

        # included parameter values (use 1.0 for excluded parameters)
        paramValues = [1.0] * len(allParams)
        if bestStats is not None:
            for (index, name) in enumerate(self.params):
                paramValues[allParams.index(name)] = bestStats.params[index]

        f.write("," + ",".join([str(x) for x in paramValues]))

        f.write("\n")


    def getStats(self):
        reply = []
        for methodID in range(len(self.runners)):
            runner = self.runners[methodID]
            cpuTimes = []
            ofValues = []
            for s in runner.stats:
                cpuTimes.append(s.cpuTime)
                if math.isnan(s.ofValue) or math.isinf(s.ofValue):
                    ofValues.append(0.0)
                else:
                    ofValues.append(s.ofValue)
            reply.append({"id" : methodID, "values" : ofValues, "time" : cpuTimes})

        return {"data" : reply, "methods" : self.methods}
