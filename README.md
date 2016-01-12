# CoRunner: [Copasi](http://copasi.org) optimization run launcher ##

Given a Copasi configuration file
with an optimization task, optimization parameters, and methods,
**CoRunner** determines the minimal subset of parameters that gives "good enough" results.

**CoRunner** at the moment supports greedy and exhaustive search strategies.
"Smarter" search strategies are planned as future additions.

**CoRunner** is easy to use and configure. It uses a command-line interface and expects a configuration file in JSON format as the only argument. The output of active and finished Copasi optimization runs is visualized via a web interface. The results of the parameter search are stored in `.csv` files.


# Directory structure

* `launcher` - CoRunner source code
* `web` - CoRunner web interface.
* `doc` - an example CoRunner configuration file with comments;
* `tests` - testing code, including a few CoRunner configuration files;
* `models` - Copasi example models;
* `copasi` - Copasi executables.


# Installation

Either `git clone` or download and extract the CoRunner source code.

The only prerequisite required to execute CoRunner at the moment is Python (version 2).

CoRunner has been successfully tested on 64-bit Linux and Windows (including Cygwin).

By default, CoRunner tries to use all available CPU cores for optmization runs. To leave some cores free for other tasks, change the `maxConcurrentOptimizations` configuration setting to a smaller value.


# Running on Linux

Simply execute the `corunner/launcher/corunner.py` script, passing the configuration file name as a parameter.


# Running on Windows

Click on `run.bat` in the `corunner` folder to start CoRunner.

This relies on Python being installed under `C:/Python27`. If it's installed in a different location on your system, correct the path in `run.bat` file before executing it.


# Accessing the results

To view the graphs: open the `corunner/web/graph.html` file in corunner folder with a web browser.

For example, if my corunner folder is in `D:/sysbio/`, then the URL to open is: [file:///D:/sysbio/corunner/web/graph.html](file:///D:/sysbio/corunner/web/graph.html)

To view the graph of a specific job, append `?job=N` to the file name, for example: [file:///D:/sysbio/corunner/web/graph.html?job=2](file:///D:/sysbio/corunner/web/graph.html)

CoRunner stores the results in `.csv` files named `results.csv` and `results-best.csv` by default. The files are generated both when CoRunner execution is finished normally and when it is terminated with `Ctrl+C`. Intermediate results are periodically saved to these files as well: the files are overwritten after every 10 finished jobs.