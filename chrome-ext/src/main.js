function process_json(data) {
    $('strong, font').each(function() {

        var name = $(this).text();
        if (!(name in data)) {
            return;
        }

        var max = $(this).next('span');

        var avg = data[name]['average_percent'] * max.text() / 100;
        var text =
            '&nbsp;Средний балл:&nbsp;' +
            '<span class="label label-info">' + avg + '</span>';

        max.after(text);
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
