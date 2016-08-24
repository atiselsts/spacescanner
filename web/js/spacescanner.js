"use strict";
var SPACESCANNER = function() {

    var MAX_DISPLAY_JOBS = 8;
    var MAX_DISPLAY_PARAMS = 5;

    $( "#dialog-select-model" ).dialog({
        title: "Select model",
        modal: true,
        autoOpen: false,
        width: 600,
        height: 230,
        open: function() {
            $( '#input-import-taskName' ).val(SPACESCANNER.settings.get("taskName"));
        },
    });

    $('#dialog-select-model').fileUpload({
        success: function (data, textStatus, jqXHR) {
            var filename = $( '#input-import-filename' ).val();
            SPACESCANNER.notify("Model file selected:\n" + filename, "success");
            $( "#dialog-select-model" ).dialog("close");
            $( 'title' ).text("Model file '" + filename + "'");
            SPACESCANNER.settings.set("taskName", $( '#input-import-taskName' ).val());
        },
        error: function (data, textStatus, err) {
            SPACESCANNER.notify("Failed to use the model file: " + JSON.stringify(data), "error");
        },
        action: "model"
    });

    $('#button-upload-model')
        .on("click",function(e) {
            var filename = $( '#input-import-filename' ).val();
            if (!filename || filename.length == 0) {
                e.preventDefault();
                SPACESCANNER.notify("Model file not specified", "error");
            }
        });


    $( "#dialog-status" ).dialog({
        title: "Job status",
        modal: true,
        autoOpen: false,
        width: 600,
        height: $(window).height() * 0.8,
        open: function() {
            console.log("status dlg opened")
        },
        close: function() {
            console.log("status dlg closed")
        },
        buttons: [
            {
                text: "Close",
                click: function() {
                    $( this ).dialog( "close" );
                }
            }
        ]
    });

    $( "#dialog-settings" ).dialog({
        title: "Optimization settings",
        modal: true,
        autoOpen: false,
        width: 740,
        height: 580,
        open: function() {
            SPACESCANNER.settings.querySettings();
            SPACESCANNER.settings.populateSettings();
        },
        buttons: [
            {
                text: "Ok",
                click: function() {
                    SPACESCANNER.settings.saveSettings();
                    $( this ).dialog( "close" );
                }
            },
            {
                text: "Cancel",
                click: function() {
                    $( this ).dialog( "close" );
                }
            }
        ]
    });

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
            } else if (type === "zero") {
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
            SPACESCANNER.notify("Range start may not be less than 1", "error");
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

        if (type === "all") {
        } else if (type === "exhaustive") {
            result.range = [rs, re];
        } else if (type === "greedy" || type === "greedy-reverse") {
            result.range = [rs, re];
        } else if (type === "explicit") {
            result.parameters = names;
        } else if (type === "zero") {
        }
        return result;
    }

    function delParams() {
	var id = $( this ).attr("id");
        var index = parseInt(id.substr(17));
	displayParam(null, index);
    }
    for (var i = 1; i < MAX_DISPLAY_PARAMS; ++i) {
	$("#button-del-params" + i).click(delParams);
    }

    $("#button-add-params").click(function(){
	var found = -1;
	for (var i = 0; i < MAX_DISPLAY_PARAMS; ++i) {
	    if (!$( "#row-params" + i ).is(':visible')) {
		found = i;
		break;
	    }
	}
	if (found != -1) {
	    displayParam({type: "exhaustive", range: [1, 1]}, found);
	} else {
            SPACESCANNER.notify("Max " + MAX_DISPLAY_PARAMS + " different parameter sets");
	}
    });

    $( "#dialog-parameters" ).dialog({
        title: "Parameter sets to search through",
        modal: true,
        autoOpen: false,
        width: 880,
        height: 400,
        open: function() {
            var parameters = SPACESCANNER.settings.get("parameters");
            for (var i = 0; i < MAX_DISPLAY_PARAMS; ++i) {
		if (i < parameters.length) {
                    displayParam(parameters[i], i);
		} else {
                    displayParam(null, i);
		}
            }
        },
        buttons: [
            {
                text: "Ok",
                click: function() {
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
                    SPACESCANNER.settings.set("parameters", parameters);
                    $( this ).dialog( "close" );
                }
            },
            {
                text: "Cancel",
                click: function() {
                    $( this ).dialog( "close" );
                }
            }
        ]
    });

    $( "#dialog-export" ).dialog({
        title: "Export to CSV",
        modal: true,
        autoOpen: false,
        width: 600,
        height: 320,
        open: function() {
            console.log("export dlg opened")
        },
        close: function() {
            console.log("export dlg closed")
        },
        buttons: [
            {
                text: "Export",
                click: function() {
                    window.open(window.location + "results.csv");
                    $( this ).dialog( "close" );
                }
            },
            {
                text: "Cancel",
                click: function() {
                    $( this ).dialog( "close" );
                }
            }
        ]
    });

    $('#button-select').click(function(){
        if (!$( this ).hasClass('disabled')) {
            $( "#dialog-select-model" ).dialog( "open" )
        }
    });

    $('#button-start-stop').click(function(){
        if (!$( this ).hasClass('disabled')) {
            if (!SPACESCANNER.refresh.isActive()) {
                // start
		SPACESCANNER.settings.populateSettings();
		SPACESCANNER.settings.saveSettings();
                SPACESCANNER.settings.postSettings();
            } else { 
                // stop
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
        }
    });

    for (var i = 0; i < MAX_DISPLAY_JOBS; ++i) {
        $('#button-stop-job' + i).click(function(){
            var sindex = $( this ).attr("id")
            var index = parseInt(sindex.substr(15));
            var job = SPACESCANNER.display.getJobID(index);
            if (job) {
                $.ajax({
                    url: "stop/" + job,
                    success: function (returnData) {
                        SPACESCANNER.notify("Stopping job " + job);
                    },
                    error: function (data, textStatus, xhr) {
                        SPACESCANNER.notify("Failed to stop job " + job + ": " + JSON.stringify(data) + " " + textStatus, "error");
                    }
                });
            }
        });
    }

    $('#button-status').click(function(){
        if (!$( this ).hasClass('disabled')) {
            $( "#dialog-status" ).dialog( "open" );
            SPACESCANNER.refresh.refreshFull();
        }
    });

    $('#button-settings').click(function(){
        if (!$( this ).hasClass('disabled')) {
            $( "#dialog-settings" ).dialog( "open" )
        }
    });

    $('#button-parameters').click(function(){
        $( "#dialog-parameters" ).dialog( "open" )
    });

    $('#button-export').click(function(){
        if (!$( this ).hasClass('disabled')) {
            $( "#dialog-export" ).dialog( "open" )
        }
    });

    $(function() {
        console.log("loading spacescanner web interface...")
    });

    return {
    }
}();
