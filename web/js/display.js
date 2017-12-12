"use strict";
SPACESCANNER.display = function() {

    var charts = [];
    var MAX_NUM_CHARTS = 4;
    var button2jobID = [];

    // this stores the last method name for each job
    var methods = {};

    // this stores the last arguments
    var lastArguments = {
        totalNumJobs: 0,
        taskType: "optimization",
        baseline: 0,
        allData: []
    };

    // onload callback
    function setupChart() {
        for (var i = 0; i < MAX_NUM_CHARTS; ++i) {
            charts.push(new google.visualization.LineChart(
                $('#job' + i + '_chart').get(0)));
            button2jobID.push(0); // no mapping
        }
        resetMethods();
    }

    function resetMethods() {
        methods = {};
    }

    function isReady() {
        return charts.length == MAX_NUM_CHARTS;
    }

    function drawCharts(totalNumJobs, taskType, baseline, allData) {
        // copy methods
        var oldMethods = jQuery.extend({}, methods)
        // reset methods
        methods = {};

        // copy the arguments
        lastArguments.totalNumJobs = totalNumJobs;
        lastArguments.taskType = taskType;
        lastArguments.baseline = baseline;
        lastArguments.allData = allData.slice();

        if (!isReady()) {
            console.log("charts are not ready");
            return;
        }

        for (var i = 0; i < MAX_NUM_CHARTS; ++i) {
            if (i < allData.length) {
                showChart(i, charts[i], allData[i], totalNumJobs, taskType, baseline);
                button2jobID[i] = allData[i].id;
                $('#job' + i).show();
            } else {
                button2jobID[i] = 0; // no mapping
                $('#job' + i).hide();
            }
        }
        if (allData.length > MAX_NUM_CHARTS) {
            SPACESCANNER.notify("Too many active jobs, showing only first four");
        }

        for(var key in methods) {
            if (key in oldMethods) {
                if(oldMethods[key] != methods[key]) {
                    SPACESCANNER.notify("Switching job " + key.substr(4)
                                        + " to method " + methods[key]);
                }
            }
        }
    }

    function showChart(i, chart, job, totalNumJobs, taskType, baseline) {
        if (job.error) {
            console.log("Job data has an error: " + job.error);
            return;
        }
        var params = ""; 
        for (var j = 0; j < job.parameters.length; ++j) {
            params += job.parameters[j];
            if (j < job.parameters.length - 1) {
                params += ", ";
            }
        }
        var method = "";
        var pastMethods = "";
        for (var j = 0; j < job.methods.length; ++j) {
            if(j === 0) {
                method = job.methods[j];
            } else {
                pastMethods += job.methods[j];
                if (j < job.methods.length - 1) {
                    pastMethods += ", ";
                }
            }
        }

        var name = taskType === "optimization" ? "Optimization" : "Parameter estimation";
        $("#job" + i + "_name").html("<h2>" + name + " job " + job.id + " of " + totalNumJobs + "</h2>\n");
        $("#job" + i + "_parameters").html("Parameters: <i>" + params + "</i>\n");
        $("#job" + i + "_method").html("Method: <i>" + method
                                       + (pastMethods ? "</i>&nbsp;&nbsp;(previous methods: <i>" + pastMethods + "</i>)" : "</i>") + "\n");

        if (job.active) {
            $("#job" + i + "_actions").show();
            $("#job" + i + "_reason").hide();
            $("#job" + i + "_reason").html("");
        } else {
            $("#job" + i + "_actions").hide();
            $("#job" + i + "_reason").html("Termination reason: <i>" + job.reason + "</i>\n");
            $("#job" + i + "_reason").show();
        }

        // save the current method
        methods["#job" + job.id] = method

        var allData = [];
        var startData = [];
        var maxTime = 0.0;

        var config = SPACESCANNER.settings.get("optimization");
        var referenceTime = config.paramEstimationReferenceValueSec;
        if (referenceTime === undefined) {
            referenceTime = 0;
        }

        var lastValues = {};
        var hasData = [];
        var hasStartData = [];
        for (var runner = 0; runner < job.data.length; runner++) {
            var jobdata = job.data[runner];
            hasData.push(false);
            hasStartData.push(false);
            //console.log("Job " + runner + " data: " + JSON.stringify(jobdata));
            for (var j = 0; j < jobdata.values.length; j++) {
                var r = {time: jobdata.time[j], of: jobdata.values[j], runner: runner};
                if (jobdata.time[j] < referenceTime) {
                    startData.push(r);
                    hasStartData[runner] = true;
                } else {
                    allData.push(r);
                    hasData[runner] = true;
                }
                maxTime = Math.max(maxTime, r.time);
                if (j === jobdata.values.length - 1) {
                    lastValues[runner] = r.of;
                }
            }
        }

        // if before '2 * ref_time' show all data; else show just the non-starting data
        if (maxTime < 2.0 * referenceTime || taskType === "optimization" ) {
            allData = allData.concat(startData);
            // mark that the data is present if just some start data is preset
            for (var runner = 0; runner < job.data.length; runner++) {
                if (hasStartData[runner]) {
                    hasData[runner] = true;
                }
            }
        }

        var maximization = taskType === "optimization" ? 1 : -1;
        allData.sort(function (a, b){
            // sort by time first
            if (a.time < b.time) return -1;
            if (a.time > b.time) return 1;
            // sort by value second, depending on whether this is maximization task
            if (a.of < b.of) return maximization * -1;
            if (a.of > b.of) return maximization;
            return 0;
        });

        if (allData.length <= 0) {
            // no data; hide the chart (other items related to the job are still displayed)
            $("#job" + i + "_chart").hide();
            return;
        }
        // has data; show the chart
        $("#job" + i + "_chart").show();

        var lastMinValue = 10e100;
        var lastMaxValue = -10e100;
        for (var runner = 0; runner < job.data.length; runner++) {
            if (lastValues[runner] !== undefined) {
                lastMaxValue = Math.max(lastMaxValue, lastValues[runner]);
                lastMinValue = Math.min(lastMinValue, lastValues[runner]);
            }
        }

        //var bestValue = (taskType === "optimization") ? lastMaxValue : lastMinValue;
        //var worstValue = (taskType === "optimization") ? lastMinValue : lastMaxValue;
        $("#job" + i + "_best_value").html(
            "Min value: <i>" + lastMinValue + "</i>" +
                "&nbsp;&nbsp;&nbsp;&nbsp;" +
                "Max value: <i>" + lastMaxValue + "</i>");

        var runnerValues = [];
        var jobData = new google.visualization.DataTable();

        var firstValue = allData[0];
        if (taskType === "optimization") {
            if (baseline < firstValue) {
                firstValue = baseline;
            }
        } else {
            if (baseline > firstValue) {
                firstValue = baseline;
            }
        }

        jobData.addColumn('number'); //, 'Time');
        for (var runner = 0; runner < job.data.length; runner++) {
            if (hasData[runner]) {
                var name = 'Runner ' + (runner+1) + ' \n(' + lastValues[runner] + ')';
                jobData.addColumn('number', name);

                // start from the first value / baseline (if present), not from zero
                runnerValues.push(firstValue);
            }
        }

        $.each(allData, function (_, entry) { 

            runnerValues[entry.runner] = entry.of;

            var row = [];
            row.push(entry.time);
            for (var runner = 0; runner < job.data.length; runner++) {
                if (hasData[runner]) {
                    row.push(runnerValues[runner]);
                }
            }
            jobData.addRow(row);
        });

        //console.log("All job data: " + JSON.stringify(jobData));

        var webConfig = SPACESCANNER.settings.get("web");
        var taskName = taskType === "optimization" ?
            "Objective function" :
            "Parameter estimation error";

        var options =  {
            height: 400,
            width: $("#main").width(),
            vAxis : {
                title: taskName + " values",
                scaleType: webConfig["logyaxis"] === true ? 'log' : null,
            },
            hAxis : {
                title: "CPU time, seconds",
                scaleType:  webConfig["logxaxis"] === true ? 'log' : null,
            }
        };
        chart.draw(jobData, options);
    }

    // Load the Visualization API and the piechart package.
    google.load('visualization', '1', {'packages':['corechart']});
    // google.load('visualization', '1', {'packages':['line']});

    // Set a callback to run when the Google Visualization API is loaded.
    google.setOnLoadCallback(setupChart);


    return {
        drawCharts : drawCharts,
        resetMethods : resetMethods,
        refresh : function () {
            // simply redraw the last state;
            // useful when e.g. display settings have changed.
            drawCharts(lastArguments.totalNumJobs,
                       lastArguments.taskType,
                       lastArguments.baseline,
                       lastArguments.allData);
        },
        getJobID : function (i) { return button2jobID[i] }
    };

}();
