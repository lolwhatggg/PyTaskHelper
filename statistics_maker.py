import json
import glob
import os.path
from db_handlers import DBHandlerWithoutAnnotations, Database

KNOWN_ALIASES = {}


def build_task_database(files, handler):
    database = Database(handler)
    for filename in files:
        with open(filename, 'r', encoding='utf-8') as file:
            data = json.load(file)
            for task in data:
                database.add_entry(task)
    database.finalize()
    return database


if __name__ == '__main__':
    files = glob.glob(os.path.join('courses', '*.json'))
    db = build_task_database(files, DBHandlerWithoutAnnotations())
    for task in sorted(db):
        print('{}: {}'.format(task, db[task]))
