function process_json(data) {
    $('strong, font').each(function () {

        var name = $(this).text();
        if (!(name in data)) {
            return;
        }

        var max = $(this).next('span');
        var task_data = {
            'avg_percent': data[name]['average_percent'],
            'avg_points': this.avg_percent * max.text() / 100,
            'students': data[name]['students_amount'],
            'stud_full': data[name]['students_all_points'],
            'perc_full': Math.round(this.stud_full / this.students * 100)
        };
        var link = 'http://pytask.info/?task=' + encodeURIComponent(name);
        var text =
            '<div class="task_info">' +
            '<h4>' + name + '</h4>' +
            '<p>Максимальный балл: <span>' + max.text() + '</span></p>' +
            '<p>Средний балл за все года: <span>' + task_data.avg_points + '</span>' +
            '<p>Средний процент: <span>' + task_data.avg_percent + '%</span></p>' +
            '<p>Количество сдавших: <span>' + task_data.students + '</span></p>' +
            '<p>Количество сдавших на полный балл: <span>' + task_data.stud_full + '</span></p>' +
            '<p>Процент сдавших на полный балл: <span>' + task_data.perc_full + '%</span></p>' +
            '<hr>' +
            '<a href="' + link + '">Подробная статистика...</a>' +
            '</div>';

        $(this).before(text);
        $(this).remove();
        max.remove();
    });
}

var xhr = new XMLHttpRequest();

xhr.onload = function () {
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

xhr.open('GET', 'http://pytask.info/db.json');
xhr.send();
