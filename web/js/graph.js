"use strict";
CORUNNER.graph = function() {

    var chart = null;

    // onload callback
    function setupChart() {
	chart = new google.visualization.LineChart($('#job_chart').get(0));
    }

    function isReady() {
	return chart !== null;
    }

    function drawChart(data) {
	if (!isReady()) {
	    console.log("chart not ready");
	    return;
	}

	var job = data[0]; // XXX

	var params = "";
	for (var j = 0; j < job.parameters.length; ++j) {
            params += job.parameters[j];
            if (j < job.parameters.length - 1) {
                params += ", ";
            }
        }
        $("#job_name").html("<h2>Job " + job.id + "</h2>\n");
        $("#job_parameters").html("<p>Parameters: " + params + "</p>\n");

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
	for (var i = 0; i < job.data.length; i++) {
            jobData.addColumn('number', 'Runner ' + (i+1));
	    runnerValues.push(0.0); // start from zero
	}

        $.each(allData, function (i, entry) { 

	    runnerValues[entry.runner] = entry.of;

	    var row = [];
	    row.push(entry.time);
	    for (var j = 0; j < job.data.length; j++) {
		row.push(runnerValues[j]);
	    }
//	    console.log("row " + i + ": " + JSON.stringify(row));
            jobData.addRow(row);
        });


        chart.draw(jobData, {
	    height: 400, 
	    vAxis : {title: "Best objective function values"},
	    hAxis : {title: "CPU time, seconds"}
        });

    }

    // Load the Visualization API and the piechart package.
    google.load('visualization', '1', {'packages':['corechart']});
    // google.load('visualization', '1', {'packages':['line']});

    // Set a callback to run when the Google Visualization API is loaded.
    google.setOnLoadCallback(setupChart);


    return {
	drawChart : drawChart
    };

}();
