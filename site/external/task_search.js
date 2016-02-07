$(document).ready(function () {
    $("#filter").keyup(function () {
        var filter = $(this).val().toLowerCase();
        $(".task").each(function () {
            if ($(this).find('.name').text().toLowerCase().indexOf(filter) != -1 ||
                $(this).find('.category').text().toLowerCase().indexOf(filter) != -1) {
                $(this).show();
            } else {
                $(this).fadeOut();
            }
        });
    });
});