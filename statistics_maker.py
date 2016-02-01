import json
import glob
import os.path
import database


def build_task_database(files, handler):
    task_db = database.Database(handler)
    for filename in files:
        with open(filename, encoding='utf-8') as file:
            data = json.load(file)
        for task in data:
            task_db.add_entry(task)
    task_db.finalize()
    return task_db


def jdefault(o):
    if isinstance(o, set):
        return list(o)
    return o.__dict__

if __name__ == '__main__':
    files = glob.glob(os.path.join('courses', '*.json'))
    task_db = build_task_database(files, database.EntryFullInfo)
    open('db.json', 'w').write(json.dumps(task_db, default=jdefault,
                               ensure_ascii=False,
                               sort_keys=True))
    # for task in sorted(task_db):
    #    print('%s:\n%r\n' % (task, task_db[task]))
