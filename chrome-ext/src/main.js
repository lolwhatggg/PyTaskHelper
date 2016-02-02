function process_json(data) {
    $('strong, font').each(function(k, v) {
        var name = $(this).text();
        if (!(name in data)) {
            return;
        }
        var text =
            '&nbsp;Средний балл:&nbsp;' +
            '<span class="label label-success">' +
            data[name]['average'].toFixed(1) +
            '</span>';
        $(this).next('*').after(text);
        $(this).wrap('<a href="#"></a>');
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
