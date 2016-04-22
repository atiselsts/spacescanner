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
* a web interface that allows the user to interactively configure, start, and stop Copasi optimizations, as well as see their results graphically.


# Directory structure of this repository

* `source` - SpaceScanner source code;
* `doc` - an example SpaceScanner configuration file with comments and the default settings;
* `tests` - testing code, including several SpaceScanner configuration files examples;
* `models` - several Copasi model examples;
* `copasi` - Copasi executables;
* `web` - SpaceScanner web interface source code.


# Installation

There's no installation necessary. [Download](https://github.com/atiselsts/spacescanner/archive/master.zip) and extract the SpaceScanner source code. Alternatively, get it through Git: `git clone https://github.com/atiselsts/spacescanner.git`.

**Prerequisites:**
* Python (version 2.7);

SpaceScanner has been successfully tested on 64-bit Linux and Windows, including Cygwin.

`psutil` Python module is included in this together with the SpaceScanner in order to simplify the installation.


# SpaceScanner terminology

There are multiple similar terms with quite different meanings used in the UI and documentation:

* A **run** is a single optimization process. Each active run corresponds to a single Copasi process instance.
* A **job** is a collection of one or more optimization *runs* that all share the same set of parameters and are executed in parallel.
* A **task** is a collection of one or more *jobs* described by a single configuration file. A task corresponds to single command-line execution of SpaceScanner.


# Running SpaceScanner

## From the web interface

Double click on `spacescanner/spacescanner_launcher.py` file. This both starts the SpaceScanner executable (if not started yet) and opens the web interface in a web browser.

Alternatively, start `spacescanner/source/spacescanner.py` from a command line, passing the string "web" as the parameter, and open the web interface manually (default URL: `http://localhost:19000`).

## From command line

Simply execute the `spacescanner/source/spacescanner.py` script, passing the configuration file name as a parameter.


# Accessing the results

SpaceScanner stores the results of finished jobs in `spacescanner/results` directory. **Warning:** for tasks with a large number of jobs these directories can take quite a lot of space on the disk!

Each optimization task (i.e., a collection of jobs) is stored in a separate directory. This directory contains the configuration of that task, the `.log` file of the execution, and `.csv` file where the results of finished jobs are stored.

Each job gets its own subdirectory. These subdirectories contain Copasi model files (stored as `.cps`), and run execution histories (stored as `.txt` files). The `.cps` files contain the input model; for all finished runs they also include the parameter values on which that run achieved its best objective function value.
