$(document).ready(function() {
    var trigger = $('.hamburger'),
        overlay = $('.overlay'),
        isClosed = false;

    function toggle() {
        if (isClosed) {
            $('body').css('overflow', 'auto');
            overlay.hide();
        } else {
            $('body').css('overflow', 'hidden');
            overlay.show();
        }
        isClosed = !isClosed;
        $('#wrapper').toggleClass('toggled');
    }

    trigger.click(toggle);
    $('#page-content-wrapper').on('swipe', toggle);
    $('.overlay').on('click', toggle);
});
