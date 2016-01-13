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

import os, sys, time, threading, re, datetime, math, signal, platform
from subprocess import Popen, PIPE, STDOUT

CORUNNER_VERSION = "0.0.1 (10 Jan 2016) (http://biosystems.lv)"

LOG_FATAL = 0
LOG_ERROR = 1
LOG_INFO  = 2
LOG_DEBUG = 3

def isPython3():
    return sys.version_info[0] >= 3

# reliably returns true even if running under Cygwin
def isWindows():
    sysname = platform.system().lower()
    return "windows" in sysname or "cygwin" in sysname

def isMac():
    return "darwin" in platform.system().lower()

def isCygwin():
    return "cygwin" in platform.system().lower()

def getCygwinDir():
    try:
        import winreg
        CYGWIN_KEY = "SOFTWARE\\Cygwin\\setup"
        hk_user = winreg.HKEY_CURRENT_USER
        key = winreg.OpenKey(hk_user, CYGWIN_KEY)
        return winreg.QueryValueEx(key, "rootdir")[0]
    except:
        return "C:\\cygwin64\\"

def getUserInput(prompt):
    if isPython3():
        return input(prompt)
    else:
        return raw_input(prompt)

def toBytes(s):
    if isPython3() and not isinstance(s, bytes):
        return bytes(s, 'UTF-8')
    return s

def typeIsString(s):
    if isinstance(s, str):
        return True
    if not isPython3():
        return isinstance(s, unicode)
    return False

def toArrayOfStrings(s):
    if not typeIsString(s): return s
    result = []
    parts = s.split(",")
    for p in parts:
        subparts = p.split(" ")
        for sp in subparts:
            sp = sp.strip()
            if len(sp) > 0:
                result.append(sp)
    return result

def toDictionary(s):
    result = {}
    parts = s.split(",")
    for p in parts:
        nameValue = map(lambda x: x.strip(), p.split(":"))
        if typeIsString(nameValue):
            result[nameValue] = True    # default value
        elif len(nameValue[0]) > 0:
            if len(nameValue) == 1:
                result[nameValue[0]] = True  # default value
            else:
                result[nameValue[0]] = ":".join(nameValue[1:])
    return result

def getInt(s):
    try:
        return int(s)
    except:
        return 0

def isExecutable(filename):
    return os.path.isfile(filename) and os.access(filename, os.X_OK)

def isReadable(filename):
    return os.path.isfile(filename) and os.access(filename, os.R_OK)

def runSubprocess(args, runner):
    POLL_INTERVAL = 1.0 # seconds

    #sys.stdout.write("Run subprocess: " + " ".join(args) + "\n")
    retcode = -1

    try:
        with open(os.devnull, 'w') as fp:
            proc = Popen(args, stdout = fp, stderr = STDOUT)
            while proc.poll() is None:
                if runner.shouldTerminate():
                    proc.kill()
                time.sleep(POLL_INTERVAL)
            retcode = proc.returncode
    except OSError as e:
        print("run subprocess OSError:" + str(e))
    except CalledProcessError as e:
        print("run subprocess CalledProcessError:" + str(e))
        retcode = e.returncode
    except Exception as e:
        print("run subprocess exception:" + str(e))
    except:
        print("unexpected error:", sys.exc_info()[0])
    finally:
        #print("done, retcode = " + str(retcode))
        return retcode

def undefined(x, localVariables):
    return x not in localVariables

def createBackgroundThread(function, args):
    # make sure 'args' is a list or a tuple
    if not (type(args) is list or type(args) is tuple):
        args = (args,)
    t = threading.Thread(target=function, args=args)
    # keep it in daemon mode, in order to able to kill the app with Ctrl+C
    t.daemon = True
    t.start() 

# extract a boolean value from http query string
def qsExtractBool(qs, name, defaultValue = None):
    value = defaultValue
    if name in qs:
        arg = qs[name][0]
        try:
            value = bool(int(arg, 0))
        except:
            try:
                value = bool(arg)
            except:
                value = defaultValue
    return value

# extract a string value from http query string
def qsExtractString(qs, name, defaultValue = None):
    value = defaultValue
    if name in qs:
        try:
            value = qs[name][0]
        except:
            value = qs[name]
    return value

def qsExtractInt(qs, name, defaultValue = None):
    value = defaultValue
    if name in qs:
        try:
            value = int(qs[name][0])
        except:
            try:
                value = int(qs[name])
            except:
                value = defaultValue
    return value

def qsExtractFloat(qs, name, defaultValue = None):
    value = defaultValue
    if name in qs:
        try:
            value = float(qs[name][0])
        except:
            try:
                value = float(qs[name])
            except:
                value = defaultValue
    return value

def qsExtractList(qs, name):
    return qs.get(name, [])

# works with arrays of JSON objects
def arrayToDict(array):
    keys = map(lambda x: x["task"], array)
    return dict(zip(keys, array))

def getFloatSafe(s):
    try:
        return float(s)
    except:
        return 0.0

# limit the maximum length of a list by cutting from front
def limitLength(lst, count):
    if len(lst) < count:
        return lst
    return lst[(len(lst) - count + 1):]

# regexp helper
class Matcher:
    def __init__(self, pattern, flags=0):
        self._pattern = re.compile(pattern, flags)
        self._hit = None
    def match(self, line):
        self._hit = re.match(self._pattern, line)
        return self
    def search(self, line):
        self._hit = re.search(self._pattern, line)
        return self._hit
    def matched(self):
        return self._hit is not None
    def group(self, idx):
        return self._hit.group(idx)
    def as_int(self, idx):
        return int(self._hit.group(idx))

def startsWith(s, what):
    return s[:len(what)] == what

def getCurrentTime():
    return datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')

def numCombinations(n, k):
    return math.factorial(n) / math.factorial(k) / math.factorial(n-k)

def floatEqual(f1, f2, epsilon):
    return abs(f1 - f2) <= epsilon
