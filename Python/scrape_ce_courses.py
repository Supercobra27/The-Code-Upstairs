import requests
from bs4 import BeautifulSoup
import re
import os

filepath = "C:\\Users\\Owner\\Documents\\Dev\\Knowledge"
link = "https://www.queensu.ca/academic-calendar/engineering-applied-sciences/academic-plans/mathematics-engineering/mathematics-engineering-basc-class-2026/"
http_text = requests.get(link).text # send GET request to website
pattern = re.compile(r'[\x00-\x1F\x7F-\x9F]')
filename = 'MTHECore'
course_deps = ['CISC', 'CMPE', 'ELEC', 'ENPH', 'PHYS', 'MTHE', 'MREN', 'APSC', 'CIVL', 'MNTC', 'MECH', 'MATH']

def filter_array(array, condition):
    return [element for element in array if condition(element)]


def sanitize_filename(filename):
    # Remove any invalid characters with regex
    return re.sub(r'[<>:"/\\|?*]', '_', filename)

class course:

    def __init__(self, bubble, course_code, course_name) -> None:
        self.bubble = bubble
        self.course_code = course_code
        self.course_name = course_name

    def getCourseDesc(self, bubble):
        c_link = 'https://www.queensu.ca'+bubble['href']
        bubble_text = requests.get(c_link).text
        bsoup = BeautifulSoup(bubble_text, 'lxml')
        course_desc = bsoup.find('section', class_='searchresults').find('div', class_='courseblockextra noindent').text
        return course_desc
    
    def getPreReqs(self, bubble):
        bubble_text = requests.get('https://www.queensu.ca'+bubble['href']).text
        bsoup = BeautifulSoup(bubble_text, 'lxml')
        course_reqs = bsoup.find('section', class_='searchresults').find('span', class_='detail-requirements').text.split('Requirements: ')[1].split('Corequisites')[0]
        course_reqs = filter_array(course_reqs.split(' '), lambda x: any(sub in x for sub in course_deps))
        for i in range(len(course_reqs)):
            course_reqs[i] = ''.join(course_reqs[i][0:8].split('\xa0'))
            if '(' in course_reqs[i]:
                course_reqs[i].replace('(', 'C')
        return course_reqs
    
    def generatePreReqChart(self, bubble, file):
        preReqs = self.getPreReqs(bubble)
        print('```mermaid\nstateDiagram\n', file=file)
        for req in preReqs:
            print(f'{req}-->{self.course_code}', file=file)
        print('```', file=file)

    def __str__(self):
        return f"\n### [{self.course_code}]({'https://www.queensu.ca'+self.bubble['href']}) - {self.course_name}\n{self.getCourseDesc(self.bubble)}\n"

class courseTable:
    courses: list[course] = []

    def __init__(self, table) -> None:
        self.html_table = table

    def searchCourses(self):    
        courses_html = self.html_table.find_all('tr')
        self.courses = []
        for course_html in courses_html:
            course_html = course_html.find_all('td')
            bubble = course_html[0].find('a', class_='bubblelink', href=True)
            course_code = ''.join(course_html[0].text.split('\xa0'))
            self.courses.append(course(bubble, course_code, course_html[1].text))

tableArray: list[courseTable] = []

soup = BeautifulSoup(http_text, 'lxml')
tables = soup.find_all('tbody')

for table in tables:
    tableArray.append(courseTable(table))

with open(os.path.join(filepath, f'{filename}.md'), 'a', encoding="utf-8") as md:
    print('---\ntags:\n- QueensU\n---', file=md)
    for table in tableArray:
        table.searchCourses()
        for courses in table.courses:
            print(courses, file=md)
            courses.generatePreReqChart(courses.bubble, md)
            print('<div style="page-break-after: always;"></div>\n', file=md)

    print('Obsidian file generated!')
    
