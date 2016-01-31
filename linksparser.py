import re
from bs4 import BeautifulSoup
from urllib.request import urlopen


class AnyTask:
    URL = 'http://anytask.urgu.org'
    NAMES = 'Perltask', 'python.task'

    def __init__(self):
        with urlopen(AnyTask.URL) as page:
            self.html = page.read().decode()
        self._links = BeautifulSoup(self.html).find_all('li')

    def get_py_and_perl(self):
        return filter(lambda x:
                      any(name in x['name'] for name in self.NAMES),
                      self.get_links())

    def get_links(self):
        links = []
        for link in self._links:
            name = re.sub(r'\s+', ' ', link.text).strip()
            href = self.URL + link.a['href']
            links.append({'name': name, 'href': href})
        return links
