import json
import glob
import os.path

KNOWN_ALIASES = {

}


def get_all_task_names(files):
    task_names = set()
    for filename in files:
        with open(filename, 'rb') as file:
            data = json.load(file)
        for task in data:
            task_names.add(task['name'])
    return task_names


def count_middle_value(values):
    if not values:
        return 0
    return sum(values) // len(values)


def build_task_database(files, save_full_info=False):
    database = {}
    for filename in files:
        with open(filename, 'rb') as file:
            data = json.load(file)
        for task in data:
            name = task['name']
            points = [student['points'] for student in task['students']]
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
    for task in database:
        points = database[task]['points']
        database[task]['middle'] = count_middle_value(points)
    return database


if __name__ == '__main__':
    files = glob.glob(os.path.join('courses', '*.json'))
    db = build_task_database(files)
    for task in sorted(db):
        print('{}: {}'.format(task, db[task]))
