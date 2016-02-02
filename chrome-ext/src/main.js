function process_json(data) {
    var task_values = [];
    $.each(data, function (name, elem) {
        task_values[name] = elem['average']
    });
    console.log(task_values);
    var current_tasks = [];
    $('strong, font').each(function (k, v) {
        var name = $(this).text();
        var average = get_average(name, task_values);
        if (average)
        {
            $(this).next('*').after(' Средний балл за все года: <span class="label  label-success">' +
                                     average.toFixed(2).toString() +
                                     '</span>');
        }
    });
}
function get_average(name, db){
    if (name in db) {
        return db[name];
    }
    else{
        return null;
    }
}
var xhr = new XMLHttpRequest();
xhr.onload = function () {
    var json = xhr.responseText;
    data = JSON.parse(json);
    process_json(data)
};
xhr.open('GET', 'http://avefablo.xyz/db.json');
xhr.send();

