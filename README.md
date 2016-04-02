# SpaceScanner: [Copasi](http://copasi.org) optimization run launcher ##

[![Build Status](https://travis-ci.org/atiselsts/spacescanner.svg)](https://travis-ci.org/atiselsts/spacescanner/branches)

**SpaceScanner** features:
* run multiple parallel optimization tasks on a biological model, and automatically terminate when the tasks have reached a consensus value;
* display optimization history graphically for these parallel runs;
* scan the space of the possible parameters sets to optimize, and determine the minimal subset of parameters that gives "good enough" results for a specific objective function and the minimal number of parameters required for a specific target value.

SpaceScanner requires the following inputs:
* a Copasi model file (`.sbml`)
The file must include:
* the objective function to optimize;
* list of changeable parameters of the model with their minimal and maximal values;
* the optimization methods to use and the configurations of these methods.

SpaceScanner produces these global outputs:
* a `.csv` file with the best (or all) optimization results
* a `.log` file tracing the SpaceScanner execution history;

as well as these outputs for each set of optimization parameters:
* a `.txt` file for each of the several parallel optimization runs; the file includes the history of the Copasi optimization process and the end parameter values;
* a Copasi model file for each if the optimization runs; in this file, the optimization parameters are listed to their best values.

SpaceScanner internally uses [Copasi](http://copasi.org) to execute the optimizations.

SpaceScanner at the moment supports greedy and exhaustive search strategies when looking for the minimal satisfying number of parameters. "Smarter" search strategies (e.g. global stochastic search, parameter sensitivity-informed search, MFA-value informed search) are planned as future additions.

SpaceScanner is easy to use and configure. There are two ways how to work with SpaceScanner:
* a command-line interface that expects a configuration file in JSON format as the only argument;
* a web interface that allows the user to interactively configure, start, and stop the optimizations, as well as see their results graphically.


# Directory structure of this repository

* `source` - SpaceScanner source code;
* `doc` - an example SpaceScanner configuration file with comments and the default settings;
* `tests` - testing code, including several SpaceScanner configuration files examples;
* `models` - several Copasi model examples;
* `copasi` - Copasi executables;
* `web` - SpaceScanner web interface source code.


# Installation

Either `git clone` or [download](https://github.com/atiselsts/spacescanner/archive/master.zip) and extract the SpaceScanner source code.

**Prerequisites:**
* Python (version 2);
* `psutil` Python module.

SpaceScanner has been successfully tested on 64-bit Linux and Windows, including Cygwin.

Install `psutil` with PIP, Python package manager, e.g.:

   `sudo pip install psutil`

To install `pip`, it may be possible to use `easy_install`:

   `sudo easy_install pip`

Alternatively, run this on Ubuntu Linux to install `psutil`:

   `sudo apt-get install python-psutil`


# Terminology

* **Run** - a single optimization. Each active run corresponds to a single Copasi process instance.
* **Job** - single or multiple optimization runs that all share the same set of parameters and are executed in parallel.
* **Task** - a collection of jobs described by a single configuration file. A tasks corresponds to a single command-line execution of SpaceScanner.


# Execution

## Web interface

Double click on `spacescanner/spacescanner_launcher.py` file. This both starts the SpaceScanner executable (if not started yet) and opens the web interface in a web browser.

Alternatively, start `spacescanner/source/spacescanner.py` from a command line, passing the string "web" as the parameter, and open the web interface manually (default URL: `http://localhost:19000`).

## Command line

Simply execute the `spacescanner/source/spacescanner.py` script, passing the configuration file name as a parameter.

## Accessing the results

SpaceScanner stores the results in `spacescanner/results` directory. **Warning:** for tasks with a large number of jobs these directories can take quite a lot of space on the disk!

Each optimization task (collection of jobs) is stored in a separate directory. This directory contains the configuration of that task, the `.log` file of the execution, and `.csv` file where the results of finished jobs are stored.

Each job gets it's own subdirectory there. These subdirectories contain Copasi model files (as `.cps`), and run execution histories (as `.txt` files). The `.cps` files not only contain the input mode, but for all finished runs they also include the best parameter values of that run.
