import requests
from bs4 import BeautifulSoup
import re
import os
from dataclasses import dataclass
from enum import Enum
from keybert import KeyBERT
import pandas as pd

"""
Add ability to scrape transcripts and recommend the best classes to each person, classify them based on scores of industry
How do I want to store it?
"""

COURSE_REQUIREMENTS = ['prerequisite', 'exclusion', 'exclusions']

class Faculty(Enum):
    ELEC = 0
    CISC = 1

@dataclass
class grad_course:
    faculty: Faculty
    name: str
    desc: str
    keywords: list[str] = None
    prereqs: str = None

def find_faculty(course_title: str) -> Faculty:
    course_title[0:3] = ""
    return Faculty.ELEC

def fix_desc(http_course: str) -> str:
    course_desc = http_course.text.replace('\xa0', ' ').replace('\n', ' ')
    course_desc = re.sub(r'\s+', ' ', course_desc).strip()
    return course_desc

grad_courses: list[grad_course] = []

link = "https://www.queensu.ca/academic-calendar/graduate-studies/courses-instruction/elec/"
http_text = requests.get(link).text
soup = BeautifulSoup(http_text, 'lxml')
kw_model = KeyBERT()

courses = soup.find(id = 'textcontainer').find_all('p') # returns an array

for http_course in courses:
    
    # Check if title exists
    if http_course.strong:
        title = http_course.strong.extract().text
    else:
        continue
    
    # Remove all versions of <br>
    if http_course.br:
        for br in http_course.find_all('br'):
            br.decompose()
            
    course_desc = fix_desc(http_course)
    for word in COURSE_REQUIREMENTS:
        if word in course_desc.lower():
            course_prereqs = course_desc.lower().split(word)[1]
            
    #course_keywords = kw_model.extract_keywords(course_desc, keyphrase_ngram_range=(1, 2), top_n=5)
    course_keywords = []
    curr = grad_course(Faculty.ELEC, title, course_desc, course_keywords, course_prereqs)
    grad_courses.append(curr)
    
for course in grad_courses:
    print(course.name)
