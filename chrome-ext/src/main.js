String.prototype.format = function() {
  var args = arguments;
  return this.replace(/{(\d+)}/g, function(match, number) {
    return typeof args[number] != 'undefined' ? args[number] : match;
  });
};
String.prototype.replaceAll = function(search, replacement) {
    var target = this;
    return target.split(search).join(replacement);
};

$(document).ready(function() {

  if (!isPageSupported(['python.task', 'Perltask'])) {
    return;
  }

  setCSS();

  $.getJSON('http://pytask.info/db/db.json', function(data) {
    fill_task_info(data);
  });

  var year = document.title.split('|')[1].trim();
  var path = 'http://pytask.info/db/categories/' + year + '.json';
  $.getJSON(path, function(data) {
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
  $('strong, font').each(function() {

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
  $('strong').each(function() {

    var context = $(this);
    var task_name = context.text().trim();
    if (!(task_name in data['this_year'])) return;

    var html = [
      '<div class="task_info">',
      '<h4>{0}</h4>'.format(task_name),
      '<ul class="nav nav-tabs">',
      '<li role="presentation" class="active">',
      '<a href="#{0}_this_year" data-toggle="tab">Этот год</a>'.format(task_name.replaceAll(' ', '_')),
      '</li>',
      '<li role="presentation">',
      '<a href="#{0}_all_years" data-toggle="tab">Все года</a>'.format(task_name.replaceAll(' ', '_')),
      '</li>',
      '</ul>',
      '<div class="tab-content">',
      make_statistics_html(data, task_name, 'this_year'),
      make_statistics_html(data, task_name, 'all_years'),
      '</div>',
      '</div>'
    ].join('');

    context.before(html);
    context.remove();

    $('#{0}_this_year'.format(task_name.replaceAll(' ', '_'))).addClass('active');
  });
}

function make_statistics_html(data, task_name, scope) {
  var task = data[scope][task_name];

  var max_students = task['max_students'];
  var min_students = task['min_students'];
  var max_percent = task['max_percent']
  var min_percent = task['min_percent']
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

function setCSS() {
  var stylesheet = document.styleSheets[0];

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

  rules.forEach(function(rule) {
    stylesheet.insertRule(rule, stylesheet.cssRules.length);
  });
}

