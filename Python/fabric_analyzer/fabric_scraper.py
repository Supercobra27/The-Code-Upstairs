from fabric_functions import run_shell_command, check_directory, create_yt_note
import pandas as pd

gfilepath = 'C:\\Users\\Owner\\Documents\\Dev\\Knowledge'
test = pd.read_csv('test.csv')
for index, row in test.iterrows():
    create_yt_note(gfilepath, row)