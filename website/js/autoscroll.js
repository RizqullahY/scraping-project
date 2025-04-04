$(document).ready(function(){
    var scrolling = false;
    var scrollSpeed = parseInt($("#scroll-speed").val());
    var scrollInterval;

    $("#scroll-speed").change(function () {
      scrollSpeed = parseInt($(this).val());
    });

    $("#start-scroll").click(function () {
      if (!scrolling) {
        scrolling = true;
        $(this).prop("disabled", true);
        $("#stop-scroll").prop("disabled", false);

        scrollInterval = setInterval(function () {
          $(window).scrollTop($(window).scrollTop() + scrollSpeed);
        }, 30);
      }
    });

    $("#stop-scroll").click(function () {
      if (scrolling) {
        scrolling = false;
        clearInterval(scrollInterval);
        $("#start-scroll").prop("disabled", false);
        $("#stop-scroll").prop("disabled", true);
      }
    });
    
    // IF ANY INTERACTION AUTO SCROLL WILL BE STOPPED 
    // $(document).on("mousedown mousewheel keydown", function() {
    //     if (scrolling) {
    //         scrolling = false;
    //         clearInterval(scrollInterval);
    //         $("#start-scroll").prop("disabled", false);
    //         $("#stop-scroll").prop("disabled", true);
    //     }
    // });
})