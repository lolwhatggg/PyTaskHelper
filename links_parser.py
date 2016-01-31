import re
from bs4 import BeautifulSoup
from contextlib import closing
from urllib.request import urlopen

URL = 'http://anytask.urgu.org'
NAMES = 'Perltask', 'python.task'

with closing(urlopen(URL)) as page:
    raw_html = page.read().decode()

links = BeautifulSoup(raw_html).find_all('li')
filtered = filter(lambda x: any(name in x.text for name in NAMES), links)

for li in filtered:
    print('%s: %s' % (re.sub(r'\s+', '', li.text), URL + li.a['href']))
