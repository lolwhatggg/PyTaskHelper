import os
import json

KNOWN_ALIASES = {

}

def get_jsons():
    files = []
    for file in os.listdir('courses'):
        if file.endswith('.json'):
            files.append('courses/' + file)
    return files


def get_all_task_names(files):
    task_names = set()
    for filename in files:
        raw = open(filename, encoding='utf-8')
        data = json.loads(raw.read(), encoding='utf-8')
        for task in data:
            name = task['name']
            task_names.add(name)
        raw.close()
    return task_names


def count_middle_value(values):
    if len(values) == 0:
        return 0
    return sum(values) / len(values)


def build_task_database(files, save_full_info=False):
    database = {}
    for filename in files:
        raw = open(filename, encoding='utf-8')
        data = json.loads(raw.read(), encoding='utf-8')
        for task in data:
            name = task['name']
            if 'students' in task:
                points = [int(i['points']) for i in task['students']]
            else:
                points = []
            if name in database:
                database[name]['max'].add(task['max'])
                database[name]['points'] += points
                if save_full_info:
                    database[name]['students'] += task['students']
            else:
                database[name] = {'max': {task['max']},
                                  'points': points,
                                  'middle': 0}
                if save_full_info:
                    database[name]['students'] = task['students']
        raw.close()
    for task in database.keys():
        points = database[task]['points']
        database[task]['middle'] = count_middle_value(points)
    return database


if __name__ == '__main__':
    files = get_jsons()
    db = build_task_database(files)
    for i in sorted(db):
        print('{}: {}'.format(i, db[i]))
