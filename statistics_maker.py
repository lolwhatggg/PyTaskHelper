import json
import glob
import os.path
import database


def build_task_database(files, entry_class):
    task_db = database.Database(entry_class)
    for filename in files:
        with open(filename, encoding='utf-8') as file:
            data = json.load(file)
        for task in data:
            task_db.add_entry(task)
    if 'finalize' in dir(task_db):
        task_db.finalize()
    return task_db


def jdefault(o):
    if isinstance(o, set):
        return list(o)
    return o.__dict__

if __name__ == '__main__':
    files = glob.glob(os.path.join('courses', '*.json'))
    task_db = build_task_database(files, database.EntryOnlyAverageValues)
    dumped = json.dumps(task_db, ensure_ascii=False,
                        sort_keys=True, default=jdefault)
    with open('db.json', 'w', encoding='utf-8') as file:
        file.write(dumped)
