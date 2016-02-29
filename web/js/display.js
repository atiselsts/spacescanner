"use strict";
CORUNNER.display = function() {

    var charts = [];
    var MAX_NUM_CHARTS = 4;
    var button2jobID = [];

    // onload callback
    function setupChart() {
        for (var i = 0; i < MAX_NUM_CHARTS; ++i) {
            charts.push(new google.visualization.LineChart(
                $('#job' + i + '_chart').get(0)));
            button2jobID.push(0); // no mapping
        }
    }

    function isReady() {
        return charts.length == MAX_NUM_CHARTS;
    }

    function drawCharts(allData) {
        if (!isReady()) {
            console.log("charts are not ready");
            return;
        }

        for (var i = 0; i < MAX_NUM_CHARTS; ++i) {
            if (i < allData.length) {
                showChart(i, charts[i], allData[i]);
                button2jobID[i] = allData[i].id;
                $('#job' + i).show();
            } else {
                button2jobID[i] = 0; // no mapping
                $('#job' + i).hide();
            }
        }
        if (allData.length > MAX_NUM_CHARTS) {
            CORUNNER.notify("Too many active jobs, showing only first four");
        }
    }

    function showChart(i, chart, job) {
        var params = ""; 
        for (var j = 0; j < job.parameters.length; ++j) {
            params += job.parameters[j];
            if (j < job.parameters.length - 1) {
                params += ", ";
            }
        }

        $("#job" + i + "_name").html("<h2>Job " + job.id + "</h2>\n");
        $("#job" + i + "_parameters").html("<p>Parameters: " + params + "</p>\n");

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
            runnerValues.push(0.0); // start from zero
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
        getJobID : function (i) { return button2jobID[i] }
    };

}();
