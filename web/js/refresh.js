"use strict";
CORUNNER.refresh = function() {

    var pageRefreshInterval = 2000;

    var refreshTimerID = null;
    var refreshFullTimerID = null;

    // status
    var isModelExecutable = false;
    var isActive = false;
    var hasResults = false;

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
            crossDomain: true,
            success: updateStatus,
            error: function (data, textStatus, xhr) {
                CORUNNER.notify("Failed to get CoRunner status", "error");
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
        isActive = data.jobs.length > 0;
        hasResults = data.resultsPresent;

        if (isActive != oldIsActive) {
            if (isActive) {
                $("#button-select").addClass('disabled');
            } else {
                CORUNNER.notify("Optimizations finished");
                $("#button-select").removeClass('disabled');
                // remove all charts
                CORUNNER.display.drawCharts([]);
            }
        }
        if (isActive != oldIsActive || isModelExecutable != oldIsModelExecutable) {
            if (isModelExecutable) {
                $("#button-start-stop").removeClass('disabled');
            } else {
                $("#button-start-stop").addClass('disabled');
            }
            if (isActive) {
                $("#button-start-stop").html('<i class="icon-stop" style="margin-top: 3px"></i> Stop');
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
                crossDomain: true,
                success: updateActiveStatus,
                error: function (data, textStatus, xhr) {
                    console.log("get active status error: " + JSON.stringify(data) + " " + textStatus);
                    refreshTimerID = setTimeout(refresh, pageRefreshInterval);
                }
            });
        } else {
            refreshTimerID = setTimeout(refresh, pageRefreshInterval);
        }
    }

    function updateActiveStatus(data) {
        CORUNNER.display.drawCharts(data);
        refreshTimerID = setTimeout(refresh, pageRefreshInterval);
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
            crossDomain: true,
            success: updateStatusFull,
            error: function (data, textStatus, xhr) {
                console.log("get server full status error: " + data + " " + textStatus);
            }
        });
    }

    function updateStatusFull(data) {
        console.log("all jobs: " + JSON.stringify(data));

        if (!$("#dialog-status").dialog('isOpen')) {
            console.log("dialog hidden");
            return;
        }

        var anyActive = false;
        var s = "";
        for (var i = 0; i < data.length; ++i) {
            var job = data[i];
            var status = job.active ? "running" : job.reason;
            if (job.active) anyActive = true;
            var params = "";
            for (var j = 0; j < job.parameters.length; ++j) {
                params += job.parameters[j];
                if (j < job.parameters.length - 1) {
                    params += ", ";
                }
            }
            s += '<div class="form-row">\n'
            s += "Job " + job.id + " / "
                + "OF value: " + job.of + " / "
                + "CPU time: " + (Math.round(10 * job.cpu) / 10.0) + " / "
                + "Status: " + status + " / "
                + "Method: " + job.method + " / "
                + params + "\n";
            s += '</div><br/>\n'
        }

        console.log(s)
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
        isActive: function () { return isActive }
    }
}();
