import json
import glob
import os.path
from db_handlers import DBHandlerWithoutAnnotations
KNOWN_ALIASES = {

}


def build_task_database(files, handler):
    database = {}
    for filename in files:
        with open(filename, 'r', encoding='utf-8') as file:
            data = json.load(file)
        for task in data:
            task_data = handler.parse_task(task)
            handler.add_entry(database, task_data)
        handler.finalize(database)
    return database


if __name__ == '__main__':
    files = glob.glob(os.path.join('courses', '*.json'))
    db = build_task_database(files, DBHandlerWithoutAnnotations())
    for task in sorted(db):
        print('{}: {}'.format(task, db[task]))
