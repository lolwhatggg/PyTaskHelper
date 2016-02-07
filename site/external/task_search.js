$(document).ready(function () {
    $("#filter").keyup(function (e) {
        if (e.keyCode == 13)
            return;
        var filter = $(this).val().toLowerCase();
        $(".task").each(function () {
            var show = false;
            $(this).find('.searchable').each(function () {
                show |= $(this).text().toLowerCase().indexOf(filter) != -1
            });
            show ? $(this).show() : $(this).fadeOut();
        });
    });
});