from abc import ABCMeta, abstractmethod
from copy import deepcopy


class DBHandler(metaclass=ABCMeta):
    @abstractmethod
    def parse_task(self, task):
        pass

    @abstractmethod
    def add_entry(self, db, task):
        pass

    def count_middle_value(self, values):
        if not values:
            return 0
        return sum(values) / len(values)


class DBHandlerWithoutAnnotations(DBHandler):
    def parse_task(self, task):
        task_data = {}
        task_data['name'] = task['name']
        task_data['points'] = [student['points'] for student in task['students']]
        task_data['max'] = task['max']
        return task_data

    def add_entry(self, db, task_data):
        name = task_data['name']
        if name in db:
            db[name]['max'].add(task_data['max'])
            db[name]['points'] += task_data['points']
        else:
            db[name] = {'max': {task_data['max']},
                        'points': task_data['points'],
                        'middle': 0}

    def finalize(self, db):
        for task in db:
            db[task]['middle'] = self.count_middle_value(db[task]['points'])