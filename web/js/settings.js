"use strict";
CORUNNER.settings = function() {

    var defaultSettings = {
        "optimization" : {
            "timeLimitSec" : 10,
            "consensusMinDurationSec" : 10
        },
        "copasi" : {
            "modelFile" : "@SELF@/tmpweb/model.cps",
            "methods" : ["ParticleSwarm"],
            "fallbackMethods" : ["GeneticAlgorithmSR"]
        },
        "parameters" : [
            {"type" : "exhaustive", "range" : [1, 2]},
            {"type" : "greedy", "range" : [3, 4]}
        ],
        "output" : {
            "loglevel" : 3
        },
        "webTestMode" : true,
        "testMode" : true
    };

    // make a copy
    var currentSettings = JSON.parse(JSON.stringify(defaultSettings));

    // read from the server
    function querySettings() {
        $.ajax({
            type: "GET",
            url: "config",
            dataType: "json",
            success: function (returnData) {
                console.log("got config ok");
                currentSettings = returnData;
                if ($( "#dialog-settings" ).is(':visible')) {
                    populateSettings();
                }
            },
            error: function (data, textStatus, xhr) {
                console.log("get config error: " + JSON.stringify(data) + " " + textStatus);
            }
        });
    }

    function postSettings() {
        $.ajax({
            type: "POST",
            url: "start",
            data: JSON.stringify(currentSettings),
            contentType: "application/json",
            dataType: "json",
            success: function (returnData) {
                CORUNNER.notify("Jobs started", "success");
                console.log("start command: " + JSON.stringify(returnData));
            },
            error: function (data, textStatus, xhr) {
                CORUNNER.notify("Failed to start jobs: " + JSON.stringify(data) + " " + textStatus, "error");
            }
        });
    }

    function getd(obj, property, def) {
        return obj.hasOwnProperty(property) ? obj[property] : def;
    }

    function populateSettings() {
        $( "#input-option-runsPerJob" ).val(getd(currentSettings["optimization"], "runsPerJob", 4));
        $( "#input-option-timeLimit" ).val(getd(currentSettings["optimization"], "timeLimitSec", 3600));

        $( "#input-option-consensusMinDurationSec" ).val(getd(currentSettings["optimization"], "consensusMinDurationSec", 300));
        $( "#input-option-consensusMinProportionalDuration" ).val(
            Math.round(1000 * getd(currentSettings["optimization"], "consensusMinProportionalDuration", 0.15)) / 10.0);
        $( "#input-option-consensusRelativeError" ).val(
            Math.round(1000 * getd(currentSettings["optimization"], "consensusRelativeError", 0.01)) / 10.0);

        $( "#input-option-methods" ).val(
            getd(currentSettings["copasi"], "methods", []).join());
        $( "#input-option-fallbackMethods" ).val(
            getd(currentSettings["copasi"], "fallbackMethods", []).join());
        $( "#input-option-randomizeMethodSelection" ).prop("checked",
            getd(currentSettings["copasi"], "randomizeMethodSelection", false));
        $( "#input-option-restartFromBestValue" ).prop("checked",
            getd(currentSettings["optimization"], "restartFromBestValue", true));

        $( "#input-option-loglevel" ).val(
            getd(currentSettings["output"], "loglevel", 2));
    }

    function saveSettings() {
        currentSettings["optimization"]["runsPerJob"] = parseInt($( "#input-option-runsPerJob" ).val());
        currentSettings["optimization"]["timeLimitSec"] = parseInt($( "#input-option-timeLimit" ).val());

        currentSettings["optimization"]["consensusMinDurationSec"] = parseInt($( "#input-option-consensusMinDurationSec" ).val());
        currentSettings["optimization"]["consensusMinProportionalDuration"] = $( "#input-option-consensusMinProportionalDuration" ).val() / 100.0;
        currentSettings["optimization"]["consensusRelativeError"] = $( "#input-option-consensusRelativeError" ).val() / 100.0;

        currentSettings["copasi"]["methods"] = $( "#input-option-methods" ).val().split(",").map(function(x) { return x.trim() });
        currentSettings["copasi"]["fallbackMethods"] = $( "#input-option-fallbackMethods" ).val().split(",").map(function(x) { return x.trim() });

        currentSettings["copasi"]["randomizeMethodSelection"] = $( "#input-option-randomizeMethodSelection" ).is(":checked");
        currentSettings["optimization"]["restartFromBestValue"] = $( "#input-option-restartFromBestValue" ).is(":checked");

        currentSettings["output"]["loglevel"] = $( "#input-option-loglevel" ).val();
    }

    setTimeout(querySettings, 1000);

    return {
        get : function(property) { return currentSettings[property] },
        set : function(property, value) {
            currentSettings[property] = value;
        },
        querySettings : querySettings,
        postSettings : postSettings,
        populateSettings : populateSettings,
        saveSettings : saveSettings
    }
}();
