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

import os, sys, time, copy, random, math

from util import *
import g
import runner

################################################
# Job: manages execution of multiple COPASI instances with a single specific set of parameters.
# Schedules the instances as to ensure that each gets approximately the same amount of CPU time.
# May switch over to different optimization methods if the current method fails to reach consensus.

class Job:
    nextJobID = 1

    def __init__(self, pool, params):
        self.pool = pool
        self.params = params
        self.id = Job.nextJobID
        Job.nextJobID += 1
        self.methods = g.getConfig("copasi.methods")
        assert len(self.methods)
        self.fallbackMethods = copy.copy(g.getConfig("copasi.fallbackMethods"))
        self.methodIndex = 0 # always start from the first method in the list
        self.runners = []
        self.oldRunners = []
        self.convergenceTime = None
        self.convergenceValue = None
        self.copasiFile = None
        self.workDir = None
        self.startTime = time.time()

    def getFullName(self):
        return "job {} (optimization parameters: ".format(self.id) + " ".join(self.params) + ")"

    def getName(self):
        return "job {}".format(self.id)

    def execute(self, workDir, copasiFile):
        self.workDir = workDir
        self.copasiFile = copasiFile

        g.log(LOG_INFO, "starting " + self.getFullName())

        return self.createRunners()

    def createRunners(self):
        self.oldRunners.extend(self.runners)
        self.runners = []

        bestParams = None
        if self.oldRunners and bool(g.getConfig("optimization.restartFromBestValue")):
            # get best params
            bestParams = self.getBestParams()

        for id in range(int(g.getConfig("optimization.runsPerJob"))):
            r = runner.Runner(self, id + 1, self.methods[self.methodIndex])
            if not r.prepare(self.workDir, self.copasiFile, bestParams):
                g.log(LOG_ERROR, "{}: failed to create a runner".format(r.getName()))
                return False
            self.runners.append(r)

        # note that this may create more processes than the number of free CPU cores!
        for r in self.runners:
            r.execute()

        return True

    def checkReports(self):
        if self.checkIfHasTerminated():
            return

        now = time.time()

        for r in self.runners:
            if r.isActive:
                r.checkReport(hasTerminated = False, now = now)

        if all([r.terminationReason for r in self.runners]):
            return

        # check if the runs have reached consensus
        if self.hasConsensus():
            if self.convergenceTime is None:
                g.log(LOG_DEBUG, self.getName() + ": reached consensus, waiting for guard time before termination")
                self.convergenceTime = now
                self.convergenceValue = min([r.ofValue for r in self.runners])

            # if the runners have converged for long enough time, quit
            else:
                timeConverged = time.time() - self.convergenceTime
                minAbsoluteTime = float(g.getConfig("optimization.consensusMinDurationSec"))
                minRelativeTime = (time.time() - self.startTime) * float(g.getConfig("optimization.consensusMinProportionalDuration"))
                if timeConverged >= minAbsoluteTime and timeConverged >= minRelativeTime:
                    g.log(LOG_INFO, "terminating {}: consensus reached".format(self.getName()))
                    for r in self.runners:
                        if r.isActive:
                            r.terminationReason = TERMINATION_REASON_CONSENSUS
                    self.convergenceTime = now
                    return # do not check other criteria
        else:
            # reset the timer
            self.convergenceTime = None

        # take the best value only for jobs with more parameters than this
        totalBestOfValue = self.pool.strategy.getBestOfValue(len(self.params) + 1)
        optimality = g.getConfig("optimization.optimalityRelativeError")
        if totalBestOfValue is not None and optimality is not None:
            proportion = 1.0 - float(optimality)
            if self.getBestOfValue() >= proportion * totalBestOfValue:
                g.log(LOG_INFO, "terminating {}: good-enough-value criteria reached (required {})".format(self.getName(), totalBestOfValue * proportion))
                for r in self.runners:
                    if r.isActive:
                        r.terminationReason = TERMINATION_REASON_GOOD_VALUE_REACHED
                return

    # find min and max values and check that they are in 1% range
    def hasConsensus(self):
        values = [r.ofValue for r in self.runners]

        epsilonAbs = float(g.getConfig("optimization.consensusAbsoluteError"))
        epsilonRel = float(g.getConfig("optimization.consensusRelativeError"))

        minV = min(values) if self.convergenceTime is None else self.convergenceValue
        return Job.isConverged(minV, max(values), epsilonAbs, epsilonRel)

    # returns true if either absolute difference OR relative difference is small
    @staticmethod
    def isConverged(v1, v2, epsilonAbs, epsilonRel):
        if floatEqual(v1, v2, epsilonAbs):
            return True
        if math.isinf(v1) or math.isinf(v2) or v2 == 0.0:
            return False
        return abs(1.0 - v1/v2) < epsilonRel

    def checkIfHasTerminated(self):
        # if no runners are active, quit
        if any([r.isActive for r in self.runners]):
            return False

        self.convergenceTime = None
        if self.hasConsensus():
            # count COPASI termination as consensus in this case
            for r in self.runners:
                if r.terminationReason == TERMINATION_REASON_COPASI_FINISHED:
                    r.terminationReason = TERMINATION_REASON_CONSENSUS
        self.decideTermination()
        return True

    def decideTermination(self):
        badReasons = [TERMINATION_REASON_CPU_TIME_LIMIT, TERMINATION_REASON_COPASI_FINISHED]
        if not any([r.terminationReason in badReasons for r in self.runners]):
            # all terminated fine (with consensus, or because asked by the user)
            self.pool.finishJob(self)
            return

        # ok, we have at least one bad termination
        # (CPU time limit exceeded or Copasi stopped without consensus).
        # 1) if no solution found: use a fallback method
        # 2) else switch to the next method
        # 3) if no more methods are available, quit

        currentMethod = self.methods[self.methodIndex]
        if currentMethod in self.fallbackMethods:
            # remove the already-used method to avoid infinite looping between methods
            self.fallbackMethods.remove(currentMethod)

        if any([math.isinf(r.ofValue) for r in self.runners]):
            if len(self.fallbackMethods) == 0:
                g.log(LOG_INFO, "terminating {}: failed to evaluate the objective function".format(self.getName()))
                self.pool.finishJob(self)
                return

            newMethod = random.choice(self.fallbackMethods)
            # make sure the fallback methods are also in methods
            if newMethod not in self.methods:
                self.methods.append(newMethod)
            self.methodIndex = self.methods.index(newMethod)
            g.log(LOG_INFO, "switching {} to a fallback method {}".format(self.getName(), newMethod))
            # switch to the (single, randomly chosen) fallback method
            if not self.createRunners():
                self.pool.finishJob(self)
            return

        # go for the next method
        self.methodIndex += 1
        if self.methodIndex >= len(self.methods):
            g.log(LOG_INFO, "terminating {}: all methods exhausted without reaching consensus".format(self.getName()))
            self.pool.finishJob(self)
            return

        g.log(LOG_INFO, "switching {} to the next method {}".format(
            self.getName(), self.methods[self.methodIndex]))
        if not self.createRunners():
            self.pool.finishJob(self)
            return

    def getBestOfValue(self):
        value = MIN_OF_VALUE
        if self.oldRunners:
             value = max([r.ofValue for r in self.oldRunners])
        if self.runners:
             value = max(value, max([r.ofValue for r in self.runners]))
        return value

    def getBestParams(self):
        if not self.oldRunners:
            return None
        best = self.oldRunners[0]
        for r in self.oldRunners[1:]:
            if r.ofValue > best.ofValue:
                best = r
        stats = best.getLastStats()
        if not stats.isValid:
            return None
        result = {}
        for i,p in enumerate(self.params):
            result[p] = stats.params[i]
        return result

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

        # also account for CPU time of the failed methods
        for r in self.oldRunners:
            cpuTime += r.currentCpuTime

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
