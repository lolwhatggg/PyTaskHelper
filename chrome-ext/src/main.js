$(document).ready(function () {

    if (document.title.indexOf('python.task') == -1 &&
        document.title.indexOf('Perltask') == -1) {
        return;
    }

    var xhr = new XMLHttpRequest();

    xhr.onload = function () {
        var json = xhr.responseText;
        modify_page(JSON.parse(json));
        setCSS();
    };

    xhr.open('GET', 'http://pytask.info/db.json');
    xhr.send();

});

function modify_page(data) {
    $('strong, font').each(function () {

        var name = $(this).text();
        if (!(name in data)) {
            return;
        }

        var max = $(this).next('span');

        var avg_percent = data[name]['average_percent'];
        var avg_points = avg_percent * max.text() / 100;
        var students = data[name]['students_amount'];
        var stud_full = data[name]['students_all_points'];
        var perc_full = Math.round(stud_full / students * 100);
        var link = 'http://pytask.info/tasks/' + encodeURIComponent(name) + '.html'
        var text =
            '<div class="task_info">' +
            '<h4>' + name + '</h4>' +
            '<p>Максимальный балл: <span>' + max.text() + '</span></p>' +
            '<p>Средний балл за все года: <span>' + avg_points + '</span>' +
            '<p>Средний процент: <span>' + avg_percent + '%</span></p>' +
            '<p>Количество сдавших: <span>' + students + '</span></p>' +
            '<p>Количество сдавших на полный балл: <span>' + stud_full + '</span></p>' +
            '<p>Процент сдавших на полный балл: <span>' + perc_full + '%</span></p>' +
            '<hr>' +
            '<a href="' + link + '">Подробная статистика...</a>' +
            '</div>';

        $(this).before(text);
        $(this).remove();
        max.remove();
    });
}

function setCSS() {
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
}
