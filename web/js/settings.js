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
   
    function getSettings() {
	var settings = JSON.parse(JSON.stringify(defaultSettings));
	settings["taskName"] = $( "#input-import-taskname" ).val();
	return settings;
    }

    function postSettings() {
	$.ajax({
	    type: "POST",
	    url: "start",
	    data: JSON.stringify(getSettings()),
	    contentType: "application/json",
	    dataType: "json",
	    crossDomain: true,
	    success: function (returnData) {
		console.log("start command: " + JSON.stringify(returnData));
	    },
	    error: function (data, textStatus, xhr) {
		console.log("post config file: error: " + JSON.stringify(data) + " " + textStatus);
	    }
	});
    }

    return {
	getSettings : getSettings,
	postSettings : postSettings,
    }
}();
