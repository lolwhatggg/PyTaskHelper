$(document).ready(function () {
    $("#filter").keyup(function () {
        var filter = $(this).val().toLowerCase();
        $(".searchable").each(function () {
            console.log("da");
            if ($(this).find('.name').text().toLowerCase().indexOf(filter) != -1) {
                $(this).show();
            } else {
                $(this).fadeOut();
            }
        });
    });
});