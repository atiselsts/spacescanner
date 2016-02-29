"use strict";
var CORUNNER = function() {

    $( "#dialog-select-model" ).dialog({
        title: "Select a model",
        modal: true,
        autoOpen: false,
        width: 600,
        height: 230,
        open: function() {
            $( '#input-import-taskName' ).val(CORUNNER.settings.get("taskName"));
        },
    });

    $('#dialog-select-model').fileUpload({
        success: function (data, textStatus, jqXHR) {
            var filename = $( '#input-import-filename' ).val();
            CORUNNER.notify("Model file selected:\n" + filename, "success");
            $( "#dialog-select-model" ).dialog("close");
            $( 'title' ).text("Model file '" + filename + "'");
            CORUNNER.settings.set("taskName", $( '#input-import-taskName' ).val());
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
                CORUNNER.notify("Model file not specified", "error");
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
        width: 640,
        height: 750,
        open: function() {
            CORUNNER.settings.querySettings();
            CORUNNER.settings.populateSettings();
        },
        buttons: [
            {
                text: "Ok",
                click: function() {
                    CORUNNER.settings.saveSettings();
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
        } else if (type === "all") {
        } else if (type === "exhaustive") {
            doRanges = true;
        } else if (type === "greedy") {
            doRanges = true;
        } else if (type === "explicit") {
            doNames = true;
        } else if (type === "zero") {
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

    function displayParam(parameters, i) {
        var type = i < parameters.length ? parameters[i].type : "none";
        var paramField = $( "#input-option-params" + i );
        paramField.val(type).change(function () { changeParam(paramField, i) })
        changeParam(paramField, i);

        if (type === "exhaustive" || type === "greedy") {
            if (parameters[i].range && parameters[i].range.length > 0) {
                var rs = parameters[i].range[0];
                var re = parameters[i].range.length > 1 ? parameters[i].range[1] : rs;
                $( "#input-option-param" + i + "-rangeStart" ).val(rs);
                $( "#input-option-param" + i + "-rangeEnd" ).val(re);
            } else {
                $( "#input-option-param" + i + "-rangeStart" ).val("");
                $( "#input-option-param" + i + "-rangeEnd" ).val("");
            }
        } else if (type === "explicit") {
            var names = parameters[i].parameters;
            if (!names) names = [];
            $( "#input-option-param" + i + "-params" ).val(names.join());
        }
    }

    function constructParam(type, i) {
        var result = {type : type};
        
        var rs = parseInt($( "#input-option-param" + i + "-rangeStart" ).val());
        var re = parseInt($( "#input-option-param" + i + "-rangeEnd" ).val());
        if (!(rs > 0)) {
            rs = 1;
        }
        if (!(re > rs)) {
            re = rs;
        }
        var names = $( "#input-option-param" + i + "-params" ).val().split(",").map(function(x) { return x.trim() });

        if (type === "all") {
        } else if (type === "exhaustive") {
            result.range = [rs, re];
        } else if (type === "greedy") {
            result.range = [rs, re];
        } else if (type === "explicit") {
            result.parameters = names;
        } else if (type === "zero") {
        }
        return result;
    }

    $( "#dialog-parameters" ).dialog({
        title: "Parameter ranges to include in optimization",
        modal: true,
        autoOpen: false,
        width: 770,
        height: 350,
        open: function() {
            var parameters = CORUNNER.settings.get("parameters");
            for (var i = 0; i < 4; ++i) {
                displayParam(parameters, i);
            }
        },
        buttons: [
            {
                text: "Ok",
                click: function() {
                    var parameters = [];
                    for (var i = 0; i < 4; ++i) {
                        var type = $( "#input-option-params" + i ).val();
                        if (type !== "none") {
                            parameters.push(constructParam(type, i));
                        }
                    }
                    CORUNNER.settings.set("parameters", parameters);
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
            if (!CORUNNER.refresh.isActive()) {
                // start
                CORUNNER.settings.postSettings();
            } else { 
                // stop
                $.ajax({
                    url: "stopall",
                    success: function (returnData) {
                        CORUNNER.notify("Stopping all jobs");
                    },
                    error: function (data, textStatus, xhr) {
                        CORUNNER.notify("Failed to stop jobs: " + JSON.stringify(data) + " " + textStatus, "error");
                    }
                });
            }
        }
    });

    for (var i = 0; i < 4; ++i) {
        $('#button-stop-job' + i).click(function(){
            var sindex = $( this ).attr("id")
            var index = parseInt(sindex.substr(15));
            var job = CORUNNER.display.getJobID(index);
            if (job) {
                $.ajax({
                    url: "stop/" + job,
                    success: function (returnData) {
                        CORUNNER.notify("Stopping job " + job);
                    },
                    error: function (data, textStatus, xhr) {
                        CORUNNER.notify("Failed to stop job " + job + ": " + JSON.stringify(data) + " " + textStatus, "error");
                    }
                });
            }
        });
    }

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
    }
}();
