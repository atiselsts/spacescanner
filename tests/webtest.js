//
// To run this install node.js modules:
//     npm install -S 'jquery@>=2.1'
//     npm install -S 'jsdom@3.1.2'
//     npm install sleep'

'use strict';

var firstTest = testJson;

var fs = require('fs');
var sleep = require('sleep');
var $;

var jsdom = require('jsdom').jsdom;
jsdom.env({
    html : "<html><body></body></html>",
    done : function(errs, window) {
	$ = require('jquery')(window);
	firstTest();
    }
});

// post model file
function test1()
{
    var contents = fs.readFileSync('../models/simple-6params.cps', "utf8");
    if (!contents) {
	console.log("Error while reading model file");
	return;
    }

    $.ajax({
	type: "POST",
	url: "http://localhost:19000/model",
	data: contents,
	contentType: "application/xml",
	timeout: 1000,
	crossDomain: true,
	success: function (returnData) {
	    console.log("model file command: " + returnData);
	    test2();
	},
	error: function (data, textStatus, xhr) {
	    console.log("post model file: error: " + data + " " + textStatus);
	}
    });
}

// start running (with config file attached)
function test2()
{
    var contents = fs.readFileSync('webtest.json', "utf8");
    if (!contents) {
	console.log("Error while reading config file");
	return;
    }

    $.ajax({
	type: "POST",
	url: "http://localhost:19000/start",
	data: contents,
	contentType: "application/json",
	dataType: "json",
	crossDomain: true,
	success: function (returnData) {
	    console.log("start command: " + JSON.stringify(returnData));

	    // sleep a bit 
	    console.log("sleeping...")
	    sleep.sleep(7);
	    test3();
	},
	error: function (data, textStatus, xhr) {
	    console.log("post config file: error: " + data + " " + textStatus);
	}
    });
}

// get status of active jobs
function test3()
{
    // get job lists
    $.ajax({
	type: "GET",
	url: "http://localhost:19000/status",
	contentType: "application/json",
	dataType: "json",
	crossDomain: true,
	success: function (returnData) {
	    console.log("active jobs: " + JSON.stringify(returnData));
	    test3a();
	},
	error: function (data, textStatus, xhr) {
	    console.log("get active jobs error: " + data + " " + textStatus);
	}
    });
}

// get status of all jobs
function test3a()
{
    // get job lists
    $.ajax({
	type: "GET",
	url: "http://localhost:19000/allstatus",
	contentType: "application/json",
	dataType: "json",
	crossDomain: true,
	success: function (returnData) {
	    console.log("all jobs: " + JSON.stringify(returnData));
	    test4();
	},
	error: function (data, textStatus, xhr) {
	    console.log("get all jobs error: " + data + " " + textStatus);
	}
    });
}

// get specific job (number 3)
function test4()
{
    $.ajax({
	type: "GET",
	url: "http://localhost:19000/job/3",
	dataType: "json",
	crossDomain: true,
	success: function (returnData) {
	    console.log("job 3: " + JSON.stringify(returnData));
	    test5();
	},
	error: function (data, textStatus, xhr) {
	    console.log("return error: " + data + " " + textStatus);
	}
    });
}

// get results
function test5()
{
    $.ajax({
	type: "GET",
	url: "http://localhost:19000/results",
	crossDomain: true,
	success: function (returnData) {
	    console.log("results: " + returnData);
	    test6();
	},
	error: function (data, textStatus, xhr) {
	    console.log("return error: " + data + " " + textStatus);
	}
    });
}

// get config
function test6()
{
    $.ajax({
	type: "GET",
	url: "http://localhost:19000/config",
	dataType: "json",
	crossDomain: true,
	success: function (returnData) {
	    console.log("config: " + JSON.stringify(returnData));
	    test7();
	},
	error: function (data, textStatus, xhr) {
	    console.log("get config error: " + JSON.stringify(data) + " " + textStatus);
	}
    });
}


// stop running specific job (number 3)
function test7()
{
    $.ajax({
	type: "GET",
	url: "http://localhost:19000/stop/3",
	dataType: "json",
	crossDomain: true,
	success: function (returnData) {
	    console.log("stop job 3: " + JSON.stringify(returnData));
	    test8();
	},
	error: function (data, textStatus, xhr) {
	    console.log("stop job error: " + data + " " + textStatus);
	}
    });
}


// stop all jobs
function test8()
{
    $.ajax({
	type: "GET",
	url: "http://localhost:19000/stopall",
	crossDomain: true,
	dataType: "json",
	success: function (returnData) {
	    console.log("stopall: " + JSON.stringify(returnData));
	},
	error: function (data, textStatus, xhr) {
	    console.log("stopall error: " + data + " " + textStatus);
	}
    });
}
