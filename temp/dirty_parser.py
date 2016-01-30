import re
from urllib.request import urlopen

def get_autolinks():
    finder = re.compile('<li>(.*?)</li>', re.DOTALL)
    raw_html = urlopen('http://anytask.urgu.org').read().decode('utf-8')
    all_courses = re.findall(finder, raw_html)
    courses_dict = {}
    for course_link in all_courses:
        if 'python.task' in course_link or 'Perltask' in course_link:
            clean_line = re.sub(r'\s', '', course_link)
            year, link = split_course_line(clean_line)
            courses_dict[year] = link
    print(courses_dict)

def split_course_line(line):
    ahref_link, years = line.split('|')
    year = years.split('-')[0]
    link = 'http://anytask.urgu.org' + re.findall('<ahref="(.*?)">', ahref_link)[0]
    return year, link


def get_handmade_links():
    return {
        '2009': 'http://anytask.urgu.org/course/3',
        '2010': 'http://anytask.urgu.org/course/2',
        '2011': 'http://anytask.urgu.org/course/1',
        '2012': 'http://anytask.urgu.org/course/11',
        '2013': 'http://anytask.urgu.org/course/21',
        '2014': 'http://anytask.urgu.org/course/34',
    }


if __name__ == '__main__':
    get_autolinks()
