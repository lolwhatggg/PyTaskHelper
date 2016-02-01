from statistics import mean
from inspect import getmembers
from abc import ABCMeta, abstractmethod


class Database(dict):
    def __init__(self, entry_class):
        super().__init__()
        self._entry_class = entry_class

    def add_entry(self, data):
        name = data['name']
        if name not in self:
            self[name] = self._entry_class(data)
        self[name].update(data)

    def finalize(self):
        for name in self:
            self[name].finalize()


class Entry(metaclass=ABCMeta):
    def __str__(self):
        return str(self.__dict__)

    @abstractmethod
    def finalize(self):
        pass

    def update(self, new_data):
        updaters = filter(lambda m: m[0].startswith('update_'),
                          getmembers(self))
        for name, updater in updaters:
            updater(new_data)


class EntryWithoutAnnotations(Entry):
    def __init__(self, data):
        self.middle = 0
        self.name = data['name']
        self.max = {data['max']}
        self.points = [student['points'] for
                       student in data['students']]

    def update_points(self, new_data):
        self.points += [student['points'] for student
                        in new_data['students']]

    def update_max(self, new_data):
        self.max.add(new_data['max'])

    def finalize(self):
        self.middle = mean(self.points or [0])
