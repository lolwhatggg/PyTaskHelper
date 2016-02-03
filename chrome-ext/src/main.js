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
            '<h4>' + name + '</h4>' +
            '<p>Максимальный балл: <span>' + max.text() + '</span></p>' +
            '<p>Средний балл за все года: <span>' + avg_points + '</span>' +
            '<p>Средний процент: <span>' + avg_percent + '%</span></p>' +
            '<hr>' +
            '<a href="">Подробная статистика...</a>' +
            '</div>';

        $(this).before(text);
        $(this).remove();
        max.remove();
    });
}

var xhr = new XMLHttpRequest();

xhr.onload = function() {
    var json = xhr.responseText;
    process_json(JSON.parse(json));

    $('.task_info').css({
        'background-color': '#eee',
        'padding': '5px 10px',
        'margin-bottom': '5px',
        'border-radius': '5px'
    });

    $('.task_info hr').css({
        'margin': '2px 0px'
    });

    $('.task_info p').css({
        'margin': '3px 0px'
    });

    $('.task_info p span').css({
        'color': 'green',
        'font-weight': 'bold'
    });

    $('.task_info h4').css({
        'margin-bottom': '8px'
    });

    $('.task_info a').css({
        'font-size': '12px'
    });

};

xhr.open('GET', 'http://avefablo.xyz/db.json');
xhr.send();
