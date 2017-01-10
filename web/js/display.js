"use strict";
SPACESCANNER.display = function() {

    var charts = [];
    var MAX_NUM_CHARTS = 4;
    var button2jobID = [];

    // this stores the last method name for each job
    var methods = {};

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

    function drawCharts(totalNumJobs, baseline, allData) {
        // copy methods
        var oldMethods = jQuery.extend({}, methods)
        // reset methods
        methods = {};

        if (!isReady()) {
            console.log("charts are not ready");
            return;
        }

        for (var i = 0; i < MAX_NUM_CHARTS; ++i) {
            if (i < allData.length) {
                showChart(i, charts[i], allData[i], totalNumJobs, baseline);
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

    function showChart(i, chart, job, totalNumJobs, baseline) {
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

        $("#job" + i + "_name").html("<h2>Job " + job.id + " of " + totalNumJobs + "</h2>\n");
        $("#job" + i + "_parameters").html("Parameters: <i>" + params + "</i>\n");
        $("#job" + i + "_method").html("Method: <i>" + method
                                       + (pastMethods ? "</i>&nbsp;&nbsp;(previous methods: <i>" + pastMethods + ")" : "") + "</i>\n");

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
        for (var runner = 0; runner < job.data.length; runner++) {
            var jobdata = job.data[runner];
            for (var j = 0; j < jobdata.values.length; j++) {
                allData.push({time: jobdata.time[j], of: jobdata.values[j], runner: runner});
            }
        }

        allData.sort(function (a, b){  
            if (a.time < b.time) return -1;
            if (a.time > b.time) return 1;
            return 0;
        });

        var runnerValues = [];
        var jobData = new google.visualization.DataTable();
        jobData.addColumn('number'); //, 'Time');
        for (var j = 0; j < job.data.length; j++) {
            jobData.addColumn('number', 'Runner ' + (j+1));
            // start from the baseline (if present), not from zero
            runnerValues.push(baseline);
        }

        $.each(allData, function (_, entry) { 

            runnerValues[entry.runner] = entry.of;

            var row = [];
            row.push(entry.time);
            for (var j = 0; j < job.data.length; j++) {
                row.push(runnerValues[j]);
            }
            jobData.addRow(row);
        });

        var options =  {
            height: 400,
            width: $("#main").width(),
            vAxis : {title: "Best objective function values"},
            hAxis : {title: "CPU time, seconds"}
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
        getJobID : function (i) { return button2jobID[i] }
    };

}();
