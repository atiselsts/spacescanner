"use strict";
var CORUNNER = function() {

    $( "#dialog-select-model" ).dialog({
        title: "Select a model",
        modal: true,
        autoOpen: false,
        width: 600,
        height: 270,// 190,
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
            },
            {
                text: "Cancel",
                click: function() {
                    $( this ).dialog( "close" );
                }
            }
        ]
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
        height: 400,
        open: function() {
						console.log("model dlg opened")
        },
        close: function() {
						console.log("model dlg closed")
        },
        buttons: [
            {
                text: "Export",
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

    $('#button-status').click(function(){
				if (!$( this ).hasClass('disabled')) {
						$( "#dialog-status" ).dialog( "open" )
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
}();
