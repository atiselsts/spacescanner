"use strict";
var SPACESCANNER = function() {

    var MAX_DISPLAY_JOBS = 8;
    var MAX_DISPLAY_PARAMS = 5;

    $( "#dialog-select-model" ).dialog({
        title: "Select a model",
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
        height: 600,
        open: function() {
            //SPACESCANNER.settings.querySettings();
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

    function delParams() {
	var id = $( this ).attr("id");
        var index = parseInt(id.substr(17));
	SPACESCANNER.settings.displayParam(null, index);
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
	    SPACESCANNER.settings.displayParam({type: "exhaustive", range: [1, 1]}, found);
	} else {
            SPACESCANNER.notify("Max " + MAX_DISPLAY_PARAMS + " different parameter sets");
	}
    });

    $( "#dialog-parameters" ).dialog({
        title: "Adjustable parameter sets to search through",
        modal: true,
        autoOpen: false,
        width: 880,
        height: 400,
        open: function() {
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
