function process_json(data) {
    $('strong, font').each(function() {

        var name = $(this).text();
        if (!(name in data)) {
            return;
        }

        var max = $(this).next('span');

        var avg_percent = data[name]['average_percent'];
        var avg_points = avg_percent * max.text() / 100;

        var text =
            '<div class="task_info">' +
            '<p>Средний балл: ' + avg_points + '</p>' +
            '<p>Средний процент: ' + avg_percent + '%</p>' +
            '</div>';

        max.after(text);
        $(this).addClass('show_info');
    });
}

var xhr = new XMLHttpRequest();

xhr.onload = function() {
    var json = xhr.responseText;
    process_json(JSON.parse(json));

    $('.task_info').css({
        'display': 'none'
    });

    $('.show_info').css({
        'cursor': 'pointer',
        'text-decoration': 'underline'
    });

    $('.show_info').on('click', function () {
        var task_info = $(this).next().next('.task_info');
        var is_visible = task_info.css('display') == 'block';

        if (is_visible) {
            task_info.css('display', 'none');
        } else {
            task_info.css('display', 'block');
        }
    });

};

xhr.open('GET', 'http://avefablo.xyz/db.json');
xhr.send();
