(function($) {

    $.EdgeSwipe = {
        enabled: 'ontouchstart' in document.documentElement,
        preventDefault: true,
        threshold: 20,
        zone: 50
    };

    var startX;
    var isMoving = false;

    function onTouchStart(e) {
        if (e.touches.length !== 1) {
            return;
        }
        startX = e.touches[0].pageX;
        if (startX > $.EdgeSwipe.zone) {
            return;
        }
        isMoving = true;
        this.addEventListener('touchmove', onTouchMove, false);
        this.addEventListener('touchend', onTouchEnd, false);
    }

    function onTouchMove(e) {
        if ($.EdgeSwipe.preventDefault) {
            e.preventDefault();
        }
        if (!isMoving) {
            return;
        }
        var dx = e.touches[0].pageX - startX;
        if (dx >= $.EdgeSwipe.threshold) {
            onTouchEnd.call(this);
            $(this).trigger('swipe');
        }
    }

    function onTouchEnd() {
        this.removeEventListener('touchmove', onTouchMove);
        this.removeEventListener('touchend', onTouchEnd);
        isMoving = false;
    }

    $.event.special.swipe = {
        setup: function() {
            this.addEventListener('touchstart', onTouchStart, false);
        }
    };

})(jQuery);
