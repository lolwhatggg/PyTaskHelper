import html.parser
from urllib.request import urlopen
from contextlib import closing
import re

URL = 'http://anytask.urgu.org'


class CoursesHTMLParser(html.parser.HTMLParser):
    def __init__(self):
        super().__init__()
        self.li = False
        self.name = []
        self.href = ''
        self.links = []

    def handle_starttag(self, tag, attrs):
        if tag == 'li':
            self.li = True
        elif tag == 'a' and self.li:
            self.href = URL + dict(attrs)['href']

    def handle_endtag(self, tag):
        if tag == 'li':
            self.links.append((' '.join(self.name), self.href))
            self.li = False
            self.name = []
            self.href = ''

    def handle_data(self, data):
        if self.li:
            data = re.sub(r'\s+', ' ', data).strip()
            if data:
                self.name.append(data)


    def find_perl_or_py_courses(self):
        courses = {}
        for course in self.links:
            if 'python.task' in course[0] or 'Perltask' in course[0]:
                courses[course[0]]=course[1]
        return courses


if __name__ == '__main__':
    with closing(urlopen(URL)) as page:
        raw_html = page.read().decode()
    parser = CoursesHTMLParser()
    parser.feed(raw_html)
    print(parser.find_perl_or_py_courses())