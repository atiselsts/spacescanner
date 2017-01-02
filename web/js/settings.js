"use strict";
SPACESCANNER.settings = function() {

    var MAX_DISPLAY_PARAMS = 5;

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
        // Always use the same model file - the one POSTed from the web
        currentSettings["copasi"]["modelFile"] = "@SELF@/tmpweb/model.cps";

        $.ajax({
            type: "POST",
            url: "start",
            data: JSON.stringify(currentSettings),
            contentType: "application/json",
            dataType: "json",
            success: function (returnData) {
                SPACESCANNER.notify("" + returnData.totalNumJobs + " jobs queued", "success");
                console.log("start command: " + JSON.stringify(returnData));
            },
            error: function (data, textStatus, xhr) {
                SPACESCANNER.notify("Failed to start jobs: " + JSON.stringify(data) + " " + textStatus, "error");
            }
        });
    }

    function factorial(n) {
        if (n == 0 || n == 1) {
            return 1;
        }
        return factorial(n - 1) * n;
    }

    function estimateNumJobsPerSet(paramIndex, totalNumParams) {
        var type = $("#input-option-params" + paramIndex).val();
        if (type === "zero" || type === "full-set" || type === "explicit") {
            return 1;
        }

        var rs = parseInt($( "#input-option-param" + paramIndex + "-rangeStart" ).val());
        var re = parseInt($( "#input-option-param" + paramIndex + "-rangeEnd" ).val());
        if (!(rs > 0)) {
            rs = 1;
        }
        if (type === "greedy" || type === "exhaustive") {
            if (re > totalNumParams) {
                re = totalNumParams;
            }
            if (rs > re) {
                rs = re;
            }
        } else if (type === "greedy-reverse") {
            if (rs > totalNumParams) {
                rs = totalNumParams;
            }
            if (re > rs) {
                rs = re;
            }
        }

        var result = 0;
        if (type === "exhaustive") {
            var nf = factorial(totalNumParams);
            for (var i = rs; i <= re; ++i) {
                result += nf / (factorial(i) * factorial(totalNumParams - i));
            }
        }
        if (type === "greedy") {
            for (var i = rs; i <= re; ++i) {
                result += i;
            }
        }
        if (type === "greedy-reverse") {
            for (var i = rs; i >= re; --i) {
                result += i;
            }
        }
        return result;
    }
            
    function estimateNumJobs() {
        if (!$( "#dialog-parameters" ).is(':visible')) {
            return;
        }
        if($('#button-start-stop').hasClass('disabled')) {
            $( "#params-count-row-enabled" ).hide();
            $( "#params-count-row-disabled" ).show();
            return;
        }
        $( "#params-count-row-disabled" ).hide();
        $( "#params-count-row-enabled" ).show();

        var totalNumParams = SPACESCANNER.refresh ? SPACESCANNER.refresh.totalNumParams() : 0;
        if(!totalNumParams) {
            $("#params-job-status").html("Estimated");
            $("#params-job-number").html("<i>unknown</i>");
            return;
        }
        var totalNumJobs = 0;
        var parameters = [];
        for (var i = 0; i < MAX_DISPLAY_PARAMS; ++i) {
            // only if (1) visible and (2) the selected type is not "none"
            if ($( "#row-params" + i ).is(':visible')) {
                totalNumJobs += estimateNumJobsPerSet(i, totalNumParams);
            }
        }
        $("#params-job-status").html("Estimated");
        $("#params-job-number").html("" + totalNumJobs);
    }

    for (var i = 0; i < MAX_DISPLAY_PARAMS; ++i) {
        $("#input-option-params" + i).change(estimateNumJobs);
        $("#input-option-param" + i + "-rangeStart").change(estimateNumJobs);
        $("#input-option-param" + i + "-rangeEnd").change(estimateNumJobs);
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

    function toPercent(x) {
        if (typeof(x) !== 'number') {
            return null;
        }
        /* percent, including decimal parts */
        return Math.round(x * 1000.0) / 10.0;
    }

    function changeParam(element, i) {
        var type = element.val();
        var doRanges = false;
        var doNames = false;

        if (type === "none") {
            $( "#row-params" + i ).hide();
        } else {
            $( "#row-params" + i ).show();

            if (type === "exhaustive") {
                doRanges = true;
            } else if (type === "greedy" || type === "greedy-reverse") {
                doRanges = true;
            } else if (type === "explicit") {
                doNames = true;
            }
        }

        if (doRanges) {
            $( "#params" + i + "-ranges" ).show();
        } else {
            $( "#params" + i + "-ranges" ).hide();
        }
        if (doNames) {
            $( "#params" + i + "-names" ).show();
        } else {
            $( "#params" + i + "-names" ).hide();
        }
    }

    function displayParam(parameter, i) {
        var type = parameter === null ? "none" : parameter.type;
        var paramField = $( "#input-option-params" + i );
        paramField.val(type).change(function () { changeParam(paramField, i) })
        changeParam(paramField, i);

        if (type === "exhaustive" || type === "greedy" || type === "greedy-reverse") {
            if (parameter.range && parameter.range.length > 0) {
                var rs = parameter.range[0];
                var re = parameter.range.length > 1 ? parameter.range[1] : rs;
                $( "#input-option-param" + i + "-rangeStart" ).val(rs);
                $( "#input-option-param" + i + "-rangeEnd" ).val(re);
            } else {
                $( "#input-option-param" + i + "-rangeStart" ).val("");
                $( "#input-option-param" + i + "-rangeEnd" ).val("");
            }
        } else if (type === "explicit") {
            var names = parameter.parameters;
            if (!names) names = [];
            $( "#input-option-param" + i + "-params" ).val(names.join());
        }
    }

    function constructParam(type, i) {
        var result = {type : type};

        var rs = parseInt($( "#input-option-param" + i + "-rangeStart" ).val());
        var re = parseInt($( "#input-option-param" + i + "-rangeEnd" ).val());
        if (!(rs > 0)) {
            if (type === "greedy" || type === "greedy-reverse" || type === "exhaustive") {
                /* Issue this warning only when there's a valid cause for this */
                SPACESCANNER.notify("Range start may not be less than 1", "error");
            }
            rs = 1;
        }
        if (type === "greedy" || type === "exhaustive") {
            if (rs > re) {
                SPACESCANNER.notify("For type " + type + " range end may not be less than range start", "error");
                rs = re;
            }
        } else if (type === "greedy-reverse") {
            if (re > rs) {
                SPACESCANNER.notify("For type " + type + " range start may not be less than range end", "error");
                rs = re;
            }
        }
        var names = $( "#input-option-param" + i + "-params" ).val().split(",").map(function(x) { return x.trim() });

        if (type === "full-set") {
        } else if (type === "exhaustive") {
            result.range = [rs, re];
        } else if (type === "greedy" || type === "greedy-reverse") {
            result.range = [rs, re];
        } else if (type === "explicit") {
            result.parameters = names;
        }
        return result;
    }

    function populateSettings() {
  // Performance settings
        $( "#input-option-runsPerJob" ).val(getd(currentSettings["optimization"], "runsPerJob", 4));
        $( "#input-option-maxConcurrentRuns" ).val(getd(currentSettings["optimization"], "maxConcurrentRuns", 4));
        $( "#input-option-timeLimit" ).val(getd(currentSettings["optimization"], "timeLimitSec", 3600));

        $( "#input-option-consensusMinDurationSec" ).val(getd(currentSettings["optimization"], "consensusMinDurationSec", 300));
        $( "#input-option-consensusMinProportionalDuration" ).val(
            toPercent(getd(currentSettings["optimization"], "consensusMinProportionalDuration", 0.15)));
        $( "#input-option-consensusRelativeError" ).val(
            toPercent(getd(currentSettings["optimization"], "consensusRelativeError", 0.01)));

        $( "#input-option-stagnationMaxDurationSec" ).val(getd(currentSettings["optimization"], "stagnationMaxDurationSec", 300));
        $( "#input-option-stagnationMaxProportionalDuration" ).val(
            toPercent(getd(currentSettings["optimization"], "stagnationMaxProportionalDuration", 0.15)));

  // Method settings  
        $( "#input-option-methods" ).val(
            getd(currentSettings["copasi"], "methods", []).join());
        $( "#input-option-fallbackMethods" ).val(
            getd(currentSettings["copasi"], "fallbackMethods", []).join());
        $( "#input-option-randomizeMethodSelection" ).prop("checked",
            getd(currentSettings["copasi"], "randomizeMethodSelection", false));
        $( "#input-option-methodParametersFromFile" ).prop("checked",
            getd(currentSettings["copasi"], "methodParametersFromFile", false));
        $( "#input-option-restartFromBestValue" ).prop("checked",
            getd(currentSettings["optimization"], "restartFromBestValue", true));

        // Total optimization settings
        var relativeError = getd(currentSettings["optimization"], "optimalityRelativeError", 0.0);

        if (relativeError && relativeError !== 0.0) {
            updateTOPState(true);
            $( "#input-option-optimalityRelativeError" ).val(
                toPercent(getd(currentSettings["optimization"], "optimalityRelativeError", 0.0)));
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

        // parameter settings
        var parameters = currentSettings["parameters"];
        for (var i = 0; i < MAX_DISPLAY_PARAMS; ++i) {
            if (i < parameters.length) {
                displayParam(parameters[i], i);
            } else {
                displayParam(null, i);
            }
        }
    }

    function saveSettings() {
        // Performance settings
        currentSettings["optimization"]["runsPerJob"] = parseInt($( "#input-option-runsPerJob" ).val());
        currentSettings["optimization"]["maxConcurrentRuns"] = parseInt($( "#input-option-maxConcurrentRuns" ).val());
        currentSettings["optimization"]["timeLimitSec"] = parseInt($( "#input-option-timeLimit" ).val());

        currentSettings["optimization"]["consensusMinDurationSec"] = parseInt($( "#input-option-consensusMinDurationSec" ).val());
        currentSettings["optimization"]["consensusMinProportionalDuration"] = $( "#input-option-consensusMinProportionalDuration" ).val() / 100.0;
        currentSettings["optimization"]["consensusRelativeError"] = $( "#input-option-consensusRelativeError" ).val() / 100.0;

  currentSettings["optimization"]["stagnationMaxDurationSec"] = parseInt($( "#input-option-stagnationMaxDurationSec" ).val());
        currentSettings["optimization"]["stagnationMaxProportionalDuration"] = $( "#input-option-stagnationMaxProportionalDuration" ).val() / 100.0;

        // Method settings
        currentSettings["copasi"]["methods"] = $( "#input-option-methods" ).val().split(",").map(function(x) { return x.trim() });
        currentSettings["copasi"]["fallbackMethods"] = $( "#input-option-fallbackMethods" ).val().split(",").map(function(x) { return x.trim() });

        currentSettings["copasi"]["randomizeMethodSelection"] = $( "#input-option-randomizeMethodSelection" ).is(":checked");
        currentSettings["copasi"]["methodParametersFromFile"] = $( "#input-option-methodParametersFromFile" ).is(":checked");
        currentSettings["optimization"]["restartFromBestValue"] = $( "#input-option-restartFromBestValue" ).is(":checked");

        // Total optimization settings
        if ($( "#input-option-enableTotalOptimization" ).is(":checked"))  {
            currentSettings["optimization"]["optimalityRelativeError"] = $( "#input-option-optimalityRelativeError" ).val() / 100.0;
        } else {
            currentSettings["optimization"]["optimalityRelativeError"] = 0.0; // disables it
        }
        currentSettings["optimization"]["bestOfValue"] = parseInt($( "#input-option-bestOfValue" ).val());

        // other settings
        currentSettings["output"]["loglevel"] = $( "#input-option-loglevel" ).val();

        if ($( "#dialog-parameters" ).is(':visible')) {
            // parameter settings
            var parameters = [];
            for (var i = 0; i < MAX_DISPLAY_PARAMS; ++i) {
                // only if (1) visible and (2) the selected type is not "none"
                if ($( "#row-params" + i ).is(':visible')) {
                    var type = $( "#input-option-params" + i ).val();
                    if (type !== "none") {
                        parameters.push(constructParam(type, i));
                    }
                }
            }
            currentSettings["parameters"] = parameters;
        }
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
        saveSettings : saveSettings,  
        displayParam : displayParam,
        estimateNumJobs : estimateNumJobs,
    }
}();
