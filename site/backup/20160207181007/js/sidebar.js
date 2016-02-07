$(document).ready(function() {
    var trigger = $('.hamburger'),
        overlay = $('.overlay'),
        isClosed = false;

    trigger.click(function() {
        hamburger_cross();
        $('#wrapper').toggleClass('toggled');
    });

    $('#page-content-wrapper').on('swiperight', function(e) {
        hamburger_cross();
        $('#wrapper').toggleClass('toggled');
    });

    $('.overlay').on('click', function() {
        hamburger_cross();
        $('#wrapper').toggleClass('toggled');
    })

    function hamburger_cross() {
        if (isClosed) {
            overlay.hide();
        } else {
            overlay.show();
        }
        isClosed = !isClosed;
    }
});
