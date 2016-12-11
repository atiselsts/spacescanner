"use strict";
SPACESCANNER.refresh = function() {

    var pageRefreshInterval = 2000;

    var refreshTimerID = null;
    var refreshFullTimerID = null;

    // status
    var isModelExecutable = false;
    var isActive = false;
    var hasResults = false;

    var resultsButtonClicked = false;

    // get list of active jobs and the general state
    function refresh() {
        if (refreshTimerID) {
            clearTimeout(refreshTimerID);
            refreshTimerID = null;
        }

        $.ajax({
            type: "GET",
            url: "status",
            contentType: "application/json",
            dataType: "json",
            success: updateStatus,
            error: function (data, textStatus, xhr) {
                SPACESCANNER.notify("Failed to get SpaceScanner status", "error");
                // refresh slower in case of error
                refreshTimerID = setTimeout(refresh, pageRefreshInterval * 3);
            }
        });
    }

    function updateStatus(data) {
        var oldIsModelExecutable = isModelExecutable;
        var oldIsActive = isActive;
        var oldHasResults = hasResults;

        isModelExecutable = data.isExecutable;
        isActive = data.isActive;
        hasResults = data.resultsPresent;

        if (isActive != oldIsActive) {
            if (isActive) {
                resultsButtonClicked = false;
                $("#button-select").addClass('disabled');
            } else {
                SPACESCANNER.notify("Optimizations finished");
                SPACESCANNER.display.resetMethods();
                $("#button-select").removeClass('disabled');
                if (!resultsButtonClicked) {
                    // remove all charts
                    SPACESCANNER.display.drawCharts(0.0, []);
                }
            }
        }
        if (isActive != oldIsActive || isModelExecutable != oldIsModelExecutable) {
            if (isModelExecutable) {
                $("#button-start-stop").removeClass('disabled');
            } else {
                $("#button-start-stop").addClass('disabled');
            }
            if (isActive) {
                $("#button-start-stop").html('<i class="icon-stop" style="margin-top: 3px"></i> Stop all');
            } else {
                $("#button-start-stop").html('<i class="icon-play" style="margin-top: 3px"></i> Start');
            }
        }
        if ((isActive || hasResults) != (oldIsActive || oldHasResults)) {
            if (isActive || hasResults) {
                $("#button-status").removeClass('disabled');
            } else {
                $("#button-status").addClass('disabled');
            }
        }
        if (hasResults != oldHasResults) {
            if (hasResults) {
                $("#button-export").removeClass('disabled');
            } else {
                $("#button-export").addClass('disabled');
            }
        }

        if (isActive) {
            $.ajax({
                type: "GET",
                url: "activestatus",
                contentType: "application/json",
                dataType: "json",
                success: function (response) {
                    SPACESCANNER.display.drawCharts(response.baseline, response.stats);
                    refreshTimerID = setTimeout(refresh, pageRefreshInterval);
                },
                error: function (data, textStatus, xhr) {
                    console.log("get active status error: " + JSON.stringify(data) + " " + textStatus);
                    refreshTimerID = setTimeout(refresh, pageRefreshInterval);
                }
            });
        } else {
            refreshTimerID = setTimeout(refresh, pageRefreshInterval);
        }
    }

    function showFinishedJobResults(id) {
        resultsButtonClicked = true;

        SPACESCANNER.display.resetMethods();

        $.ajax({
            type: "GET",
            url: "job/" + id,
            contentType: "application/json",
            dataType: "json",
            success:  function (response) {
                SPACESCANNER.display.drawCharts(response.baseline, response.stats);
            },
            error: function (data, textStatus, xhr) {
                console.log("get job " + id + " status error: " + JSON.stringify(data) + " " + textStatus);
            }
        });

        $( "#dialog-status" ).dialog( "close" );
    }

    // get list of all jobs (active + finished)
    function refreshFull() {
        if (refreshFullTimerID) {
            clearTimeout(refreshFullTimerID);
            refreshFullTimerID = null;
        }

        $.ajax({
            type: "GET",
            url: "allstatus",
            contentType: "application/json",
            dataType: "json",
            success: updateStatusFull,
            error: function (data, textStatus, xhr) {
                console.log("get server full status error: " + data + " " + textStatus);
            }
        });
    }

    function updateStatusFull(response) {
        if (!$("#dialog-status").dialog('isOpen')) {
            console.log("status dialog hidden");
            return;
        }

	var data = response.stats;

        var anyActive = false;
        for (var i = data.length - 1; i >= 0 ; --i) {
            if (data[i].active) {
                anyActive = true;
                break;
            }
        }
        var s = "";
        for (var i = 0; i < data.length; ++i) {
            var job = data[i];
            var status = job.active ? "running" : job.reason;
            var params = "";
            for (var j = 0; j < job.parameters.length; ++j) {
                params += job.parameters[j];
                if (j < job.parameters.length - 1) {
                    params += ", ";
                }
            }
            s += '<div class="form-row">\n'
            s += "Job " + job.id + " / ";
            if (!anyActive) {
                s += '<a title="Show job results graph" class="button-results" id="button-results-' + job.id +'" onclick="SPACESCANNER.refresh.showFinishedJobResults(' + job.id + ')">Result graph</a> / ';
            }
            s += "OF value: " + job.of + " / "
                + "Max CPU time: " + (Math.round(10 * job.cpu) / 10.0) + " sec / "
                + "Total CPU time: " + (Math.round(10 * job.totalCpu) / 10.0) + " sec / "
                + "Status: " + status + " / "
                + "Method: " + job.method + " / "
                + params + "\n";
            s += '</div><br/>\n'
        }

        $( "#dialog-status" ).dialog("option", "title",
            anyActive ? "Job status" : "Job status (finished only)");
        $("#dialog-status").html(s);
        
        refreshFullTimerID = setTimeout(refreshFull, pageRefreshInterval * 3);
    }

    // delayed refresh
    refreshTimerID = setTimeout(refresh, pageRefreshInterval);

    return {
        refresh: refresh,
        refreshFull: refreshFull,
        isActive: function () { return isActive },
        showFinishedJobResults: showFinishedJobResults,
    }
}();
