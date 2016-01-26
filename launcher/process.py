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

import os, psutil, time, threading, signal, sys
from subprocess import Popen, PIPE, STDOUT

class Process:
    POLL_INTERVAL = 1.0 # seconds

    def __init__(self, args, runner):
        self.args = args
        self.runner = runner
        self.process = None
        self.psutilProcess = None

    def run(self):
        #sys.stdout.write("Run subprocess: " + " ".join(self.args) + "\n")
        retcode = -1

        try:
            with open(os.devnull, 'w') as fp:
                self.process = Popen(self.args, stdout = fp, stderr = STDOUT)
                self.psutilProcess = psutil.Process(self.process.pid)
                while self.process.poll() is None:
                    if self.runner.shouldTerminate():
                        self.process.kill()
                    time.sleep(Process.POLL_INTERVAL)
                retcode = self.process.returncode
        except Exception as e:
            print("run subprocess exception:" + str(e))
        except:
            print("unexpected error:", sys.exc_info()[0])
        finally:
            #print("done, retcode = " + str(retcode))
            return retcode

    def getCpuTime(self):
        if self.psutilProcess is None:
            return 0.0
        if "get_cpu_times" in dir(self.psutilProcess):
            user, system = self.psutilProcess.get_cpu_times()
        else:
            user, system = self.psutilProcess.cpu_times()
        return user + system

    def suspend(self, yes):
        if yes:
            self.psutilProcess.suspend()
        else:
            self.psutilProcess.resume()

def createBackgroundThread(function, args):
    # make sure 'args' is a list or a tuple
    if not (type(args) is list or type(args) is tuple):
        args = (args,)
    t = threading.Thread(target=function, args=args)
    # keep it in daemon mode, in order to able to kill the app with Ctrl+C
    t.daemon = True
    t.start() 

#####################################################
class Runner:
    def __init__(self):
        self.doQuit = False
    def shouldTerminate(self):
        return self.doQuit

def test1(p):
    while p.psutilProcess is None:
        time.sleep(1)
    while True:
        t = p.getCpuTime()
        if t > 2.0:
            break
        print("cpu time: {}".format(t))
        time.sleep(0.5)
    print("cpu time limit over, suspend")
    p.suspend(False)
    time.sleep(1)
    print("resume")
    p.suspend(False)
    while True:
        t = p.getCpuTime()
        if t > 4.0:
            break
        print("cpu time: {}".format(t))
        time.sleep(0.5)
    print("cpu time limit over, quit")
    p.runner.doQuit = True

def test():
    print("Suprocess test")
    r = Runner()
    p = Process(["/bin/cat", "/dev/zero"], r)
    createBackgroundThread(test1, p)
    ret = p.run()
    print("return code: {}".format(ret))

if __name__ == "__main__":
    # CPU speed testing: `echo "6^6^3^2" | bc`
    test()
