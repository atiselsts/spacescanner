"use strict";
SPACESCANNER.settings = function() {

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
                SPACESCANNER.notify("Jobs started", "success");
                console.log("start command: " + JSON.stringify(returnData));
            },
            error: function (data, textStatus, xhr) {
                SPACESCANNER.notify("Failed to start jobs: " + JSON.stringify(data) + " " + textStatus, "error");
            }
        });
    }

    function getd(obj, property, def) {
        return obj.hasOwnProperty(property) ? obj[property] : def;
    }

    function updateTOPState(enable) {
	if (enable) {
            $( "#input-option-enableTotalOptimization" ).prop("checked", true);
	    $( "#input-option-optimalityRelativeError" ).prop('disabled', false);
	    $( "#input-option-bestOfValue" ).prop('disabled', false);
	} else {
            $( "#input-option-enableTotalOptimization" ).prop("checked", false);
	    $( "#input-option-optimalityRelativeError" ).prop('disabled', true);
	    $( "#input-option-bestOfValue" ).prop('disabled', true);
	}
    }

    function populateSettings() {
	// Performance settings
        $( "#input-option-runsPerJob" ).val(getd(currentSettings["optimization"], "runsPerJob", 4));
        $( "#input-option-maxConcurrentRuns" ).val(getd(currentSettings["optimization"], "maxConcurrentRuns", 4));
        $( "#input-option-timeLimit" ).val(getd(currentSettings["optimization"], "timeLimitSec", 3600));

        $( "#input-option-consensusMinDurationSec" ).val(getd(currentSettings["optimization"], "consensusMinDurationSec", 300));
        $( "#input-option-consensusMinProportionalDuration" ).val(
            Math.round(1000 * getd(currentSettings["optimization"], "consensusMinProportionalDuration", 0.15)) / 10.0);
        $( "#input-option-consensusRelativeError" ).val(
            Math.round(1000 * getd(currentSettings["optimization"], "consensusRelativeError", 0.01)) / 10.0);

	// Method settings	
        $( "#input-option-methods" ).val(
            getd(currentSettings["copasi"], "methods", []).join());
        $( "#input-option-fallbackMethods" ).val(
            getd(currentSettings["copasi"], "fallbackMethods", []).join());
        $( "#input-option-randomizeMethodSelection" ).prop("checked",
            getd(currentSettings["copasi"], "randomizeMethodSelection", false));
        $( "#input-option-restartFromBestValue" ).prop("checked",
            getd(currentSettings["optimization"], "restartFromBestValue", true));

	// Total optimization settings
	var relativeError = getd(currentSettings["optimization"], "optimalityRelativeError", 0.0);

	if (relativeError && relativeError !== 0.0) {
	    updateTOPState(true);
            $( "#input-option-optimalityRelativeError" ).val(
		Math.round(10000 * getd(currentSettings["optimization"], "optimalityRelativeError", 0.0)) / 100.0);
            $( "#input-option-bestOfValue" ).val(
		getd(currentSettings["optimization"], "bestOfValue", 0.0));
	} else {
	    updateTOPState(false);
            $( "#input-option-optimalityRelativeError" ).val("");
            $( "#input-option-bestOfValue" ).val("");
	}

	// other settings
        $( "#input-option-loglevel" ).val(
            getd(currentSettings["output"], "loglevel", 2));
    }

    function saveSettings() {
	// Performance settings
        currentSettings["optimization"]["runsPerJob"] = parseInt($( "#input-option-runsPerJob" ).val());
        currentSettings["optimization"]["maxConcurrentRuns"] = parseInt($( "#input-option-maxConcurrentRuns" ).val());
        currentSettings["optimization"]["timeLimitSec"] = parseInt($( "#input-option-timeLimit" ).val());

        currentSettings["optimization"]["consensusMinDurationSec"] = parseInt($( "#input-option-consensusMinDurationSec" ).val());
        currentSettings["optimization"]["consensusMinProportionalDuration"] = $( "#input-option-consensusMinProportionalDuration" ).val() / 100.0;
        currentSettings["optimization"]["consensusRelativeError"] = $( "#input-option-consensusRelativeError" ).val() / 100.0;

	// Method settings
        currentSettings["copasi"]["methods"] = $( "#input-option-methods" ).val().split(",").map(function(x) { return x.trim() });
        currentSettings["copasi"]["fallbackMethods"] = $( "#input-option-fallbackMethods" ).val().split(",").map(function(x) { return x.trim() });

        currentSettings["copasi"]["randomizeMethodSelection"] = $( "#input-option-randomizeMethodSelection" ).is(":checked");
        currentSettings["optimization"]["restartFromBestValue"] = $( "#input-option-restartFromBestValue" ).is(":checked");

	// Always use the same model file - the one POSTed from the web
	currentSettings["copasi"]["modelFile"] = "@SELF@/tmpweb/model.cps";

	// Total optimization settings
	if ($( "#input-option-enableTotalOptimization" ).is(":checked"))  {
            currentSettings["optimization"]["optimalityRelativeError"] = $( "#input-option-optimalityRelativeError" ).val() / 100.0;
	} else {
	    currentSettings["optimization"]["optimalityRelativeError"] = 0.0; // disbales it
	}
        currentSettings["optimization"]["bestOfValue"] = parseInt($( "#input-option-bestOfValue" ).val());

	// other settings
        currentSettings["output"]["loglevel"] = $( "#input-option-loglevel" ).val();
    }

    $( "#input-option-enableTotalOptimization" ).on("click", function() {
	updateTOPState($( this ).is(":checked"));
    });

    setTimeout(querySettings, 1000);

    // enable tab functionality in the "settings" dialog
    $('.dialog-tab-label').on('click', function(e)  {
        var currentAttrValue = $(this).attr('href');
        $('.dialog-tabs ' + currentAttrValue).show().siblings().hide();
        $(this).parent('li').addClass('active').siblings().removeClass('active');
        e.preventDefault();
    });

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
