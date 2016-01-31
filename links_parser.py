import re
from bs4 import BeautifulSoup
from urllib.request import urlopen

NAMES = 'Perltask', 'python.task'

with urlopen('http://anytask.urgu.org') as page:
    raw_html = page.read().decode()

links = BeautifulSoup(raw_html).find_all('li')

for link in filter(lambda x: any(name in x.text for name in NAMES), links):
    print('%s: %s' % (re.sub(r'\s+', '', link.text), URL + link.a['href']))
