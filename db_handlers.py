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
        for field in self:
            self[field] = self.handler.get_finalized(self[field])


class Field:
    def __init__(self, name, update_method, default_value):
        self.name = name
        self.update_method = update_method
        self.default_value = default_value


class DBHandler:
    def __init__(self):
        self.fields = []

    def update_entry(self, old_data, new_data):
        result = {}
        for field in self.fields:
            if field.update_method is not None:
                result[field.name] = field.update_method(old_data, new_data)
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
            Field('name', None, Task.get_name),
            Field('points', Task.update_points, Task.get_points),
            Field('max', Task.update_max, Task.get_max)
        ]

    @staticmethod
    def get_finalized(entry):
        if entry['points']:
            entry['middle'] = mean(entry['points'])
        return entry


class Task:
    @staticmethod
    def get_name(task):
        return task['name']

    @staticmethod
    def get_points(task):
        return [student['points'] for student
                in task['students']]

    @staticmethod
    def get_max(task):
        return {task['max']}

    @staticmethod
    def update_points(task, another_task):
        return task['points'] + Task.get_points(another_task)

    @staticmethod
    def update_max(task, another_task):
        return task['max'].union(Task.get_max(another_task))
