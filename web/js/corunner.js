"use strict";
var CORUNNER = function() {

    var serverUrl = "http://localhost:19000/"

    $( "#dialog-select-model" ).dialog({
        title: "Select a model",
        modal: true,
        autoOpen: false,
        width: 600,
        height: 260,
        open: function() {
            console.log("model dlg opened")
        },
        close: function() {
            console.log("model dlg closed")
        }
    });

    $('#dialog-select-model').fileUpload({
        success: function (data, textStatus, jqXHR) {
            CORUNNER.notify("Model file selected: " + JSON.stringify(data), "success");
	    $( "#dialog-select-model" ).dialog("close");
        },
        error: function (data, textStatus, err) {
            CORUNNER.notify("Failed to use the model file: " + JSON.stringify(data), "error");
        },
	action: "model"
    });

    $('#button-upload-model')
        .on("click",function(e) {
            var filename = $( '#input-import-filename' ).val();
            if (!filename || filename.length == 0) {
                e.preventDefault();
                CORUNNER.notify("Model file is not selected!", "error");
            }
        });


    $( "#dialog-status" ).dialog({
        title: "Job status",
        modal: true,
        autoOpen: false,
        width: 600,
        height: $(window).height() * 0.8,
        open: function() {
            console.log("model dlg opened")
        },
        close: function() {
            console.log("model dlg closed")
        },
        buttons: [
            {
                text: "Ok",
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
        width: 600,
        height: 400,
        open: function() {
            console.log("settings dlg opened")
        },
        close: function() {
            console.log("settings dlg closed")
        },
        buttons: [
            {
                text: "Ok",
                click: function() {
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


    $( "#dialog-parameters" ).dialog({
        title: "Parameter ranges to include in optimization",
        modal: true,
        autoOpen: false,
        width: 600,
        height: 400,
        open: function() {
            console.log("param dlg opened")
        },
        close: function() {
            console.log("param dlg closed")
        },
        buttons: [
            {
                text: "Ok",
                click: function() {
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
        height: 250,
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
		    window.open(window.location + "results");
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

/*    function showHelp() {
        console.log("show help")
//        $("#btn-icn-sim").removeClass('icon-play').addClass('icon-pause');

        $( "#dialog-comm-options" ).dialog( "open" ) }
    } */

    $('#button-select').click(function(){
        if (!$( this ).hasClass('disabled')) {
            $( "#dialog-select-model" ).dialog( "open" )
        }
    });

    $('#button-start-stop').click(function(){
        if (!$( this ).hasClass('disabled')) {
	    if (!CORUNNER.refresh.isActive()) {
		// start
		CORUNNER.settings.postSettings();
	    } else { 
		// stop
		$.ajax({
		    url: "stopall",
		    success: function (returnData) {
			console.log("stopall ok: " + JSON.stringify(returnData));
		    },
		    error: function (data, textStatus, xhr) {
			console.log("stopall failed, error: " + JSON.stringify(data) + " " + textStatus);
		    }
		});
	    }
        }
    });

    $('#button-status').click(function(){
        if (!$( this ).hasClass('disabled')) {
            $( "#dialog-status" ).dialog( "open" );
            CORUNNER.refresh.refreshFull();
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
        console.log("loading corunner...")
    });

    return {
	serverUrl : function() { return serverUrl }
    }
}();
