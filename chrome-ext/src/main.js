String.prototype.format = function () {
    var args = arguments;
    return this.replace(/{(\d+)}/g, function (match, number) {
        return typeof args[number] != 'undefined' ? args[number] : match;
    });
};
String.prototype.replaceAll = function (search, replacement) {
    return this.split(search).join(replacement);
};

$(document).ready(function () {

    if (!isPageSupported(['python.task', 'Perltask'])) {
        return;
    }

    setCSS();

    $.getJSON('http://pytask.info/db/tasks_base.json', function (data) {
        fill_task_info(data);
    });

    var year = document.title.split('|')[1].trim();
    var path = 'http://pytask.info/db/categories/' + year + '.json';
    $.getJSON(path, function (data) {
        fill_cat_info(data);
    });

});

function isPageSupported(supported) {
    for (var i = 0; i < supported.length; i++) {
        if (document.title.indexOf(supported[i]) !== -1) {
            return true;
        }
    }
    return false;
}

function fill_task_info(data) {
    $('strong, font').each(function () {

        var context = $(this);
        var task_name = context.text().trim();
        if (!(task_name in data)) return;

        var task = data[task_name];

        var max = context.next('span');
        var avg_percent = task['average_percent'];
        var avg_points = avg_percent * max.text() / 100;

        var students = task['students_amount'];
        var stud_full = task['students_full_points'];
        var perc_full = task['full_points_percent'];
        var link = 'http://pytask.info/tasks/' + task['filename'];

        var html = [
            '<div class="task_info">',
            '<h4>{0}</h4>'.format(task_name),
            '<p>Максимальный балл: ',
            '<span>{0}</span>'.format(max.text()),
            '</p>',
            '<p>Средний балл за все года: ',
            '<span>{0} ({1}%)</span>'.format(avg_points, avg_percent),
            '</p>',
            '<p>Сдавшие: ',
            '<span>{0} чел.</span>'.format(students),
            '</p>',
            '<p>Полный балл: ',
            '<span>{0} чел. ({1}%)</span>'.format(stud_full, perc_full),
            '</p>',
            '<hr>',
            '<a href="{0}">Подробная статистика...</a>'.format(link),
            '</div>'
        ].join('');

        context.before(html);
        context.remove();
        max.remove();
    });
}

function fill_cat_info(data) {
    $('strong').each(function () {
        var context = $(this);
        var task_name = context.text().trim();
        var html = [
            '<div class="task_info">',
            '<h4>{0}</h4>'.format(task_name),
            '<ul class="nav nav-tabs">',
            createTab(data, task_name, 'this_year', 'Этот год'),
            createTab(data, task_name, 'all_years', 'Все года'),
            '</ul>',
            '<div class="tab-content">',
            make_statistics_html(data, task_name, 'this_year'),
            make_statistics_html(data, task_name, 'all_years'),
            '</div>',
            '</div>'
        ].join('');

        context.before(html);
        context.remove();

        var tags = ['this_year', 'all_years'];

        for (var i = 0; i < tags.length; i++) {
            var task = task_name.replaceAll(' ', '_');
            var content = $('#{0}_{1}'.format(task, tags[i]));
            var tab = $('#{0}_{1}_tab'.format(task, tags[i]));
            if (!content.length) continue;
            content.addClass('active');
            tab.addClass('active');
            break;
        }

    });
}
function createTab(data, task_name, tag, tab_name) {
    if (!(task_name in data[tag]))
        return '';
    var task = task_name.replaceAll(' ', '_');

    var html = [
        '<li role="presentation" id="{0}_{1}_tab">'.format(task, tag),
        '<a href="#{0}_{1}" data-toggle="tab">{2}</a>'.format(task, tag, tab_name),
        '</li>'
    ].join('');

    return html;

}

function make_statistics_html(data, task_name, scope) {
    if (!(task_name in data[scope]))
        return '';
    var task = data[scope][task_name];
    var max_students = task['max_students'];
    var min_students = task['min_students'];
    var max_percent = task['max_percent'];
    var min_percent = task['min_percent'];
    var max_points = task['max_points'];
    var min_points = task['min_points'];
    var max_full_points = task['max_full_points'];
    var min_full_points = task['min_full_points'];

    var html = [
        '<div id="{0}_{1}" class="tab-plane">'.format(task_name.replaceAll(' ', '_'), scope),
        '<p>Количество людей:</p>',
        '<p>max: ',
        '<b>{0}</b> '.format(max_students[1]),
        '<span>({0})</span>'.format(max_students[0]),
        '</p>',
        '<p>min: ',
        '<b>{0}</b> '.format(min_students[1]),
        '<span>({0})</span>'.format(min_students[0]),
        '</p>',
        '<p>Средний балл:</p>',
        '<p>max: ',
        '<b>{0}</b> '.format(max_points[1]),
        '<span>({0})</span>'.format(max_points[0]),
        '</p>',
        '<p>min: ',
        '<b>{0}</b> '.format(min_points[1]),
        '<span>({0})</span>'.format(min_points[0]),
        '</p>',
        '<p>Средний процент выполнения:</p>',
        '<p>max: ',
        '<b>{0}</b> '.format(max_percent[1]),
        '<span>({0}%)</span>'.format(max_percent[0]),
        '</p>',
        '<p>min: ',
        '<b>{0}</b> '.format(min_percent[1]),
        '<span>({0}%)</span>'.format(min_percent[0]),
        '</p>',
        '<p>На полный балл:</p>',
        '<p>max: ',
        '<b>{0}</b> '.format(max_full_points[1]),
        '<span>({0})</span>'.format(max_full_points[0]),
        '</p>',
        '<p>min: ',
        '<b>{0}</b> '.format(min_full_points[1]),
        '<span>({0})</span>'.format(min_full_points[0]),
        '</p>',
        '</div>'
    ].join('');
    return html;
}

function findStylesheet() {
    for (var i = 0; i < document.styleSheets.length; i++) {
        if (document.styleSheets[i].cssRules != null)
            return document.styleSheets[i];
    }
}
function setCSS() {
    var stylesheet = findStylesheet();
    var rules = [
        ['.tab-content > .tab-plane {display: none;}'],
        ['.tab-content > .active {display: block;}'],
        ['.task_info {background-color: #eee; padding: 5px 10px; margin-bottom: 5px; border-radius: 5px;}'],
        ['.task_info hr {margin: 2px 0px;}'],
        ['.task_info p {margin: 3px 0px;}'],
        ['.task_info p span {color: green; font-weight: bold;}'],
        ['.task_info h4 {margin-bottom: 8px;}'],
        ['.task_info a {font-size: 12px;}']
    ];

    rules.forEach(function (rule) {
        stylesheet.insertRule(rule, stylesheet.cssRules.length);
    });
}

