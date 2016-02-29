#!/usr/bin/env python

import os, subprocess, threading, webbrowser, time
from sys import path, version, executable

CORUNNER_PATH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "source")
path.append(CORUNNER_PATH)
from util import *

isServerStarted = False
glock = threading.Lock()

DEFAULT_PORT = 19000

###########################################

def importsOk():
    psutilModuleOK = True

    try:
        import psutil #@UnusedImport
    except ImportError:
        psutilModuleOK = False

    if not psutilModuleOK:
        print("Cannot start CoRunner: psutil module not found")

        if isWindows():
            installStr = "Run:\n\tpip install psutil"
        else:
            installStr = "Run:\n\tsudo apt-get install python-psutil"
        print (installStr)
        return False

    return True

###########################################

def isProcessRunningPosix(names):
    myPid = os.getpid()
    output = subprocess.check_output(["ps", "x"])
    for line in output.splitlines():
        for name in names:
            if line.find(name) == -1: continue
            try:
                pid = int(line.split()[0])
                if pid == myPid: continue
            except:
                continue
            return True
    return False

def isProcessRunningWindows(names):
    # Finding process info on Windows all versions is too complicated
    # without Python extension packages. Leave it for now.
    return False

def isProcessRunning(names):
    if os.name == "posix":
        return isProcessRunningPosix(names)
    else:
        return isProcessRunningWindows(names)

###########################################

def launchBrowser():
    # wait for server to start starting...
    while True:
        with glock:
            doBreak = isServerStarted
        if doBreak: break
        time.sleep(0.1)

    # wait for server to finish starting
    time.sleep(0.2)

    # open the web browser (Firefox in Linux, user's preferred on Windows)
    if isWindows():
        controller = webbrowser.get('windows-default')
    else:
        # will return default system's browser if Firefox is not installed
        controller = webbrowser.get('Firefox')

    url = "http://localhost:{}".format(DEFAULT_PORT)
    controller.open_new_tab(url)

#######################################

def main():
    global isServerStarted

    if not version.startswith("2.7"):
        print("You are using Python version {0}".format(version[:5]))
        print("For CoRunner only version 2.7 is supported")

    if not importsOk():
        exit(1)

    try:
        browserThread = threading.Thread(target=launchBrowser)
        browserThread.start()

        if not isProcessRunning(['corunner.py']):
            print("Launching CoRunner...")
            with glock:
                isServerStarted = True
            pid = os.fork()
            if pid == 0:
                os.execl(executable, executable,
                         * [os.path.join(CORUNNER_PATH, 'corunner.py'), 'web'])
        else:
            with glock:
                isServerStarted = True

        browserThread.join()
    except Exception as e:
        print("Something went wrong:")
        print(e)

#######################################

if __name__ == '__main__':
    main()
