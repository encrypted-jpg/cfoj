(function ($) {

    "use strict";
    var fullHeight = function () {

        $('.js-fullheight').css('height', $(window).height());
        $(window).resize(function () {
            $('.js-fullheight').css('height', $(window).height());
        });
    };
    fullHeight();

    $('#sidebarCollapse').on('click', function () {
        $('#sidebar').toggleClass('active');
        var width = $('#content').css('left');
        console.log(document.getElementById('sidebar').classList.contains('active'));
        if (width === "100px") {
            $('#content').css({'left': '250px'});
        } else {
            $('#content').css({'left': '100px'});
        }
    });

})(jQuery);
