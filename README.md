# CoRunner: [Copasi](http://copasi.org) optimization run launcher ##

Given a Copasi configuration file
with an optimization task, optimization parameters, and methods,
**CoRunner** determines the minimal subset of parameters that gives "good enough" results.

**CoRunner** at the moment supports greedy and exhaustive search strategies.
"Smarter" search strategies are planned as future additions.

**CoRunner** is easy to use and configure. It uses a command-line interface and expects a configuration file in JSON format as the only argument. The output of active and finished Copasi optimization runs is visualized via a web interface. The results of the parameter search are stored in `.csv` files.


# Directory structure

* `launcher` - CoRunner source code;
* `web` - CoRunner web interface source code;
* `doc` - an example CoRunner configuration file with comments and the default settings;
* `tests` - testing code, including several CoRunner configuration files examples;
* `models` - several Copasi model examples;
* `copasi` - Copasi executables.


# Installation

Either `git clone` or [download](https://github.com/atiselsts/corunner/archive/master.zip) and extract the CoRunner source code.

At the moment, the only prerequisite software required to be installed to CoRunner is Python (version 2).

CoRunner has been successfully tested on 64-bit Linux and Windows, including Cygwin.

By default, CoRunner tries to use all available CPU cores for optimization runs. To leave some cores free for other tasks, reduce the `maxConcurrentOptimizations` configuration setting.


# Running on Linux

Simply execute the `corunner/launcher/corunner.py` script, passing the configuration file name as a parameter.


# Running on Windows

Click on the `run.bat` file in the `corunner` folder to start CoRunner.

This relies on Python being installed under `C:/Python27`. If it's installed in a different location on your system, correct the path in `run.bat` before executing the file.


# Accessing the results

To graphically view the progress of individual runs, open the file named `corunner/web/graph.html` file with a web browser while CoRunner is executing.

For example, if CoRunner is installed in `D:/sysbio/`, then the URL to open is: <a href="file:///D:/sysbio/corunner/web/graph.html">`file:///D:/sysbio/corunner/web/graph.html`</a>

To view the graph of a specific job, append `?job=N` to the URL, for example: <a href="file:///D:/sysbio/corunner/web/graph.html?job=2">`file:///D:/sysbio/corunner/web/graph.html?job=2`</a> opens graph showing job #2 progress, given that such a job is either running or has been finished.

CoRunner stores the results in `.csv` files named `results.csv` and `results-best.csv` by default. The files are generated both when CoRunner execution is finished normally and when it is terminated with `Ctrl+C`. Intermediate results are periodically saved to these files as well: the files are overwritten after every 10 finished jobs.