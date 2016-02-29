# CoRunner: [Copasi](http://copasi.org) optimization run launcher ##

[![Build Status](https://travis-ci.org/atiselsts/corunner.svg)](https://travis-ci.org/atiselsts/corunner/branches)

**CoRunner** features:
* run multiple parallel optimization tasks on a biological model, and automatically terminate when the tasks have reached a consensus value;
* display optimization history graphically for these parallel runs;
* determine the minimal subset of parameters that gives "good enough" results for a specific objective function.

Corunner requires the following inputs:
* a Copasi model file (`.sbml`), that
* includes a user-defined objective function,
* optimization parameters and methods
and produces these outputs:
* `.csv` file with the best (or all) optimization results
* a `.log` file
* a `.txt` file for each optimization run, describing the history of the optimization process and the end parameter values;
* a Copasi model for each optimization run; besides the input model, each of these file contains the parameter values that gives the best objective function value at the file's configuration.

CoRunner internally uses [Copasi](http://copasi.org) to execute the optimizations.

**CoRunner** at the moment supports greedy and exhaustive search strategies when looking for the minimal satisfying number of parameters. "Smarter" search strategies are planned as future additions.

**CoRunner** is easy to use and configure. There are two ways how to work with CoRunner:
* a command-line interface that expects a configuration file in JSON format as the only argument;
* a web interface that allows the user to interactively configure, start, and stop the optimizations, as well as see their results graphically.


# Directory structure of this repository

* `source` - CoRunner source code;
* `doc` - an example CoRunner configuration file with comments and the default settings;
* `tests` - testing code, including several CoRunner configuration files examples;
* `models` - several Copasi model examples;
* `copasi` - Copasi executables;
* `web` - CoRunner web interface source code.


# Installation

Either `git clone` or [download](https://github.com/atiselsts/corunner/archive/master.zip) and extract the CoRunner source code.

**Prerequisites:**
* Python (version 2);
* `psutil` Python module.

CoRunner has been successfully tested on 64-bit Linux and Windows, including Cygwin.

Install `psutil` with PIP, Python package manager, e.g.:

   `sudo pip install psutil`

To install `pip`, it may be possible to use `easy_install`:

   `sudo easy_install pip`

Alternatively, run this on Ubuntu Linux to install `psutil`:

   `sudo apt-get install python-psutil`


# Terminology

* **Run** - a single optimization. Each active run corresponds to a single Copasi process instance.
* **Job** - single or multiple optimization runs that all share the same set of parameters and are executed in parallel.
* **Task** - a collection of jobs described by a single configuration file. A tasks corresponds to a single command-line execution of CoRunner.


# Execution

## Web interface

Double click on `corunner/corunner_launcher.py` file. This both starts the CoRunner executable (if not started yet) and opens the web interface in a web browser.

Alternatively, start `corunner/source/corunner.py` from a command line, passing the string "web" as the parameter, and open the web interface manually (default URL: `http://localhost:19000`).

## Command line

Simply execute the `corunner/source/corunner.py` script, passing the configuration file name as a parameter.

## Accessing the results

CoRunner stores the results in `corunner/results` directory. **Warning:** for tasks with a large number of jobs these directories can take quite a lot of space on the disk!

Each optimization task (collection of jobs) is stored in a separate directory. This directory contains the configuration of that task, the `.log` file of the execution, and `.csv` file where the results of finished jobs are stored.

Each job gets it's own subdirectory there. These subdirectories contain Copasi model files (as `.cps`), and run execution histories (as `.txt` files). The `.cps` files not only contain the input mode, but for all finished runs they also include the best parameter values of that run.
