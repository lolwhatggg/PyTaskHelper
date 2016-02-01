from abc import ABCMeta, abstractmethod
from statistics import mean


class Database(dict):
    def __init__(self, handler):
        super().__init__()
        self.handler = handler

    def add_entry(self, entry):
        name = entry['name']
        if name in self:
            self[name] = self.handler.update_entry(self[name], entry)
        else:
            self[name] = self.handler.get_new_entry(entry)

    def finalize(self):
        for e in self.keys():
            self[e] = self.handler.get_finalized_value(self[e])


class Field:
    def __init__(self, name, update_method, default_value):
        self.name = name
        self.update = update_method
        self.default_value = default_value


class DBHandler:
    def __init__(self):
        self.fields = []

    def update_entry(self, old_data, new_data):
        result = {}
        for field in self.fields:
            if field.update is not None:
                result[field.name] = field.update(old_data, new_data)
            else:
                result[field.name] = old_data[field.name]
        return result

    def get_new_entry(self, entry):
        result = {}
        for field in self.fields:
            result[field.name] = field.default_value(entry)
        return result


class DBHandlerWithoutAnnotations(DBHandler):
    def __init__(self):
        super().__init__()
        self.fields = [
            Field('name', None, get_name),
            Field('points', update_points, get_points),
            Field('max', update_max, get_max)
        ]

    def get_finalized_value(self, entry):
        result = entry
        if result['points']:
            result['middle'] = mean(result['points'])
        return result


def get_name(task):
    return task['name']


def get_points(task):
    return [student['points'] for student in task['students']]


def get_max(task):
    return {task['max']}


def update_points(old_data, new_data):
    return old_data['points'] + get_points(new_data)


def update_max(old_data, new_data):
    return old_data['max'].union(get_max(new_data))
