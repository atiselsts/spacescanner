"use strict";
var SPACESCANNER = function() {

    var MAX_DISPLAY_JOBS = 8;
    var MAX_DISPLAY_PARAMS = 5;

    $( "#dialog-select-model" ).dialog({
        title: "Select a model",
        modal: true,
        autoOpen: false,
        width: 750,
        height: 300,
        open: function() {
            SPACESCANNER.settings.populateSettings();
        },
    });

    $('#dialog-select-model').fileUpload({
        success: function (data, textStatus, jqXHR) {
            var filename = $( '#input-import-filename' ).val();
            if (filename) {
                // remove the "C:\fakepath" part of it, if present
                filename = filename.substring(filename.lastIndexOf('\\') + 1);
            }
            SPACESCANNER.notify("Model file selected:\n" + filename, "success");
            $( "#dialog-select-model" ).dialog("close");
            SPACESCANNER.settings.saveSettings();
            SPACESCANNER.settings.setParams(data["params"]);
            var title = SPACESCANNER.settings.get("copasi")["taskType"] === "optimization" ?
                "Optimization task" :
                "Parameter fitting task";
            title += ": model file '" + filename + "'";
            $( 'title' ).text(title);
        },
        error: function (data, textStatus, err) {
            SPACESCANNER.notify("Failed to use the model file: " + JSON.stringify(data), "error");
        },
        action: "modelfile"
    });

    $('#button-upload-model')
        .on("click",function(e) {
            var filename = $( '#input-import-filename' ).val();
            if (!filename || filename.length == 0) {
                e.preventDefault();
                SPACESCANNER.notify("Model file not specified", "error");
                return;
            }
        });

    $('#button-terminate-server')
        .on("click",function(e) {
            var msg;
            if (SPACESCANNER.refresh.isActive()) {
                msg = "Are you sure? The SpaceScanner is currently active!\n\n";
                msg += "Stopping the server will stop the current operations and lose all state.\n\n";
                msg += "It will also stop the server and disconnect the web interface.";
            } else {
                msg = "Are you sure?\n\n";
                msg = "This will stop the server and disconnect the web interface.";
            }

            var r = confirm(msg);
            if (r !== true) {
                return;
            }
            $.ajax({
                url: "terminate",
                success: function (returnData) {
                    SPACESCANNER.notify("Stopped the server");
                },
                error: function (data, textStatus, xhr) {
                    SPACESCANNER.notify("Failed to stop the server: " + JSON.stringify(data) + " " + textStatus, "error");
                }
            });
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
        width: 1150,
        height: 700,
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
        SPACESCANNER.settings.estimateNumJobs();
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
            SPACESCANNER.settings.estimateNumJobs();
        } else {
            SPACESCANNER.notify("Max " + MAX_DISPLAY_PARAMS + " different parameter sets");
        }
    });

    $( "#dialog-parameters" ).dialog({
        title: "Adjustable parameter sets to search through",
        modal: true,
        autoOpen: false,
        width: 880,
        height: 510,
        open: function() {
            SPACESCANNER.settings.populateSettings();
            SPACESCANNER.settings.estimateNumJobs();

            var s = "";
            var params = SPACESCANNER.settings.getParams();
            if (params.length) {
                s += "<table><tbody>";
                s += '<tr>';
                s += '<th style="width:64%;text-align:center;vertical-align:middle;font-weight:bold">Parameter</th>';
                s += '<th style="width:12%;text-align:center;font-weight:bold">Combinatorially optimized</th>';
                s += '<th style="width:12%;text-align:center;font-weight:bold">Always optimized</th>';
                s += '<th style="width:12%;text-align:center;font-weight:bold">Never optimized</th>';
                s += '</tr>\n';

                for (var i = 0; i < params.length; ++i) {
                    var r = '<input type="radio" name="dialog-params-param-' + i + '" ';
                    var included = SPACESCANNER.settings.getParamIncluded(params[i]);
                    var c1 = included === "contingent" ? " checked" : "";
                    var c2 = included === "always" ? " checked" : "";
                    var c3 = included === "never" ? " checked" : "";
                    s += '<td id="dialog-params-param-row-' + i + '" style="width:55%">' + params[i] + '</td>';
                    s += '<td style="width:12%;text-align:center">' + r + 'value="contingent"' + c1 + '></td>';
                    s += '<td style="width:12%;text-align:center">' + r + 'value="always"' + c2 + '></td>';
                    s += '<td style="width:12%;text-align:center">' + r + 'value="never"' + c3 + '></td>';
                    s += '</tr>\n';
                }
                s += "</tbody></table>";
            }
            $( "#dialog-params-model-params" ).html(s);

            // setup change callbacks
            for (var i = 0; i < params.length; ++i) {
                $( 'input[type=radio][name=dialog-params-param-' + i + ']' ).change(function() {
                    SPACESCANNER.refresh.redrawAlwaysNeverIncludedParams();
                    SPACESCANNER.settings.estimateNumJobs();
                });
            }
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
                SPACESCANNER.settings.stopAll();
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
                    url: "stop?jobid=" + job,
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
        if (!$( this ).hasClass('disabled')) {
            $( "#dialog-parameters" ).dialog( "open" )
        }
    });

    $('#button-export').click(function(){
        if (!$( this ).hasClass('disabled')) {
            $( "#dialog-export" ).dialog( "open" )
        }
    });

    $(function() {
        console.log("loading SpaceScanner web interface...")
    });

    var uppie = new Uppie();

    //    uppie($('#input-import-filename'), function(event, formData, files) {
    uppie(document.querySelectorAll("#input-import-filename"), function(event, formData, files) {
        console.log("got reply");
        console.log("files = " + files.join("\n"));
        console.log("data = " + JSON.stringify(formData));
        // document.querySelector(".output").textContent = files.join("\n");
    });

    return {
    }
}();
