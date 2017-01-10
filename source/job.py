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

import os, sys, time, copy, random, math, threading

from util import *
import g
import runner

LOAD_BALANCE_INTERVAL = 10.0 # seconds

################################################
# Job: manages execution of multiple COPASI instances with a single specific set of parameters.
# Schedules the instances as to ensure that each gets approximately the same amount of CPU time.
# May switch over to different optimization methods if the current method fails to reach consensus.

class Job:
    def __init__(self, pool, params, maxCores, areParametersChangeable):
        self.pool = pool
        self.params = params
        self.areParametersChangeable = areParametersChangeable
        self.id = pool.strategy.nextJobID
        pool.strategy.nextJobID += 1
        self.methods = copy.copy(g.getConfig("copasi.methods"))
        assert len(self.methods)
        self.fallbackMethods = copy.copy(g.getConfig("copasi.fallbackMethods"))
        self.currentMethod = None
        self.pastMethods = []
        self.isUsingFallback = False
        self.runners = []
        self.oldRunners = []
        self.runnerGeneration = 0
        self.oldCpuTimes = []
        self.convergenceTime = None
        self.convergenceValue = None
        self.copasiFile = None
        self.workDir = None
        self.startTime = time.time()
        self.lastOfUpdateTime = self.startTime
        self.lastBalanceTime = self.startTime - LOAD_BALANCE_INTERVAL
        # XXX: note that the number of free cores can increase during job's
        # lifetime, but the code will not react to that, keeping maxCores constant
        self.maxCores = maxCores
        self.loadBalanceFactor = float(g.getConfig("optimization.runsPerJob")) / maxCores


    def getFullName(self):
        return "job {} (optimization parameters: ".format(self.id) + " ".join(self.params) + ")"


    def getName(self):
        return "job {}".format(self.id)


    def getMethods(self):
        # in reverse chronological order
        return [self.currentMethod] + self.pastMethods[::-1]


    def execute(self, workDir, copasiFile):
        self.workDir = workDir
        self.copasiFile = copasiFile

        if bool(g.getConfig("optimization.randomizeMethodSelection")):
            self.currentMethod = random.choice(self.methods)
        else:
            self.currentMethod = self.methods[0]

        g.log(LOG_INFO, "starting " + self.getFullName())

        return self.createRunners()


    def createRunners(self):
        # move the current runners, if any, to the array with old runners
        if self.runners:
            self.oldCpuTimes.append(max(r.currentCpuTime for r in self.runners))
            self.oldRunners.extend(self.runners)
            self.runners = []

        # reset other state
        self.convergenceTime = None
        self.lastOfUpdateTime = time.time()

        self.runnerGeneration += 1

        bestParams = None
        if self.oldRunners and bool(g.getConfig("optimization.restartFromBestValue")):
            # get best params
            bestParams = self.getBestParams()

        for id in range(int(g.getConfig("optimization.runsPerJob"))):
            r = runner.Runner(self, id + 1, self.currentMethod, self.runnerGeneration)
            if not r.prepare(self.workDir, self.copasiFile, bestParams):
                g.log(LOG_ERROR, "{}: failed to create a runner".format(r.getName()))
                return False
            self.runners.append(r)

        # note that this may create more processes than the number of free CPU cores!
        for r in self.runners:
            r.execute()

        return True


    def timeDiffExceeded(self, measuredDiff, requiredDiff):
        return measuredDiff > requiredDiff * self.loadBalanceFactor


    def checkReports(self):
        # if no runners are active, quit
        if not any([r.isActive for r in self.runners]):
            if self.convergenceTime is not None:
                minAbsoluteTime = float(g.getConfig("optimization.consensusDelaySec"))
                # XXX: do not check the relative time here
                if self.hasConsensus() and self.timeDiffExceeded(time.time() - self.convergenceTime, minAbsoluteTime):
                    # count COPASI termination as consensus in this case
                    # XXX: note that this does *not* overwrite "time limit exceeded" exit code!
                    for r in self.runners:
                        if r.terminationReason == TERMINATION_REASON_COPASI_FINISHED:
                            r.terminationReason = TERMINATION_REASON_CONSENSUS
            # switch the methods if required
            self.decideTermination()
            return

        if not all([r.isActive for r in self.runners]):
            # some but not all have quit; quit the others with "stagnation"
            # (not technically true, but the best match from the existing codes)
            for r in self.runners:
                if r.isActive and not r.terminationReason:
                    r.terminationReason = TERMINATION_REASON_STAGNATION
            return

        numActiveRunners = 0
        now = time.time()
        cpuTimeLimit = float(g.getConfig("optimization.timeLimitSec"))
        maxCpuTime = 0
        anyUpdated = False
        with runner.reportLock:
            for r in self.runners:
                if r.isActive:
                    numActiveRunners += 1
                    if r.checkReport(hasTerminated = False, now = now):
                        # the runner updated the OF time
                        self.lastOfUpdateTime = now
                        anyUpdated = True
                    maxCpuTime = max(maxCpuTime, r.currentCpuTime)

        if not self.areParametersChangeable:
            # it is simple; as soon as the first value is read, return
            if anyUpdated:
                for r in self.runners:
                    if r.isActive:
                        r.terminationReason = TERMINATION_REASON_CONSENSUS
                return

        consensusReached = self.hasConsensus()

        if all([r.terminationReason for r in self.runners]):
            return

        # use the old CPU time as a basis
        maxCpuTime += sum(self.oldCpuTimes)
        doKillOnTimeLimit = maxCpuTime >= cpuTimeLimit and not consensusReached
        if doKillOnTimeLimit:
            # kill all jobs immediately
            for r in self.runners:
                if r.isActive:
                    r.terminationReason = TERMINATION_REASON_CPU_TIME_LIMIT
                    g.log(LOG_INFO, "terminating {}: CPU time limit exceeded ({} vs. {})".format(
                        r.getName(), maxCpuTime, cpuTimeLimit))
            return

        # check if the runs have reached consensus
        if consensusReached:
            if self.convergenceTime is None:
                g.log(LOG_DEBUG, self.getName() + ": reached consensus, waiting for guard time before termination")
                self.convergenceTime = now
                self.convergenceValue = min([r.ofValue for r in self.runners])

            # if the runners have converged for long enough time, quit
            else:
                timeConverged = time.time() - self.convergenceTime
                minAbsoluteTime = float(g.getConfig("optimization.consensusDelaySec"))
                minRelativeTime = (time.time() - self.startTime) * float(g.getConfig("optimization.consensusProportionalDelay"))
                if self.timeDiffExceeded(timeConverged, minAbsoluteTime) and timeConverged > minRelativeTime:
                    g.log(LOG_INFO, "terminating {}: consensus reached".format(self.getName()))
                    for r in self.runners:
                        if r.isActive:
                            r.terminationReason = TERMINATION_REASON_CONSENSUS
                    self.convergenceTime = now
                    return # do not check other criteria
        else:
            # reset the timer
            self.convergenceTime = None

            # check for stagnation's time limit
            timeStagnated = time.time() - self.lastOfUpdateTime
            maxAbsoluteTime = float(g.getConfig("optimization.stagnationDelaySec"))
            maxRelativeTime = (time.time() - self.startTime) * float(g.getConfig("optimization.stagnationProportionalDelay"))

            # XXX: specialcase for the non-parameters job: quit it quite quickly (in 10 seconds for each method)
            if not self.areParametersChangeable:
                maxAbsoluteTime = 10.0
                maxRelativeTime = 0.0

            if self.timeDiffExceeded(timeStagnated, maxAbsoluteTime) and timeStagnated > maxRelativeTime:
                # stagnation detected
                for r in self.runners:
                    if r.isActive:
                        r.terminationReason = TERMINATION_REASON_STAGNATION
                    g.log(LOG_INFO, "terminating {}: Optimization stagnated (did not produce new results) for {} seconds".format(self.getName(), timeStagnated))
                return

        # We will continue. Check if load balancing needs to be done
        if now - self.lastBalanceTime >= LOAD_BALANCE_INTERVAL:
            self.lastBalanceTime = now
            if numActiveRunners > self.maxCores:
                # not converged yet + too many active; limit some runners
                cpuTimes = [(r.currentCpuTime, r) for r in self.runners if r.isActive]
                cpuTimes.sort()
                # continue first `maxCores` runners, suspend the rest
                resumeRunners = cpuTimes[:self.maxCores]
                suspendRunners = cpuTimes[self.maxCores:]
                for _,j in resumeRunners:
                    j.suspend(False)
                for _,j in suspendRunners:
                    j.suspend(True)
            else:
                for r in self.runners:
                    r.suspend(False)


    # find min and max values and check that they are in 1% range
    def hasConsensus(self):
        epsilonAbs = float(g.getConfig("optimization.consensusAbsoluteError"))
        epsilonRel = float(g.getConfig("optimization.consensusCorridor"))

        if self.convergenceTime is None:
            minV = min([r.ofValue for r in self.runners])
        else:
            minV = self.convergenceValue
        # if this is not the first method, also should use max from the previous
        maxV = self.getBestOfValue()

        # return False if exited without a result
        if math.isinf(minV) or math.isinf(maxV):
            return False

        # returns true if either the absolute difference OR relative difference are small
        if floatEqual(minV, maxV, epsilonAbs):
            return True

        # XXX: avoid division by zero; this means relative convergence will always fail on 0.0
        if maxV == 0.0:
            return False

        return abs(1.0 - minV / maxV) < epsilonRel


    def decideTermination(self):
        continuableReasons = [TERMINATION_REASON_STAGNATION,
                              TERMINATION_REASON_COPASI_FINISHED]
        if not any([r.terminationReason in continuableReasons for r in self.runners]):
            # all terminated with consensus, because asked by the user, or with time limit
            self.pool.finishJob(self)
            return

        # So we have at least one termination with either:
        #  a) the stagnation limit was exceeded, or
        #  b) Copasi stopped without consensus.
        # Actions now:
        #  1) if no solution found: use a fallback method;
        #  2) else switch to the next method;
        #  3) if no more methods are available, quit.

        if self.currentMethod in self.fallbackMethods:
            # remove the already-used method to avoid infinite looping between methods
            self.fallbackMethods.remove(self.currentMethod)

        assert (self.currentMethod in self.methods)
        self.methods.remove(self.currentMethod)

        anyNotFound = any([math.isinf(r.ofValue) for r in self.runners])
        if anyNotFound or self.isUsingFallback:
            if len(self.fallbackMethods) == 0:
                if anyNotFound:
                    g.log(LOG_INFO, "terminating {}: failed to evaluate the objective function".format(self.getName()))
                else:
                    g.log(LOG_INFO, "terminating {}: all fallback methods exhausted without reaching consensus".format(self.getName()))
                self.pool.finishJob(self)
                return

            self.pastMethods.append(self.currentMethod)
            if bool(g.getConfig("optimization.randomizeMethodSelection")):
                self.currentMethod = random.choice(self.fallbackMethods)
            else:
                self.currentMethod = self.fallbackMethods[0]
            # make sure the fallback methods are also in methods
            if self.currentMethod not in self.methods:
                self.methods.append(self.currentMethod)
            g.log(LOG_INFO, "switching {} to a fallback method {}".format(self.getName(), self.currentMethod))
            self.isUsingFallback = True
            # switch to the fallback method
            if not self.createRunners():
                self.pool.finishJob(self)
            return

        if len(self.methods) == 0:
            g.log(LOG_INFO, "terminating {}: all methods exhausted without reaching consensus".format(self.getName()))
            self.pool.finishJob(self)
            return

        # go for the next method
        self.pastMethods.append(self.currentMethod)
        if bool(g.getConfig("optimization.randomizeMethodSelection")):
            self.currentMethod = random.choice(self.methods)
        else:
            self.currentMethod = self.methods[0]

        g.log(LOG_INFO, "switching {} to the next method {}".format(
            self.getName(), self.currentMethod))
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
        isActive = False
        for r in self.runners:
            if r.isActive:
                r.terminationReason = TERMINATION_REASON_PROGRAM_QUITTING
                isActive = True
        return isActive


    def getStatus(self):
        maxCpuTime = 0
        totalCpuTime = 0
        terminationReason = TERMINATION_REASON_MAX
        bestRunner = None
        bestOfValue = MIN_OF_VALUE
        isActive = False

        for r in self.runners:
            if r.isActive:
                isActive = True
            terminationReason = min(terminationReason, r.terminationReason)
            maxCpuTime = max(r.currentCpuTime, maxCpuTime)
            totalCpuTime += r.currentCpuTime
            if bestOfValue < r.ofValue:
                bestOfValue = r.ofValue
                bestRunner = r

        # also account the failed methods
        for r in self.oldRunners:
            totalCpuTime += r.currentCpuTime
            if bestOfValue < r.ofValue:
                bestOfValue = r.ofValue
                bestRunner = r

        bestStats = None
        if bestRunner is not None and bestRunner.getLastStats().isValid:
            bestStats = bestRunner.getLastStats()

        # add the sum of all previosus generations max runners' times
        maxCpuTime += sum(self.oldCpuTimes)

        return (bestOfValue, bestStats, maxCpuTime, totalCpuTime, isActive, terminationReason)


    def dumpResults(self, f, allParams):
        (bestOfValue, bestStats, maxCpuTime, totalCpuTime, _, terminationReason) = self.getStatus()

        # OF value,CPU time,Total CPU time,Job ID,Stop reason
        f.write("{},{},{},{},{},{},{},".format(
            bestOfValue, maxCpuTime, totalCpuTime, self.id, self.currentMethod,
            len(self.params), reasonToStr(terminationReason)))

        # which parameters are included
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


    def unquoteParams(self):
        return [x.strip("'") for x in self.params]


    def getStatsBrief(self):
        (bestOfValue, _, maxCpuTime, totalCpuTime, isActive, terminationReason) = self.getStatus()

        return {
            "id" : self.id,
            "of" : jsonFixInfinity(bestOfValue, 0.0),
            "cpu" : maxCpuTime,
            "totalCpu" : totalCpuTime,
            "active" : isActive,
            "reason" : reasonToStr(terminationReason),
            "methods" : self.getMethods(),
            "parameters" : self.unquoteParams()
        }


    def getStatsFull(self):
        # Note! This does not get the stats from runners already finished
        reply = []
        isActive = False
        for runnerID in range(len(self.runners)):
            runner = self.runners[runnerID]
            cpuTimes = []
            ofValues = []
            if runner.isActive:
                isActive = True

            baselineValue = jsonFixInfinity(self.pool.strategy.topBaseline, 0.0)

            for generation in range(1, self.runnerGeneration + 1):
                stats = runner.getAllStatsForGeneration(generation)
                prevTime = sum(self.oldCpuTimes[:generation - 1])
                isFirstProcessed = False
                for s in stats:
                    t = prevTime + s.cpuTime
                    if not isFirstProcessed:
                        isFirstProcessed = True
                        # insert a dummy item at the time of the first value found
                        cpuTimes.append(t)
                        ofValues.append(baselineValue)
                    cpuTimes.append(t)
                    ofValues.append(jsonFixInfinity(s.ofValue, 0.0))

                if not isFirstProcessed:
                    t = sum(self.oldCpuTimes[:generation])
                    cpuTimes.append(t)
                    ofValues.append(baselineValue)

            # always add the current state
            if len(ofValues):
                # use the last computed OF value
                lastOfValue = ofValues[-1]
            else:
                # use the baseline value
                lastOfValue = baselineValue
            cpuTimes.append(sum(self.oldCpuTimes) + runner.currentCpuTime)
            ofValues.append(lastOfValue)

            reply.append({"id" : runnerID, "values" : ofValues, 
                          "time" : cpuTimes, "active" : runner.isActive})

        (bestOfValue, _, maxCpuTime, totalCpuTime, isActive, terminationReason) = self.getStatus()

        return {"id" : self.id,
                "data" : reply,
                "methods" : self.getMethods(),
                "active" : isActive,
                "reason" : reasonToStr(terminationReason),
                "parameters": self.unquoteParams()}

