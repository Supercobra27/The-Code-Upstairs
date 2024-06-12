import requests
from bs4 import BeautifulSoup
import re
import os


# Change your filepath here
filepath = "C:\\Users\\Owner\\Documents\\Dev\\Knowledge\\High Performance Computing\\COSS 2024\\"
filepath2 = os.path.join(filepath, 'courses\\')
http_text = requests.get("https://training.computeontario.ca/coss2024.php").text # send GET request to website

soup = BeautifulSoup(http_text, 'lxml')
rows = soup.find_all('tr')
checks = ['Level:', 'Length:', 'Format:', 'Prerequisites:']
pattern = re.compile(r'[\x00-\x1F\x7F-\x9F]')
count = 0
acc = 0

def sanitize_filename(filename):
    # Remove any invalid characters with regex
    return re.sub(r'[<>:"/\\|?*]', '_', filename)

def empty_directory(directory_path):
    try:
        # Iterate over all the files and subdirectories in the directory
        for filename in os.listdir(directory_path):
            file_path = os.path.join(directory_path, filename)
            # Check if the item is a file
            if os.path.isfile(file_path):
                # Remove the file
                os.remove(file_path)
            # Check if the item is a directory
            elif os.path.isdir(file_path):
                # Recursively call the function to empty the subdirectory
                empty_directory(file_path)
        # Remove the directory itself
        print(f"Directory emptied successfully.\n")
    except Exception as e:
        print(f"Error occurred while emptying directory '{directory_path}': {e}\n")

empty_directory(filepath)
if not os.path.exists(filepath2):
        os.makedirs(filepath2)

with open(os.path.join(filepath, 'COSS 2024 Courses.md'), 'w', encoding="utf-8") as main: #Open file
    open(os.path.join(filepath, 'COSS 2024 Courses.md')).close() #clear file
    print("# Course List", file=main) #print header
    for row in rows: #iterate over
        courses = row.find_all('div', class_='course')
        datas = row.find_all('td')
        if len(datas)>=3:
            dates = datas[1]
        else:
            continue

        for course in courses:
            title = sanitize_filename(course.find('h3').text)
            description_arr = row.find('div', class_="course-description")
            ul_list = row.find('div', class_="course-description").find_all('ul')
            description = description_arr.find_all('p')[0]

            with open(os.path.join(filepath2,f'{title}.md'), 'a', encoding="utf-8") as sub: # Create file for course
                print('---\ntags:\n- HPC\n---', file=sub)
                print('### Description', file=sub)
                for desc in description_arr.children:
                    desc_fix = re.sub(r'[�]', ' ', desc.text)
                    if any(desc_fix.startswith(item) for item in checks):
                        desc_fix = desc_fix.split(':')
                        desc_fix[0] = f"**{desc_fix[0]}**:"
                        desc_fix = "".join(desc_fix)
                        desc_fix = re.sub(pattern, ' ', desc_fix)
                        print(f'- {desc_fix}', file=sub)
                    else:
                        if any(desc.name == item for item in ['ul', 'ol']):
                            for li in desc:
                                print(f'{li.get_text()}', file=sub)
                                if 'Alliance Account' in li.text:
                                    print(f'Alliance Account required for --> {title}')
                                    count += 1
                                    acc = 1
                        else:
                            print(f'{desc_fix}', file=sub)
                print('### Lecture Notes', file=sub)

            print(f"## [[{title}]]", file=main) #print title
            if acc == 1:
                print('<p style="color:red;">Alliance Account Required</p>', file=main)
                acc = 0
            print(description.text, file=main) #print description
            print(f'\n**Dates**:\n{dates}', file=main)

print(f"\nAlliance Account required for {count} courses.\n")
