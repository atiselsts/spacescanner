//
// To run this install node.js modules:
//  $ npm install -S 'jquery@>=2.1'
//  $ npm install -S 'jsdom@3.1.2'
//  $ npm install sleep
//
// Then run:
//  $ nodejs webtest.js

'use strict';

var fs = require('fs');
var sleep = require('sleep');
var $;

var jsdom = require('jsdom').jsdom;
jsdom.env({
    html : "<html><body></body></html>",
    done : function(errs, window) {
        $ = require('jquery')(window);
        startTests();
    }
});

// ------------------------------------------------------------

// post model file
function test1()
{
    logTest("TEST 1");

    var contents = fs.readFileSync('../dependencies/models/simple-6params.cps', "utf8");
    if (!contents) {
        console.log("Error while reading model file");
        failTests();
        return;
    }

    $.ajax({
        type: "POST",
        url: "http://localhost:19000/modelfile",
        data: contents,
        contentType: "application/xml",
        timeout: 1000,
        crossDomain: true,
        success: function (returnData) {
            console.log("model file command: " + returnData);
            if (returnData.error) {
                failTests();
            } else {
                nextTest();
            }
        },
        error: function (data, textStatus, xhr) {
            console.log("post model file: error: " + data + " " + textStatus);
            failTests();
        }
    });
}

// start running (with config file attached)
function test2()
{
    logTest("TEST 2");

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

            if (returnData.error) {
                failTests();
            } else {
                // sleep a bit
                console.log("sleeping for 7 seconds...")
                sleep.sleep(7);
                nextTest();
            }
        },
        error: function (data, textStatus, xhr) {
            console.log("post config file: error: " + data + " " + textStatus);
            failTests();
        }
    });
}

// get status of active jobs
function test3()
{
    logTest("TEST 3");

    // get job lists
    $.ajax({
        type: "GET",
        url: "http://localhost:19000/status",
        contentType: "application/json",
        dataType: "json",
        crossDomain: true,
        success: function (returnData) {
            console.log("active jobs: " + JSON.stringify(returnData));
            if (returnData.error) {
                failTests();
            } else {
                nextTest();
            }
        },
        error: function (data, textStatus, xhr) {
            console.log("get active jobs error: " + data + " " + textStatus);
            failTests();
        }
    });
}

// get status of all jobs
function test4()
{
    logTest("TEST 4");

    // get job lists
    $.ajax({
        type: "GET",
        url: "http://localhost:19000/allstatus",
        contentType: "application/json",
        dataType: "json",
        crossDomain: true,
        success: function (returnData) {
            console.log("all jobs: " + JSON.stringify(returnData));
            if (returnData.error) {
                failTests();
            } else {
                nextTest();
            }
        },
        error: function (data, textStatus, xhr) {
            console.log("get all jobs error: " + data + " " + textStatus);
            failTests();
        }
    });
}

// get specific job (number 2)
function test5()
{
    logTest("TEST 5");

    $.ajax({
        type: "GET",
        url: "http://localhost:19000/job/2",
        dataType: "json",
        crossDomain: true,
        success: function (returnData) {
            console.log("job 2: " + JSON.stringify(returnData));
            if (returnData.error) {
                failTests();
            } else {
                nextTest();
            }
        },
        error: function (data, textStatus, xhr) {
            console.log("return error: " + data + " " + textStatus);
            failTests();
        }
    });
}

// get results
function test6()
{
    logTest("TEST 6");

    $.ajax({
        type: "GET",
        url: "http://localhost:19000/results",
        crossDomain: true,
        success: function (returnData) {
            console.log("results: " + returnData);
            if (returnData.error) {
                failTests();
            } else {
                nextTest();
            }
        },
        error: function (data, textStatus, xhr) {
            console.log("return error: " + data + " " + textStatus);
            failTests();
        }
    });
}

// get config
function test7()
{
    logTest("TEST 7");

    $.ajax({
        type: "GET",
        url: "http://localhost:19000/config",
        dataType: "json",
        crossDomain: true,
        success: function (returnData) {
            console.log("config: " + JSON.stringify(returnData));
            if (returnData.error) {
                failTests();
            } else {
                nextTest();
            }
        },
        error: function (data, textStatus, xhr) {
            console.log("get config error: " + JSON.stringify(data) + " " + textStatus);
            failTests();
        }
    });
}


// stop running specific job (number 2)
function test8()
{
    logTest("TEST 8");

    $.ajax({
        type: "GET",
        url: "http://localhost:19000/stop/2",
        dataType: "json",
        crossDomain: true,
        success: function (returnData) {
            console.log("stop job 2: " + JSON.stringify(returnData));
            if (returnData.error) {
                failTests();
            } else {
                nextTest();
            }
        },
        error: function (data, textStatus, xhr) {
            console.log("stop job error: " + data + " " + textStatus);
            failTests();
        }
    });
}


// stop all jobs
function test9()
{
    logTest("TEST 9");

    $.ajax({
        type: "GET",
        url: "http://localhost:19000/stopall",
        crossDomain: true,
        dataType: "json",
        success: function (returnData) {
            console.log("stopall: " + JSON.stringify(returnData));
            if (returnData.error) {
                failTests();
            } else {
                nextTest();
            }
        },
        error: function (data, textStatus, xhr) {
            console.log("stopall error: " + data + " " + textStatus);
            failTests();
        }
    });
}

// ------------------------------------------------------------

var testArray = [test1, test2, test3,
                 test4, test5, test6,
                 test7, test8, test9];
var testIndex = 0;

function startTests() {
    console.log("Starting web API testing...\n");

    nextTest();
}

function nextTest()
{
    if (testIndex < testArray.length) {
        // call the next function
        var index = testIndex++;
        testArray[index]();
    } else {
        finishTests();
    }
}

function terminateSpacesScanner(doFail) {
    $.ajax({
        type: "GET",
        url: "http://localhost:19000/terminate",
        crossDomain: true,
        dataType: "json",
        success: function (returnData) {
            console.log("terminate ok: " + JSON.stringify(returnData));
	    process.exit(doFail ? -1 : 0) // 0 exit code on success
        },
        error: function (data, textStatus, xhr) {
            console.log("terminate failed: " + data + " " + textStatus);
	    process.exit(-1) // nonzero exit code on failure
        }
    });
}

function finishTests() {
    console.log("\nSuccess: web API testing finished!");

    terminateSpacesScanner();
}

function failTests() {
    console.log("\nError: web API testing failed!");

    terminateSpacesScanner();
}

function logTest(testname)
{
    console.log("******************************");
    console.log("** Starting test " + testname);
    console.log("******************************");
}
