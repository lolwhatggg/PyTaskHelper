import re
from bs4 import BeautifulSoup
from urllib.request import urlopen


class AnyTask:
    URL = 'http://anytask.urgu.org'

    def __init__(self):
        with urlopen(AnyTask.URL) as page:
            self.html = page.read().decode()
        self._links = BeautifulSoup(self.html).find_all('li')

    def get_courses(self, *courses):
        return filter(lambda x:
                      any(name in x['name'] for name in courses),
                      self.get_links())

    def get_links(self):
        links = []
        for link in self._links:
            name = re.sub(r'\s+', ' ', link.text).strip()
            href = self.URL + link.a['href']
            links.append({'name': name, 'href': href})
        return links
