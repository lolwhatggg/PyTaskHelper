import os
import re
import bs4
import json
import html
import linksparser
from urllib.request import urlopen

COURSES = 'python.task', 'Perltask'


def write_course(link):
    with urlopen(link['href']) as page:
        raw_html = page.read().decode()
    soup = bs4.BeautifulSoup(raw_html)
    tasks = soup.find('tbody').findChildren(recursive=False)
    year = link['name'].split('|')[-1].strip()
    db = parse_tasks(tasks, year)
    filename = link['name'].replace('| ', '')
    directory = os.path.join('../courses', '%s.%s' % (filename, 'json'))
    with open(directory, 'w', encoding='utf-8') as file:
        file.write(json.dumps(db, ensure_ascii=False,
                              indent=4, sort_keys=True))


def parse_tasks(tasks, year):
    db = []
    for task in tasks:
        if not isinstance(task, bs4.Tag):
            continue
        task = task.td
        base_name = task.strong.text.strip()
        next_tag = task.strong.next_sibling.next_sibling.name
        if next_tag == 'span':
            name = base_name
            maximum = task.span.text.strip()
            results = parse_results(task.table, year)
            db.append({'category': None, 'name': name,
                       'max': int(maximum), 'students': results,
                       'year': year})
        else:
            for st in task.findAll('font'):
                if st.previous.name != 'div':
                    continue
                name = st.text.strip()
                category = base_name
                maximum = st.findNext('span').text.strip()
                results = parse_results(st.findNext('table'), year)
                db.append({'category': category, 'name': name,
                           'max': int(maximum), 'students': results,
                           'year': year})
    return db


def parse_results(table, year):
    results = []
    for a in table.findAll('tr'):
        fields = a.findAll('td')
        data = {
            'student': fields[0].text.strip(),
            'first_date': fields[1].text.strip(),
            'second_date': get_second_date(fields),
            'points': get_points(fields[2]),
            'comment': get_comment(fields[2]),
            'year': year
        }
        results.append(data)
    return results


def get_second_date(fields):
    field_one = fields[2].text.strip()
    field_two = fields[3].text.strip()
    return field_one if '.' in field_one else field_two


def get_points(field):
    points = field.text.strip()
    return 0 if '.' in points else int(points)


def get_comment(field):
    if not field.a:
        return ''
    js = field.a['href']
    comment = js[js.index('\'') + 1:-2]
    comment = html.unescape(comment)
    comment = re.sub(r'<br/>\s*', '\n', comment)
    return comment.strip()


if __name__ == '__main__':
    anytask = linksparser.AnyTask()
    for link in anytask.get_courses(*COURSES):
        write_course(link)
