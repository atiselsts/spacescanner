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

import os, sys, time, copy, random, threading
import psutil_local as psutil

from util import *
import g
import process

# how often to check if the report file has been modified
MIN_REPORT_CHECK_INTERVAL = 1.0

reportLock = threading.Lock()

################################################
# Helper function for executing Copasi binary

def executeCopasi(runner):
    # a pseudo-loop for simpler error handling
    while True:
        if bool(g.getConfig("webTestMode")):
            if runner.job.id < 4:
                time.sleep(1.0)
                runner.ofValue = random.random() * 100
                runner.isActive = False
            else:
                # wait for the strategy to quit
                while not runner.job.pool.strategy.doQuitFlag:
                    time.sleep(1.0)
                    runner.ofValue += random.random()
                runner.isActive = False
            break

        g.log(LOG_DEBUG, "executing " + " ".join(runner.process.args))
        runner.isError = runner.process.run()

        # check report in order to update OF value (even if nonzero return value)
        with reportLock:
            runner.checkReport(hasTerminated = True, now = time.time())

        # exit the loop without an error
        break

    # check termination conditions at the global run level
    g.log(LOG_DEBUG, "{}: terminated".format(runner.getName()))
    runner.isActive = False
    # disable this; do it from polling in the main thread instead
    #runner.job.checkIfHasTerminated()
    # overwrite the .cps file with best parameter values
    runner.cleanup()

################################################
# Runner: manages execution of single COPASI instance
# with specific parameters and with a single specific method.

class Runner:
    def __init__(self, job, id, methodName):
        self.job = job
        self.id = id
        self.methodName = methodName
        self.ofValue = MIN_OF_VALUE
        self.stats = StatsItem("")
        self.isError = False
        self.isActive = False
        self.isSuspended = False
        self.terminationReason = TERMINATION_REASON_COPASI_FINISHED
        self.lastReportCheckTime = None
        self.lastReportModificationTime = None
        self.startTime = None
        self.process = None
        self.currentCpuTime = 0.0
        self.inputFilename = None
        self.reportFilename = None
        self.copasiFile = None

    def getFullName(self):
        return self.job.getFullName() + "/{} (method '{}')".format(
            self.id, self.methodName)

    def getName(self):
        return self.job.getName() + "/{} (method '{}')".format(
            self.id, self.methodName)

    def prepare(self, workDir, copasiFile, startParamValues):
        filename = "job{}_runner{}".format(self.job.id, self.id)

        # Use separate directory for each run to avoid too many files per directory
        # or at least not hit this issue too early.
        # Note: there are just 65535 max files per directory on FAT32!
        dirname = os.path.join(workDir, "job{}".format(self.job.id))
        try:
            os.mkdir(dirname)
        except:
            pass # may already exist, that's fine

        self.inputFilename = os.path.join(dirname, "input_" + filename + ".cps")
        self.reportFilename = os.path.join(dirname, "output_" + filename + ".log")
        self.copasiFile = copasiFile
        if not copasiFile.createCopy(self.inputFilename, self.reportFilename,
                                     self.job.params, [self.methodName], startParamValues):
            return False

        # clean up the report file
        try:
            os.remove(self.reportFilename)
        except:
            pass # may not exist, that's fine

        copasiExe = os.path.join(COPASI_DIR, COPASI_EXECUTABLE)
        if not isExecutable(copasiExe):
            g.log(LOG_ERROR, 'COPASI binary is not executable or does not exist under "' + copasiExe + '"')
            return False

        args = [copasiExe, "--nologo", self.inputFilename]
        self.process = process.Process(args, self)
        return True

    def execute(self):
        self.startTime = time.time()
        t = threading.Thread(target=executeCopasi, args=(self,))
        # keep it in daemon mode, in order to able to kill the app with Ctrl+C
        t.daemon = True
        self.isActive = True
        t.start()
        # wait to exec to be completed: otherwise Popen() in Python 2.7 can lock up
        time.sleep(0.0)
        while self.isActive and self.process.process is None:
            time.sleep(0.1)
        return True

    def shouldTerminate(self):
        return self.terminationReason != 0

    def getLastStats(self):
        return self.stats

    def suspend(self, yes):
        if yes != self.isSuspended:
            self.isSuspended = yes
            self.process.suspend(yes)

    def getAllStats(self):
        result = []

        if bool(g.getConfig("webTestMode")):
            r = 0.0
            t = 0.0
            random.seed(0)
            for i in range(20):
                r += random.random()
                t += random.random()
                si = StatsItem("{} {} 1 ( 74.24 ) -1.81914".format(r, t))
                result.append(si)
            return result

        try:
            with open(self.reportFilename, "r") as f:
                inValues = False
                for line in f:
                    if startsWith(line, "CPU time"):
                        inValues = True
                        continue
                    if not inValues: continue

                    if startsWith(line, "Optimization Result"):
                        break

                    si = StatsItem(line)
                    if si.isValid:
                        result.append(si)

        except IOError as e:
            g.log(LOG_DEBUG, "failed to read a report file " + self.reportFilename)

        return result

    def cleanup(self):
        stats = self.getLastStats()
        if stats.isValid:
            # overwrite the input file with parameter values corresponding to the best result so far
            paramsDict = dict(zip(self.job.params, stats.params))
            self.copasiFile.createCopy(self.inputFilename, self.reportFilename,
                                       self.job.params, [self.methodName],
                                       paramsDict)

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

        self.lastReportCheckTime = now

        try:
            st = os.stat(self.reportFilename)
            if self.lastReportModificationTime is None \
                    or st.st_mtime > self.lastReportModificationTime:
                self.lastReportModificationTime = st.st_mtime
                with open(self.reportFilename, "r") as f:
                    self.stats.isValid = False
                    inValues = False
                    for line in f:
                        if startsWith(line, "CPU time"):
                            inValues = True
                            continue
                        if not inValues: continue

                        if startsWith(line, "Optimization Result"):
                            break

                        si = StatsItem(line)
                        if si.isValid:
                            self.stats = si

                if self.stats.isValid:
                    self.ofValue = self.getLastStats().ofValue
                    g.log(LOG_INFO, "{}: new OF value {}".format(self.getName(), self.ofValue))

                    # Check for CPU time end condition using the report file
                    self.currentCpuTime = self.getLastStats().cpuTime
            else:
                # no report file update; check for CPU time end condition using OS measurements
                if not hasTerminated:
                    try:
                        self.currentCpuTime = self.process.getCpuTime()
                    except psutil.NoSuchProcess:
                        pass # has already quit

        except OSError as e:
            g.log(LOG_ERROR, "accessing report file {} failed: {}".format(
                self.reportFilename, os.strerror(e.errno)))
        except IOError as e:
            g.log(LOG_ERROR, "parsing report file {} failed: {}".format(
                self.reportFilename, os.strerror(e.errno)))

        if not hasTerminated and not self.terminationReason:
            g.log(LOG_DEBUG, "checked {}, CPU time: {}".format(self.getName(), self.currentCpuTime))
            # XXX: hardcoded "slow" method names
            if self.methodName not in ["ScatterSearch", "SimulatedAnnealing"]:
                # XXX: reuse consensus time for this
                maxTimeWithNoValue = float(g.getConfig("optimization.consensusMinDurationSec")) + 10.0
                if self.job.timeDiffExceeded(now - self.startTime, maxTimeWithNoValue) and \
                   (not self.stats.isValid or self.ofValue == MIN_OF_VALUE):
                    g.log(LOG_DEBUG, "terminating {}: no value found in CPU time: {}".format(self.getName(), self.currentCpuTime))
                    self.terminationReason = TERMINATION_REASON_CPU_TIME_LIMIT


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
        self.ofValue = MIN_OF_VALUE
        self.numOfEvaluations = 0
        self.maxRealPart = 0.0
        line = line.strip()
        if not line:
            self.isValid = False
            return
        if "\t" in line:
            numbers = line.split("\t")
        else:
            numbers = line.split(" ")
        try:
            self.cpuTime = float(numbers[0])
            self.ofValue = float(numbers[1])
            # check for NaN and +inf, but allow -inf, as it's
            # sometimes returned as the "no solution found" value
            if math.isnan(self.ofValue) or \
                   (math.isinf(self.ofValue) and self.ofValue > 0.0):
                # XXX: something went wrong, what's the best action?
                g.log(LOG_ERROR, "invalid objective function value {}, using -infinity instead".format(self.ofValue))
                self.ofValue = MIN_OF_VALUE
            self.numOfEvaluations = int(numbers[2])
            self.maxRealPart = float(numbers[-1])
            # param value list starts with "(", finishes with ")"
            for i in range(4, len(numbers) - 2):
                self.params.append(float(numbers[i]))
        except ValueError as e:
            g.log(LOG_DEBUG, "value error {} in line".format(e))
            g.log(LOG_DEBUG, line)
        except:
            g.log(LOG_DEBUG, "unexpected error {} in line".format(sys.exc_info()[0]))
            g.log(LOG_DEBUG, line)
            self.isValid = False

    def __str__(self):
        paramStr = " ".join([str(x) for x in self.params])
        return "{}: {} {} {} ({}) {}".format(self.isValid, self.cpuTime, self.ofValue, self.numOfEvaluations, paramStr, self.maxRealPart)
