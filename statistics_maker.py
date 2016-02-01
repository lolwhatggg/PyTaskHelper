import json
import glob
import os.path
import db_handlers as dbh
from pprint import pprint, pformat


def build_task_database(files, handler):
    database = dbh.Database(handler)
    for filename in files:
        with open(filename, encoding='utf-8') as file:
            data = json.load(file)
        for task in data:
            database.add_entry(task)
    database.finalize()
    return database


if __name__ == '__main__':
    files = glob.glob(os.path.join('courses', '*.json'))
    db = build_task_database(files, dbh.EntryWithoutAnnotations)
    for task in sorted(db):
        print('%s:\n%r\n' % (task, db[task]))
