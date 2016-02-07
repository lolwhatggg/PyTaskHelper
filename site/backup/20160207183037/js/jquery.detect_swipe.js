(function($) {

    $.detectSwipe = {
        version: '2.1.1',
        enabled: 'ontouchstart' in document.documentElement,
        preventDefault: true,
        threshold: 20,
        zone: 50
    };

    var startX,
        startY,
        isMoving = false,
        side;

    function onTouchStart(e) {
        if (e.touches.length !== 1) {
            return;
        }

        startX = e.touches[0].pageX;
        startY = e.touches[0].pageY;

        switch (side) {
            case 'left':
                if (startX > $.detectSwipe.zone) return;
                break;
            case 'right':
                if (startX < $(window).width() - $.detectSwipe.zone) return;
                break;
            case 'up':
                if (startY > $.detectSwipe.zone) return;
                break;
            case 'down':
                if (startY < $(window).height() - $.detectSwipe.zone) return;
                break;
        }

        isMoving = true;
        this.addEventListener('touchmove', onTouchMove, false);
        this.addEventListener('touchend', onTouchEnd, false);
    }

    function onTouchMove(e) {
        if ($.detectSwipe.preventDefault) {
            e.preventDefault();
        }

        if (!isMoving) {
            return;
        }

        var x = e.touches[0].pageX;
        var y = e.touches[0].pageY;
        var dx = startX - x;
        var dy = startY - y;

        var dir;
        if (Math.abs(dx) >= $.detectSwipe.threshold) {
            dir = dx > 0 ? 'right' : 'left'
        } else if (Math.abs(dy) >= $.detectSwipe.threshold) {
            dir = dy > 0 ? 'up' : 'down'
        }

        if (dir) {
            onTouchEnd.call(this);
            $(this).trigger('swipe', dir).trigger('swipe' + dir);
        }
    }

    function onTouchEnd() {
        this.removeEventListener('touchmove', onTouchMove);
        this.removeEventListener('touchend', onTouchEnd);
        isMoving = false;
    }

    function setup() {
        this.addEventListener && this.addEventListener('touchstart', onTouchStart, false);
    }

    function teardown() {
        this.removeEventListener('touchstart', onTouchStart);
    }

    $.event.special.swipe = {
        setup: setup
    };

    $.event.special['swipeleft'] = {
        setup: function () {
          side = 'left';
          $(this).on('swipe', $.noop);
        }
    };

    $.event.special.swiperight = {
        setup: function () {
          side = 'right';
          $(this).on('swipe', $.noop);
        }
    };

    $.event.special.swipeup = {
        setup: function () {
          side = 'up';
          $(this).on('swipe', $.noop);
        }
    };

    $.event.special.swipedown = {
        setup: function () {
          side = 'down';
          $(this).on('swipe', $.noop);
        }
    };

})(jQuery);
