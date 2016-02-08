from abc import ABCMeta, abstractmethod
from pprint import pformat
from statistics import mean
import datetime

KNOWN_NAME_ALIASES = {'FAT32': 'Разбор FAT32',
                      'ext4': 'Разбор ext4'}


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
        name = KNOWN_NAME_ALIASES.get(name, name)
        if name not in self:
            self[name] = self._entry_class(data)
        self[name].update(data)


class Entry(metaclass=ABCMeta):
    @abstractmethod
    def __init__(self, data):
        pass

    @abstractmethod
    def update(self, data):
        pass

    def __str__(self):
        return str(self.__dict__)

    def __repr__(self):
        return pformat(self.__dict__, depth=1)


class EntryWithoutAnnotations(Entry):
    def __init__(self, data):
        self.max = tuple()
        self.category = tuple()
        self.name = KNOWN_NAME_ALIASES.get(data['name'],
                                           data['name'])
        self.filename = self.get_filename()
        self.points = []
        self.history = {}
        self.students_amount = 0
        self.students_full_points = 0

    def update(self, data):
        year = data['year']
        self.history[year] = data['category']
        if not self.category or self.category[1] < year:
            self.category = (data['category'], year)
        if not self.max or self.max[1] < year:
            self.max = (data['max'], year)
        self.points += [(student['points'], data['max']) for student
                        in data['students']]

    def finalize(self):
        self.points = [elem for elem in self.points if elem[0]]
        self.students_amount = len(self.points)
        self.students_full_points = len([elem for elem in self.points
                                         if elem[0] == elem[1]])

        self.category = self.category[0]
        self.max = self.max[0]
        del self.points

    def get_filename(self):
        specific_names = {'bmp': 'bmp_stegano'}
        return specific_names.get(self.name, self.name) + '.html'

    @staticmethod
    def get_average(iterable, precision=0):
        average = mean([elem for elem in iterable if elem] or [0])
        average = round(average, precision)
        if average.is_integer():
            return int(average)
        return average


class EntryWithPercentage(EntryWithoutAnnotations):
    def __init__(self, data):
        super().__init__(data)
        self.percents = []
        self.average_percent = 0
        self.average_points = 0
        self.full_points_percent = 0

    def update(self, data):
        super().update(data)
        self.percents += [(student['points'] / data['max'] * 100) for
                          student in data['students']]

    def finalize(self):
        super().finalize()
        self.average_percent = self.get_average(self.percents)
        self.average_points = self.average_percent * self.max / 100
        if self.students_amount:
            self.full_points_percent = int(self.students_full_points /
                                           self.students_amount * 100)
        else:
            self.full_points_percent = 0
        del self.percents


class EntryFullInfo(EntryWithPercentage):
    def __init__(self, data):
        super().__init__(data)
        self.students = []

    @staticmethod
    def create_dt(student_data, field):
        return datetime.datetime.strptime(student_data[field],
                                          '%d.%m.%Y')

    def get_days(self, student_data):
        if student_data['points'] == 0:
            return 0
        first_dt = self.create_dt(student_data, 'first_date')
        second_dt = self.create_dt(student_data, 'second_date')
        return (second_dt - first_dt).days

    def update(self, data):
        super().update(data)
        new_students = [student for student in data['students'] if student['points']]
        for student in new_students:
            student['max'] = data['max']
            student['days'] = self.get_days(student)
            student['percent'] = int(student['points'] / data['max'] * 100)
        self.students += new_students


class EntryAnnualFullInfo(EntryFullInfo):
    def __init__(self, data):
        super().__init__(data)
        self.annual_averages = {}

    def finalize(self):
        super().finalize()
        results = {}
        for student in self.students:
            year = student['year']
            if year not in results:
                results[year] = {'points': [],
                                 'percents': [],
                                 'max': student['max'],
                                 'students_amount': 0,
                                 'students_full_points': 0
                                 }
            results[year]['points'].append(student['points']),
            results[year]['percents'].append(student['percent'])
            results[year]['students_amount'] += 1
            if student['points'] == student['max']:
                results[year]['students_full_points'] += 1

        for year in results:
            results[year]['average_percent'] = \
                self.get_average(results[year]['percents'])
            results[year]['average_points'] = \
                self.get_average(results[year]['points'], 2)
            if self.students_amount:
                results[year]['full_points_percent'] = \
                    int(results[year]['students_full_points'] /
                         results[year]['students_amount'] * 100)
            del results[year]['points']
            del results[year]['percents']
        self.annual_averages = results


class EntryAnnualShortInfo(EntryAnnualFullInfo):
    def finalize(self):
        super().finalize()
        del self.students