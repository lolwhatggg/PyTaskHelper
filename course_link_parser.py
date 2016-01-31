import re
import html.parser
import urllib.error
from contextlib import closing
from urllib.request import urlopen

URL = 'http://anytask.urgu.org'


class Link:
    def __init__(self):
        self.href = ''
        self.name = ''

    def __str__(self):
        return '%s: %s' % (self.name, self.href)


class CoursesHTMLParser(html.parser.HTMLParser):
    def __init__(self):
        super().__init__()
        self._tags = dict.fromkeys(('li',), False)
        self.links = []

    def handle_starttag(self, tag, attrs):
        if tag == 'li':
            self._tags['li'] = True
            self.links.append(Link())
        elif tag == 'a' and self._tags['li']:
            self.links[-1].href = URL + dict(attrs)['href']

    def handle_endtag(self, tag):
        if tag == 'li':
            self._tags['li'] = False

    def handle_data(self, data):
        if self._tags['li']:
            data = re.sub(r'\s+', ' ', data).rstrip()
            if not data:
                return
            self.links[-1].name += data

    def get_some(self, *names):
        return filter(lambda link:
                      any(name in link.name for name in names),
                      self.links)


def main():
    try:
        with closing(urlopen(URL)) as page:
            raw_html = page.read().decode()
    except urllib.error as e:
        print('Cannot open url')
        print(e)
        return
    except IOError as e:
        print('Cannot read html')
        print(e)
        return
    except UnicodeDecodeError as e:
        print('Cannot decode html')
        print(e)
        return

    parser = CoursesHTMLParser()
    parser.feed(raw_html)
    print(list(map(str, parser.get_some('python.task', 'Perltask'))))

if __name__ == '__main__':
    main()
