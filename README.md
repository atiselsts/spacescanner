# SpaceScanner: [Copasi](http://copasi.org) optimization run launcher ##

[![Build Status](https://travis-ci.org/atiselsts/spacescanner.svg?branch=master)](https://travis-ci.org/atiselsts/spacescanner/branches)

**The SpaceScanner publication**:

If you use this software, please cite the relevant application note:

*Atis Elsts, Agris Pentjuss, Egils Stalidzans;* SpaceScanner: COPASI wrapper for automated management of global stochastic optimization experiments. *Bioinformatics*, Oxford University Press, 2017.
DOI: https://doi.org/10.1093/bioinformatics/btx363*

**SpaceScanner** features:

* run multiple parallel optimization or parameter estimation tasks on a biological model, and automatically terminate when the tasks have reached a consensus value;
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


# User manual

Available [here](doc/SpaceScanner%20User%20Manual%20v03.pdf).


# Directory structure of this repository

* `source` - SpaceScanner source code;
* `doc` - an example SpaceScanner configuration file with comments and the default settings;
* `tests` - testing code, including several SpaceScanner configuration files examples;
* `models` - several Copasi model examples;
* `copasi` - Copasi executables;
* `web` - SpaceScanner web interface source code.


# Installation

[Download](https://github.com/atiselsts/spacescanner/archive/master.zip) and extract the SpaceScanner repository, which includes SpaceScanner source code and Web interface launcher, as well as COPASI binaries for Windows, Linux (64-bit) and macOS.

Alternatively, get it through Git: `git clone https://github.com/atiselsts/spacescanner.git`.

**Prerequisites:**

* Python (both version 2 and version 3 are supported);
* `psutil` Python module.
* `Flask` Python module.
* `gevent` Python module.

Install the requirements with PIP, Python package manager, e.g.:

   `sudo pip install -r requirements.txt`
 
To install `pip`, it may be possible to use `easy_install`:

   `sudo easy_install pip`

SpaceScanner has been successfully tested on 64-bit Linux and Windows, including Cygwin.


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


## Configuration file

The name of the file must be passed as command line parameter if run from the command line. If web interface is used, the file is automatically generated.

The configuration file contains a number of fields grouped in a number of sections.

### "copasi" section

This section defines the model file and optimization methods to use.

Fields:

* `modelFile` - COPASI model file name; `@SELF@` refers to SpaceScanner source directory
* `taskType` - whether to run an optimization task ("optimization") or a parameter estimation ("parameterFitting") task; default: "optimization")
* `methods` - list of optimization methods to use; the methods are selected sequentially, each subsequent one is selected when the previous ones fail; can contain a method more than once
* `fallbackMethods` - list of optimization methods to use when a method fails to evaluate the objective function in given time; useful for e.g. highly constrained models on which many methods may not find any solutions at all
* `randomizeMethodSelection` - whether to pick methods from the configuration randomly or in order (default: `false`)
* `methodParametersFromFile` - whether to use optimization method parameters from COPASI model file (default: `false`)

### "optimization" section

Defines maximal duration of optimization runs, termination criteria etc.

Fields:

* `timeLimitSec` - maximal CPU time for optimization in case the consensus criteria and other end conditions have not been reached (default: 600 sec)
* `consensusCorridor` - the consensus criteria is satisfied if values of all runs are within this consensus corridor range (default: 1%)
* `consensusAbsoluteError` - to determine whether the consensus criteria has been reached (default: 1e-6)
* `consensusDelaySec` - the minimal time to continue after the consensus criteria has been reached (default: 300 sec)
* `consensusProportionalDelay` - the minimal time to continue after the consensus criteria has been reached as proportion of the runtime so-far (default: 15%)
* `stagnationDelaySec` - the maximal time to continue when no values of any parallel run are changing (default: 300 sec)
* `stagnationProportionalDelay` - the maximal time to continue when no values of any parallel run are changing, as proportion of the runtime so-far (default: 15%)
* `targetFractionOfTOP` - compared to the full-set objective function value or the user-defined TOP value(default: 0.0 (i.e., disabled), range: [0.0 .. 1.0])
* `bestOfValue` - the user-defined best (TOP) objective function's value (default: `null`)
* `restartFromBestValue` - restart each subsequent method from the best point in the search space so far (default: `true`)
* `paramEstimationReferenceValueSec` - this is used a reference point when to obtain the initial baseline value of the objective function (default: 3 seconds of the CPU time)
* `maxConcurrentRuns` - how many COPASI processes to run by parallel (default: max(4, the number of CPU cores); range: [1 .. number of CPU cores])
* `runsPerJob` - how many parallel COPASI processes per each job (i.e. a single set of parameters)

### "parameters" section

Defines the way how subsets of parameters are selected. Note that the optimization parameters as such are defined in the `.sbml` model file, not here!

The section is an array of records of arbitrary length. If repeating or overlapping records are specified, an optimization job for a given subset of parameters is still run only once.

Records may have the following type:

* `full-set` - a single optimization job containing all parameters in the model as specified in the `.sbml` file
* `exhaustive - all` possible combinations of `N` to `M` parameters. Field "range" defines the values of `N` and `M`. For example, `"range" : [1, 3]` selects `N` to be equal to 1, `M` to 3. `"range" : [2]` selects `N = M = 2`.
* `greedy` - for `N` parameters, take the best set of `N-1` parameters and run all possible optimizations that add one parameter not yet in the set. Unless `N=1`, there must also be a record describing which strategy to use to for `N-1` parameter sets.
* `greedy-reverse` - similar to "greedy", but takes away a single parameter from the best `N+1` parameter set instead of adding it.
* `explicit` - the names of parameters to use are explicitly named in the "parameters" field of the record.

By default, these records are present:

* `full-set`;
* `exhaustive` with range [1..3];
* `greedy` with range [4..8].

### "web" section

Web interface settings.

Fields:

* `enable` - whether to run the web interface (default: `true`). **Warning:** access control is not supported by SpaceScanner! Enable this only in trusted environments.
* `port` - HTTP port number (default: 19000)
* `logxaxis` - show x-axis in log scale (default: `false`)
* `logyaxis` - show y-axis in log scale (default: `false`)


### "output" section

Logging settings.

Fields:

* `filename` - the file name to use for optimization results (default: "results-<taskname>-<datetime>.csv")
* `loglevel` - debug log level; from 0 to 4, higher means more messages (default: 2)
* `numberOfBestCombinations` -  how many of the best parameter combinations to include in results for each number of parameters; 0 means unlimited (default: unlimited)

### Not in separate sections

* `restartOnFile` - .csv file name on which to restart optimization runs, trying to complete timed-out jobs (default: `null`)
* `taskName` - the global name of this optimization task

### Example configuration file

<pre>{
    "copasi" : {
        "modelFile" : "@SELF@/models/optimization/simple-6params.cps",
	"taskType" : "optimization",
        "methods" : ["ParticleSwarm", "GeneticAlgorithm", "GeneticAlgorithmSR", "EvolutionaryProgram", "EvolutionaryStrategySR", "ScatterSearch", "SimulatedAnnealing"],
        "fallbackMethods" : ["GeneticAlgorithmSR", "EvolutionaryStrategySR"],
        "randomizeMethodSelection" : false,
        "methodParametersFromFile" : false,
        "parameters": []
    },
    "optimization" : {
        "timeLimitSec" : 60,
        "consensusCorridor" : 0.01,
        "consensusAbsoluteError" : 1e-6,
        "consensusDelaySec" : 60,
        "consensusProportionalDelay" : 0.15,
        "paramEstimationReferenceValueSec" : 3.0,
        "targetFractionOfTOP" : 0.9,
        "bestOfValue" : null,
        "restartFromBestValue" : true,
        "maxConcurrentRuns" : 4,
        "runsPerJob" : 2
    },
    "parameters" : [
        {"type" : "full-set"},
        {"type" : "exhaustive", "range" : [1, 3]},
        {"type" : "greedy", "range" : [4, 8]}
    ],
    "restartOnFile" : null,
    "web" : {
	"enable" : true,
	"port" : 19000
    },
    "output" : {
        "filename" : "results.csv",
        "loglevel" : 2,
	"numberOfBestCombinations" : 0
    },
    "taskName" : null
}</pre>


# Stopping SpaceScanner

* "Stop" button - terminate a specific, currently running job (stops all runners of that job).
* "Stop all" button - completely stops the analysis of the current model - terminates all running jobs and clears the queue of scheduled jobs.

To terminate the SpaceScanner server, either use the command line (Ctrl+C) or go to *Settings* -> *Other*. Here, a button for that is provided:
* "Stop server" - terminates the SpaceScanner application itself.

# Accessing the results

SpaceScanner stores the results of finished jobs in `spacescanner/results` directory. **Warning:** for tasks with a large number of jobs these directories can take quite a lot of space on the disk!

Each optimization task (i.e., a collection of jobs) is stored in a separate directory. This directory contains the configuration of that task, the `.log` file of the execution, and `.csv` file where the results of finished jobs are stored.

Each job gets its own subdirectory. These subdirectories contain Copasi model files (stored as `.cps`), and Copasi process execution histories (stored as `.log` files). The `.cps` files contain the input model; for all finished runs they also include the parameter values on which that run achieved its best objective function value.
