import json
import glob
import os.path
<<<<<<< HEAD
import db_handlers as dbh
from pprint import pprint, pformat

=======
import database
import pprint
>>>>>>> 32ce2dc6514aba10abfc4a021837db9712587f4d

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
<<<<<<< HEAD
    db = build_task_database(files, dbh.EntryWithoutAnnotations)
    for task in sorted(db):
        print('%s:\n%r\n' % (task, db[task]))
=======
    task_db = build_task_database(files, database.EntryWithPercentage)
    for task in sorted(task_db):
        pprint.pprint('{}: {}'.format(task, task_db[task]))
>>>>>>> 32ce2dc6514aba10abfc4a021837db9712587f4d
