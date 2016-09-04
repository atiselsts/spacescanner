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

import os, sys, time, re, datetime, math, platform, json, csv


################################################
# Version detection

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

################################################
# Constants

# paths
DEFAULT_CONFIG_FILE = "config.json"
SELF_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# note that just 64-bit binaries are included out-of-the-box! (except for Mac)
if isWindows():
    PLATFORM_DIR = "WIN64"
    COPASI_EXECUTABLE = "CopasiSE.exe"
    if isCygwin():
        CYGWIN_DIR = getCygwinDir()
elif isMac():
    PLATFORM_DIR = "Darwin"
    COPASI_EXECUTABLE = "CopasiSE"
else:
    PLATFORM_DIR = "Linux64"
    COPASI_EXECUTABLE = "CopasiSE"

COPASI_DIR = os.environ.get('COPASIDIR')
if not COPASI_DIR:
    COPASI_DIR = os.path.join(SELF_PATH, "copasi", PLATFORM_DIR)
else:
    COPASI_DIR = os.path.join(COPASI_DIR, "bin")

SPACESCANNER_VERSION = "0.1.0 (c) 2016 http://biosystems.lv"

LOG_FATAL = 0
LOG_ERROR = 1
LOG_INFO  = 2
LOG_DEBUG = 3

# possible reasons why a copasi run was stopped
TERMINATION_REASON_COPASI_FINISHED    = 0
TERMINATION_REASON_CPU_TIME_LIMIT     = 1
TERMINATION_REASON_CONSENSUS          = 2
TERMINATION_REASON_GOOD_VALUE_REACHED = 3
TERMINATION_REASON_PROGRAM_QUITTING   = 4
TERMINATION_REASON_STAGNATION         = 5
TERMINATION_REASON_MAX                = 5

MIN_OF_VALUE = float("-inf") # minimal objective function value

ENC = json.JSONEncoder()

################################################

def reasonToStr(reason):
    if reason == TERMINATION_REASON_COPASI_FINISHED:
        return "COPASI finished"
    if reason == TERMINATION_REASON_CPU_TIME_LIMIT:
        return "CPU time limit"
    if reason == TERMINATION_REASON_CONSENSUS:
        return "Consensus reached"
    if reason == TERMINATION_REASON_GOOD_VALUE_REACHED:
        return "Good value reached"
    if reason == TERMINATION_REASON_PROGRAM_QUITTING:
        return "User terminated"
    if reason == TERMINATION_REASON_STAGNATION:
        return "Stagnation"
    return "?"

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

def undefined(x, localVariables):
    return x not in localVariables

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
    return datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d_%H-%M-%S')

def numCombinations(n, k):
    return math.factorial(n) / math.factorial(k) / math.factorial(n-k)

def floatEqual(f1, f2, epsilon):
    return abs(f1 - f2) <= epsilon

def getNonconvergedResults(filename):
    results = []
    with open(filename) as f:
        line = f.readline()
        columns = line.strip().split(",")
        n = (len(columns) - 6) // 2
        paramNames = columns[-n:]
        reader = csv.reader(f)
        for row in reader:
            if row[5] != "CPU time limit":
                continue
            paramsIncluded = [int(x) for x in row[-n*2:-n]]
            rowParamNames = [x for (i,x) in enumerate(paramNames) if paramsIncluded[i]]
            results.append(rowParamNames)
    return results

def jsonFixInfinity(x, defaultValue):
    if math.isnan(x) or math.isinf(x):
        return defaultValue
    return x
