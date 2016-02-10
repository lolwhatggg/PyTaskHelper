import json
import glob
import os
import re


class CategoryDB:
    def __init__(self, db_filename, year):
        self.year = year
        self.tasks = self.get_tasks(db_filename)
        all_years = self.categorize_tasks(self.tasks)
        db_all_years = self.create_db(all_years)
        annual_tasks = self.get_annual_tasks()
        this_year = self.categorize_tasks(annual_tasks)
        db_this_year = self.create_db(this_year)
        self.db = {'all_years': db_all_years, 'this_year': db_this_year}

    def categorize_tasks(self, tasks):
        result = dict()
        for task in tasks:
            task_data = tasks[task]
            history = task_data['history']
            category = self.get_last_known_name(history)
            if self.year in history:
                result.setdefault(category, [])
                result[category].append(task_data)
        return result

    def get_last_known_name(self, history):
        last_year = max(history)
        return history.get(self.year, history[last_year])

    def get_annual_tasks(self):
        result = {}
        for task in self.tasks:
            annual_averages = self.tasks[task]['annual_averages']
            this_year = [t for t in annual_averages
                         if t['year'] == self.year]
            if not this_year:
                continue
            this_year = this_year[0]
            result[task] = self.tasks[task]
            result[task].update(this_year)
            del result[task]['annual_averages']
        return result

    def create_db(self, categories):
        result = {}
        for cat in categories:
            if cat == 'common':
                continue
            data = categories[cat]
            result[cat] = self.create_entry(data)
        return result

    def create_entry(self, data):
        return {
            'max_students': self.get_max(data, 'students_amount'),
            'min_students': self.get_min(data, 'students_amount'),
            'max_percent': self.get_max(data, 'average_percent'),
            'min_percent': self.get_min(data, 'average_percent'),
            'max_points': self.get_max(data, 'average_points'),
            'min_points': self.get_min(data, 'average_points'),
            'max_full_points': self.get_max(data, 'students_full_points'),
            'min_full_points': self.get_min(data, 'students_full_points')
        }

    @staticmethod
    def get_tasks(db_filename):
        with open(db_filename, encoding='utf-8') as file:
            tasks = json.load(file)
        return tasks

    @staticmethod
    def get_max(data, field):
        return max((task[field], task['name']) for task in data)

    @staticmethod
    def get_min(data, field):
        return min((task[field], task['name']) for task in data)

if __name__ == '__main__':
    files = glob.glob(os.path.join('../courses', '*.json'))
    for file in files:
        year = file.split(' ')[-1].strip().replace('.json', '')
        db = CategoryDB('../database/categories.json', year).db
        path = '../database/categories/%s.json' % year
        with open(path, 'w', encoding='utf-8') as file:
            file.write(json.dumps(db, ensure_ascii=False,
                                  indent=4, sort_keys=True))
