from pprint import pformat
from statistics import mean
from inspect import getmembers


class Database(dict):
    def __new__(cls, entry_class):
        if 'finalize' in dir(entry_class):
            def _finalize(self):
                for name in self:
                    self[name].finalize()

            cls.finalize = _finalize
        return super().__new__(cls)

    def __init__(self, entry_class):
        super().__init__()
        self._entry_class = entry_class

    def add_entry(self, data):
        name = data['name']
        if name not in self:
            self[name] = self._entry_class(data)
        else:
            self[name].update(data)


class Entry:
    def __str__(self):
        return str(self.__dict__)

    def __repr__(self):
        return pformat(self.__dict__, depth=1)

    def update(self, new_data):
        updaters = filter(lambda m: m[0].startswith('update_'),
                          getmembers(self))
        for name, updater in updaters:
            updater(new_data)


class EntryWithoutAnnotations(Entry):
    def __init__(self, data):
        self.average = 0
        self.categories = {data['category']}
        self.name = data['name']
        self.max = {data['max']}
        self.points = [student['points'] for
                       student in data['students']]

    def update_points(self, new_data):
        self.points += [student['points'] for student
                        in new_data['students']]

    def update_max(self, new_data):
        self.max.add(new_data['max'])

    def update_category(self, new_data):
        self.categories.add(new_data['category'])

    def finalize(self):
        self.average = self.get_average(precision=2)

    def get_average(self, precision=0):
        average = mean([elem for elem in self.points if elem] or [0])
        average = round(average, precision)
        if average.is_integer():
            return int(average)
        return average


class EntryWithPercentage(EntryWithoutAnnotations):
    def __init__(self, data):
        super().__init__(data)
        self.percents = [(student['points'] / data['max'] * 100) for
                         student in data['students']]
        self.average_percent = 0

    def update_percents(self, new_data):
        self.percents += [(student['points'] / new_data['max'] * 100) for
                          student in new_data['students']]

    def finalize(self):
        super().finalize()
        self.average_percent = self.get_average()


class EntryFullInfo(EntryWithPercentage):
    def __init__(self, data):
        super().__init__(data)
        self.students = data['students']

    def update_students(self, new_data):
        self.students += new_data['students']


class EntryOnlyAverageValues(EntryWithPercentage):
    def finalize(self):
        super().finalize()
        del self.points
        del self.percents
