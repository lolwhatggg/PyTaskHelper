import json
import glob
import os.path
import database
import pprint

def build_task_database(files, handler):
    task_db = database.Database(handler)
    for filename in files:
        with open(filename, encoding='utf-8') as file:
            data = json.load(file)
        for task in data:
            task_db.add_entry(task)
    task_db.finalize()
    return task_db


if __name__ == '__main__':
    files = glob.glob(os.path.join('courses', '*.json'))
    task_db = build_task_database(files, database.EntryWithPercentage)
    for task in sorted(task_db):
        pprint.pprint('{}: {}'.format(task, task_db[task]))
