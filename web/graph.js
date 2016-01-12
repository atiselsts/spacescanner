"use strict";

var chartJob = null;
var methodField = null;

var isInitialized = false;

// view the first job results by default
var jobIndex = 1;

function getParameterByName(name) {
    name = name.replace(/[\[]/, "\\[").replace(/[\]]/, "\\]");
    var regex = new RegExp("[\\?&]" + name + "=([^&#]*)"),
        results = regex.exec(location.search);
    return results === null ? "" : decodeURIComponent(results[1].replace(/\+/g, " "));
}

// onload callback
function setupChart() {
    chartJob = new google.visualization.LineChart($('#chart-job').get(0));

    methodField = $('#methods');

    var qsJob = getParameterByName('job');
    if (qsJob) jobIndex = qsJob;

    drawChart();
}

function drawChart() {
    var url = 'http://localhost:19000/jobs/' + jobIndex;
    var jsonData = $.ajax({
        url: 'http://localhost:19000/jobs/' + jobIndex,
        data: {},
        contentType: "application/json",
        dataType: "json",
        crossDomain: true,
    }).done(function (result, textStatus, jqXHR) {

        //console.log("done, result=" + JSON.stringify(result));

	var methods = result.methods;
	var allData = [];

        $.each(result.data, function (method, row) { 
            //console.log("row=" + JSON.stringify(row));

            for (var i = 0; i < row.values.length; i++) {
		var data = [row.time[i], row.values[i], method];
		allData.push(data);
            }
        });

	function Cmp(a, b){  
	    if (a[0] < b[0]) return -1;
	    if (a[0] > b[0]) return 1;
	    return 0;
	}

	allData.sort(Cmp);

        //console.log("row=" + JSON.stringify(allData));

	var methodValues = [];
        var jobData = new google.visualization.DataTable();
        jobData.addColumn('number', 'Time');
	for (var i = 0; i < methods.length; i++) {
            jobData.addColumn('number', 'Method ' + (i+1));
	    methodValues.push(0);
	}

        $.each(allData, function (i, entry) { 

	    methodValues[entry[2]] = entry[1];

	    var row = [];
	    row.push(entry[0]);
	    for (var i = 0; i < methods.length; i++) {
		row.push(methodValues[i]);
	    }

            jobData.addRow(row);
        });

        chartJob.draw(jobData, {
            title: 'Convergence of the different methods',
            vAxis: {
                title: "Best objective function values"
            },
            hAxis: {
                title: "CPU time, seconds"
            }
        });

	var txt = "<p>";
	for (var i = 0; i < methods.length; i++) {
	    txt += "&nbsp;&nbsp;Method " + (i+1) + ": " + methods[i] + "<br/>";
	}
	txt += "</p>"
	methodField.html(txt);
	

        setTimeout(drawChart, 1000);
    })
    .fail(function(jqXHR, textStatus, errorThrown) {
        setTimeout(drawChart, 1000);
    });
}

// Load the Visualization API and the piechart package.
google.load('visualization', '1', {'packages':['corechart']});

// Set a callback to run when the Google Visualization API is loaded.
google.setOnLoadCallback(setupChart);
