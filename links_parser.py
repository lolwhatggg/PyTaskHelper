import re
from bs4 import BeautifulSoup
from urllib.request import urlopen

URL = 'http://anytask.urgu.org'
NAMES = 'Perltask', 'python.task'

with urlopen(URL) as page:
    raw_html = page.read().decode()

links = BeautifulSoup(raw_html).find_all('li')

for li in filter(lambda x: any(name in x.text for name in NAMES), links):
    print('%s: %s' % (re.sub(r'\s+', '', li.text), URL + li.a['href']))
