import json
import glob
import os
import re


class CategoryDB:
    def __init__(self, db_filename, year):
        self.year = year
        self.tasks = self.open_task_db(db_filename)
        self.categorized_tasks = self.categorize_tasks(self.tasks, year)
        db_all_years = self.create_db(self.categorized_tasks)

        self.this_year_tasks = self.get_annual_tasks()
        self.categorized_tasks_this_year = \
            self.categorize_tasks(self.this_year_tasks, year)
        db_this_year = self.create_db(self.categorized_tasks_this_year)
        db = {'all_years': db_all_years, 'this_year': db_this_year}
        self.write_db(db, '../database/categories/' + year + '.json')

    def categorize_tasks(self, tasks, year):
        result = dict()
        for task in tasks:
            task_data = tasks[task]
            history = task_data['history']
            category = self.get_last_known_name(history, year)
            if year in task_data['history']:
                if category in result:
                    result[category].append(task_data)
                else:
                    result[category] = [task_data]
        return result

    def get_annual_tasks(self):
        result = {}
        for task in self.tasks:
            if self.year in self.tasks[task]['annual_averages']:
                result[task] = self.tasks[task]
                result[task].update(self.tasks[task]['annual_averages'][self.year])
                del result[task]['annual_averages']
        return result

    def create_db(self, categories):
        result = dict()
        for cat in categories:
            if cat == 'common':
                continue
            data = categories[cat]
            result[cat] = self.create_entry(data)
        return result

    def create_entry(self, data):
        entry = {
            'max_students': self.get_max_value(data, 'students_amount'),
            'min_students': self.get_min_value(data, 'students_amount'),
            'max_percent': self.get_max_value(data, 'average_percent'),
            'min_percent': self.get_min_value(data, 'average_percent'),
            'max_points': self.get_max_value(data, 'average_points'),
            'min_points': self.get_min_value(data, 'average_points')
        }
        max_full_points, name = self.get_max_value(data,
                                                   'students_full_points')
        percent, students = self.get_info_about_task(name)
        entry['max_full_points'] = {'students_full_points': max_full_points,
                                    'name': name, 'percent': percent,
                                    'students_amount': students}
        min_full_points, name = self.get_min_value(data,
                                                   'students_full_points')
        percent, students = self.get_info_about_task(name)
        entry['min_full_points'] = {'students_full_points': min_full_points,
                                    'name': name, 'percent': percent,
                                    'students_amount': students}
        return entry

    def get_info_about_task(self, name):
        task = self.tasks[name]
        percent = task['full_points_percent']
        students = task['students_amount']
        return percent, students

    @staticmethod
    def get_max_value(data, field):
        return max((task[field], task['name']) for task in data)

    @staticmethod
    def get_min_value(data, field):
        return min((task[field], task['name']) for task in data)

    @staticmethod
    def get_last_known_name(history, year):
        last_year = max(history)
        return history.get(year, history[last_year])

    @staticmethod
    def write_db(db, path):
        with open(path, 'w', encoding='utf-8') as file:
            file.write(json.dumps(db, ensure_ascii=False,
                                  indent=4, sort_keys=True))

    @staticmethod
    def open_task_db(db_filename):
        with open(db_filename, encoding='utf-8') as file:
            tasks = json.load(file)
        return tasks


if __name__ == '__main__':
    files = glob.glob(os.path.join('../courses', '*.json'))
    for file in files:
        year = file.split('/')[-1]
        year = re.sub('.json', '', year)
        CategoryDB('../database/db_cat.json', year)
