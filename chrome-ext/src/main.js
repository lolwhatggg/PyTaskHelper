function process_json(data) {
    $('strong, font').each(function(k, v) {
        var name = $(this).text();
        if (!(name in data)) {
            return;
        }
        var current_max_points = parseInt($(this).next('span').text());
        var percent_average = data[name]['average_percent']*current_max_points/100;
        var text =
            '&nbsp;Средний балл:&nbsp;' +
            '<span class="label label-info">' +
           percent_average+'</span>';
        console.log(current_max_points);
        $(this).next('*').after(text);
        //$(this).wrap('<a href="#"></a>');
    });
}

var xhr = new XMLHttpRequest();

xhr.onload = function() {
    var json = xhr.responseText;
    data = JSON.parse(json);
    process_json(data);
};

xhr.open('GET', 'http://avefablo.xyz/db.json');
xhr.send();
