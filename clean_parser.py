import html.parser
from urllib.request import urlopen

class CoursesHTMLParser(html.parser.HTMLParser):
    def __init__(self):
        super().__init__()
        self.li = False

    def handle_starttag(self, tag, attrs):
        if tag == 'li':
            self.li = True

    def handle_endtag(self, tag):
        if tag == 'li':
            self.li = False

    def handle_data(self, data):
        if self.li:
            print(data)
if __name__ == '__main__':
    raw_html = urlopen('http://anytask.urgu.org').read().decode('utf-8')
    CoursesHTMLParser().feed(raw_html)
