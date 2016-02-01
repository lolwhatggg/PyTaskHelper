import os
import re
import bs4
import json
import linksparser
import html
from urllib.request import urlopen


def parse_results(table):
    results = []
    for a in table.findAll('tr'):
        fields = a.findAll('td')
        data = {
            'student': fields[0].text.strip(),
            'points': get_points(fields[2]),
            'comment': get_comment(fields[2]),
            'date': fields[1].text.strip()
        }
        results.append(data)
    return results


def get_points(field):
    points = field.text.strip()
    if '.' in points:
        points = 0
    return int(points)


def get_comment(field):
    if not field.a:
        return ''
    js = field.a['href']
    comment = js[js.index('\'') + 1:-2]
    comment = html.unescape(comment)
    comment = re.sub(r'<br/>\s*', '\n', comment)
    return comment.strip()


def write_course(link):
    with urlopen(link['href']) as page:
        raw_html = page.read().decode()

    soup = bs4.BeautifulSoup(raw_html, 'html.parser')
    tasks = soup.find('tbody').findChildren(recursive=False)

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
            results = parse_results(task.table)
            db.append({'category': 'common','name': name, 'max': int(maximum), 'students': results})
        else:
            for st in task.findAll('font'):
                if st.previous.name != 'div':
                    continue
                name = st.text.strip()
                category = base_name
                maximum = st.findNext('span').text.strip()
                results = parse_results(st.findNext('table'))
                db.append({'category': category, 'name': name, 'max': int(maximum), 'students': results})

    directory = os.path.join('courses', '%s.%s' % (link['name'], 'json'))
    with open(directory, 'w', encoding='utf-8') as file:
        file.write(json.dumps(db, ensure_ascii=False,
                              indent=4, sort_keys=True))


if __name__ == '__main__':
    anytask = linksparser.AnyTask()
    for link in anytask.get_courses('python.task', 'Perltask'):
        print(link['name'])
        write_course(link)
