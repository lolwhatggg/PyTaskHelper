$(document).ready(function(){
    console.log('da');
    $("#filter").keyup(function(){
        var filter = $(this).val();
        $(".searchable").each(function(){

            if ($(this).find('.name').text().toLowerCase().substring(0, filter.length) == filter.toLowerCase()) {
                $(this).show();
            } else {
                $(this).fadeOut();
            }
        });
    });
});