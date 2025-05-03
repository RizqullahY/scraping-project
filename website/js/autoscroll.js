$(document).ready(function () {
  var scrolling = false;
  var scrollSpeed = parseInt($("#scroll-speed").val());
  var scrollInterval;

  $("#scroll-speed").change(function () {
      scrollSpeed = parseInt($(this).val());
  });

  function startScrolling() {
      if (!scrolling) {
          scrolling = true;
          $("#start-scroll").prop("disabled", true);
          $("#stop-scroll").prop("disabled", false);
          scrollInterval = setInterval(function () {
              $(window).scrollTop($(window).scrollTop() + scrollSpeed);
          }, 30);
      }
  }

  function stopScrolling() {
      if (scrolling) {
          scrolling = false;
          clearInterval(scrollInterval);
          $("#start-scroll").prop("disabled", false);
          $("#stop-scroll").prop("disabled", true);
      }
  }

  $("#start-scroll").click(startScrolling);
  $("#stop-scroll").click(stopScrolling);

  // Toggle with SPACE key
  $(document).keydown(function (e) {
    if (e.code === "Space") {
        e.preventDefault(); // prevent scroll jump
        if (scrolling) {
            stopScrolling();
        } else {
            startScrolling();
        }
    } else if (e.code === "ArrowLeft") {
        stopScrolling();
    } else if (e.code === "ArrowRight") {
        startScrolling();
    }
});


  // Optional: stop scroll on user interaction
  // $(document).on("mousedown mousewheel keydown", function(e) {
  //     if (scrolling && e.code !== "Space") {
  //         stopScrolling();
  //     }
  // });
});
