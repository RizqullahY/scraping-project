$(document).ready(function (){
    $("#fullscreen-button").click(function() {
        toggleFullScreen();
    });

    function toggleFullScreen() {
        if (!document.fullscreenElement &&    // alternative standard method
            !document.mozFullScreenElement && !document.webkitFullscreenElement && !document.msFullscreenElement ) {  // current working methods
            if (document.documentElement.requestFullscreen) {
                document.documentElement.requestFullscreen();
            } else if (document.documentElement.mozRequestFullScreen) {          /* Firefox */
                document.documentElement.mozRequestFullScreen();
            } else if (document.documentElement.webkitRequestFullscreen) {       /* Chrome, Safari & Opera */
                document.documentElement.webkitRequestFullscreen(Element.ALLOW_KEYBOARD_INPUT);
            } else if (document.documentElement.msRequestFullscreen) {         /* IE/Edge */
                document.documentElement.msRequestFullscreen();
            }
            $("#fullscreen-button").text("Exit");
        } else {
            if (document.exitFullscreen) {
                document.exitFullscreen();
            } else if (document.mozCancelFullScreen) {                     /* Firefox */
                document.mozCancelFullScreen();
            } else if (document.webkitExitFullscreen) {                  /* Chrome, Safari and Opera */
                document.webkitExitFullscreen();
            } else if (document.msExitFullscreen) {                      /* IE/Edge */
                document.msExitFullscreen();
            }
            $("#fullscreen-button").text("Fullscreen");
        }
    }

    $(document).on('fullscreenchange mozfullscreenchange webkitfullscreenchange msfullscreenchange', function () {
        if (document.fullscreenElement || document.mozFullScreenElement || document.webkitFullscreenElement || document.msFullscreenElement) {
            $("#fullscreen-button").text("Exit");
        } else {
            $("#fullscreen-button").text("Fullscreen");
        }
    });

})