"use strict";
SPACESCANNER.settings = function() {

    var MAX_DISPLAY_PARAMS = 5;

    var defaultSettings = {
        "optimization" : {
            "timeLimitSec" : 10,
            "consensusDelaySec" : 10
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
        "named_parameters" : [
        ],
        "output" : {
            "loglevel" : 3
        },
        "web" : {
            "logxaxis" : false,
            "logyaxis" : false,
        }
    };

    // make a copy
    var currentSettings = JSON.parse(JSON.stringify(defaultSettings));

    var currentParams = [];

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
                } else {
                    var relativeError = getd(currentSettings["optimization"], "targetFractionOfTOP", 0.0);
                    // Update top state depending on whether enabled
                    updateTOPState(relativeError && relativeError !== 0.0);
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

    function stopAll() {
        $.ajax({
            url: "stopall",
            success: function (returnData) {
                SPACESCANNER.notify("Stopping all jobs");
            },
            error: function (data, textStatus, xhr) {
                SPACESCANNER.notify("Failed to stop jobs: " + JSON.stringify(data) + " " + textStatus, "error");
            }
        });
    }

    function factorial(n) {
        if (n < 2) {
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
                re = rs;
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

    function getNumOptimizableParams() {
        if (!currentParams) {
            currentParams = [];
        }
        var numParams = currentParams.length;
        var len = currentSettings["named_parameters"] ? currentSettings["named_parameters"].length : 0;
        for (var i = 0; i < len; ++i) {
            var p = currentSettings["named_parameters"][i];
            if (p.included === "always" || p.included === "never") {
                if(currentParams.indexOf(p.name) >= 0) {
                    numParams--;
                }
            }
        }
        return numParams >= 0 ? numParams : 0; // don't allow to be negative
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

        if(!SPACESCANNER.refresh) {
            $("#params-job-status").html("Estimated");
            $("#params-job-number").html("<i>unknown</i>");
            return;
        }
        var totalNumParams = getNumOptimizableParams();
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
        if ($( "#dialog-settings" ).is(':visible')) {
            if (enable) {
                $( "#input-option-enableTotalOptimization" ).prop("checked", true);
                $( "#input-option-targetFractionOfTOP" ).prop('disabled', false);
                $( "#input-option-bestOfValue" ).prop('disabled', false);
            } else {
                $( "#input-option-enableTotalOptimization" ).prop("checked", false);
                $( "#input-option-targetFractionOfTOP" ).prop('disabled', true);
                $( "#input-option-bestOfValue" ).prop('disabled', true);
            }
        }

        /* Set the global button state to the inverse of "enable" */
        if (enable) {
            $( "#button-parameters" ).addClass('disabled');
        } else {
            $( "#button-parameters" ).removeClass('disabled');
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

    function onTaskTypeChanged() {
        var taskType = $('input[name=input-import-taskType]:checked').val();
        if (taskType === "parameterFitting") {
            // enable multiple file upload
            $( "#input-import-filename" ).prop('multiple', true);
            $( "#input-import-filename" ).prop('directory', true);
            $( "#input-import-filename" ).prop('webkitdirectory', true);
            $( "#input-import-filename" ).prop('allowdirs', true);
        } else {
            // disable multiple file upload
            $( "#input-import-filename" ).removeProp('multiple');
            $( "#input-import-filename" ).removeProp('directory');
            $( "#input-import-filename" ).removeProp('webkitdirectory');
            $( "#input-import-filename" ).removeProp('allowdirs');
        }
    }

    function populateSettings() {
        // Task settings
        $( '#input-import-taskName' ).val(currentSettings["taskName"]);
        $( '#input-import-taskType' ).val(currentSettings["copasi"]["taskType"]);
        $( 'input[type=radio][name=input-import-taskType]' ).change(onTaskTypeChanged);
        // call this now to update the button class
        onTaskTypeChanged();

        // Performance settings
        $( "#input-option-runsPerJob" ).val(getd(currentSettings["optimization"], "runsPerJob", 4));
        $( "#input-option-maxConcurrentRuns" ).val(getd(currentSettings["optimization"], "maxConcurrentRuns", 4));
        $( "#input-option-timeLimit" ).val(getd(currentSettings["optimization"], "timeLimitSec", 3600));

        $( "#input-option-consensusDelaySec" ).val(getd(currentSettings["optimization"], "consensusDelaySec", 300));
        $( "#input-option-consensusProportionalDelay" ).val(
            toPercent(getd(currentSettings["optimization"], "consensusProportionalDelay", 0.15)));
        $( "#input-option-consensusCorridor" ).val(
            toPercent(getd(currentSettings["optimization"], "consensusCorridor", 0.01)));

        $( "#input-option-stagnationDelaySec" ).val(getd(currentSettings["optimization"], "stagnationDelaySec", 300));
        $( "#input-option-stagnationProportionalDelay" ).val(
            toPercent(getd(currentSettings["optimization"], "stagnationProportionalDelay", 0.15)));

        $( "#input-option-paramEstimationReferenceValueSec" ).val(getd(currentSettings["optimization"], "paramEstimationReferenceValueSec", 3.0));

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
        var relativeError = getd(currentSettings["optimization"], "targetFractionOfTOP", 0.0);

        if (relativeError && relativeError !== 0.0) {
            updateTOPState(true);
            $( "#input-option-targetFractionOfTOP" ).val(
                toPercent(getd(currentSettings["optimization"], "targetFractionOfTOP", 0.0)));
            $( "#input-option-bestOfValue" ).val(
                getd(currentSettings["optimization"], "bestOfValue", 0.0));
        } else {
            updateTOPState(false);
            $( "#input-option-targetFractionOfTOP" ).val("");
            $( "#input-option-bestOfValue" ).val("");
        }

        // Display settings
        $( "#input-option-logxaxis" ).prop("checked",
            getd(currentSettings["web"], "logxaxis", false));
        $( "#input-option-logyaxis" ).prop("checked",
            getd(currentSettings["web"], "logyaxis", false));

        // Other settings
        $( "#input-option-loglevel" ).val(
            getd(currentSettings["output"], "loglevel", 2));

        // Parameter settings
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
        // Task settings
        currentSettings["taskName"] = $( '#input-import-taskName' ).val();
        currentSettings["copasi"]["taskType"] = $('input[name=input-import-taskType]:checked').val();

        // Performance settings
        currentSettings["optimization"]["runsPerJob"] = parseInt($( "#input-option-runsPerJob" ).val());
        currentSettings["optimization"]["maxConcurrentRuns"] = parseInt($( "#input-option-maxConcurrentRuns" ).val());
        currentSettings["optimization"]["timeLimitSec"] = parseInt($( "#input-option-timeLimit" ).val());

        currentSettings["optimization"]["consensusDelaySec"] = parseInt($( "#input-option-consensusDelaySec" ).val());
        currentSettings["optimization"]["consensusProportionalDelay"] = $( "#input-option-consensusProportionalDelay" ).val() / 100.0;
        currentSettings["optimization"]["consensusCorridor"] = $( "#input-option-consensusCorridor" ).val() / 100.0;

        currentSettings["optimization"]["stagnationDelaySec"] = parseInt($( "#input-option-stagnationDelaySec" ).val());
        currentSettings["optimization"]["stagnationProportionalDelay"] = $( "#input-option-stagnationProportionalDelay" ).val() / 100.0;

        currentSettings["optimization"]["paramEstimationReferenceValueSec"] = $( "#input-option-paramEstimationReferenceValueSec" ).val() / 1.0;

        // Method settings
        currentSettings["copasi"]["methods"] = $( "#input-option-methods" ).val().split(",").map(function(x) { return x.trim() });
        currentSettings["copasi"]["fallbackMethods"] = $( "#input-option-fallbackMethods" ).val().split(",").map(function(x) { return x.trim() });

        currentSettings["copasi"]["randomizeMethodSelection"] = $( "#input-option-randomizeMethodSelection" ).is(":checked");
        currentSettings["copasi"]["methodParametersFromFile"] = $( "#input-option-methodParametersFromFile" ).is(":checked");
        currentSettings["optimization"]["restartFromBestValue"] = $( "#input-option-restartFromBestValue" ).is(":checked");

        // Total optimization settings
        if ($( "#input-option-enableTotalOptimization" ).is(":checked"))  {
            currentSettings["optimization"]["targetFractionOfTOP"] = $( "#input-option-targetFractionOfTOP" ).val() / 100.0;
        } else {
            currentSettings["optimization"]["targetFractionOfTOP"] = 0.0; // disables it
        }
        currentSettings["optimization"]["bestOfValue"] = parseInt($( "#input-option-bestOfValue" ).val());

        // display settings
        currentSettings["web"]["logxaxis"] = $( "#input-option-logxaxis" ).is(":checked");
        currentSettings["web"]["logyaxis"] = $( "#input-option-logyaxis" ).is(":checked");

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

            // always/never optimize parameters
            currentSettings["named_parameters"] = [];
            for (var i = 0; i < currentParams.length; ++i) {
                var paramIncluded = $('input[name=dialog-params-param-' + i + ']:checked').val();
                var p = {name: currentParams[i], included: paramIncluded};
                currentSettings["named_parameters"].push(p);
            }
        }

        if (currentSettings["optimization"]["targetFractionOfTOP"] != 0) {
            /* TOP enabled; set default params */
            currentSettings["parameters"] = [
                {"type" : "full-set"},
                {"type" : "exhaustive", "range" : [1, 1000]}
            ];
        }

        // in case graphical settings have changed
        SPACESCANNER.display.refresh();
    }

    updateTOPState(false); /* Unchecked by default */

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
        get : function(property) {
            return currentSettings[property]
        },
        set : function(property, value) {
            currentSettings[property] = value;
        },
        setParams : function(newParams) {
            console.log("setting new params: " + JSON.stringify(newParams));
            currentParams = newParams;
        },
        getParams : function() {
            return currentParams;
        },
        getParamIncluded : function(paramName) {
            var len = currentSettings["named_parameters"] ? currentSettings["named_parameters"].length : 0;
            for (var i = 0; i < len; ++i) {
                var p = currentSettings["named_parameters"][i];
                if(p.name === paramName) {
                    return p.included;
                }
            }
            return "contingent";
        },
        getNumNamedParams : function() {
            var settings;
            if ($( "#dialog-parameters" ).is(':visible')) {
                // populate from the dialog
                settings = {"named_parameters" : []};
                for (var i = 0; i < currentParams.length; ++i) {
                    var paramIncluded = $('input[name=dialog-params-param-' + i + ']:checked').val();
                    var p = {name: currentParams[i], included: paramIncluded};
                    settings["named_parameters"].push(p);
                }
            } else {
                // use cached settings
                settings = currentSettings;
            }
            var ret = {numAlways: 0, numNever: 0, numContingent: 0};
            var len = settings["named_parameters"] ? settings["named_parameters"].length : 0;
            for (var i = 0; i < len; ++i) {
                var p = settings["named_parameters"][i];
                if (p.included === "always") {
                    ret.numAlways++;
                } else if (p.included === "never") {
                    ret.numNever++;
                } else {
                    ret.numContingent++;
                }
            }
            return ret;
        },
        querySettings : querySettings,
        postSettings : postSettings,
        stopAll : stopAll,
        populateSettings : populateSettings,
        saveSettings : saveSettings,  
        displayParam : displayParam,
        estimateNumJobs : estimateNumJobs,
    }
}();
