from fabric_functions import create_yt_note
from dotenv import load_dotenv
import pandas as pd
import os

load_dotenv()

gfilepath = os.getenv('GFILEPATH')
test = pd.read_csv('test.csv')
for index, row in test.iterrows():
    create_yt_note(gfilepath, row)