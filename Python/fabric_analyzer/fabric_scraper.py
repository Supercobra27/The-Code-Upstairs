from fabric_functions import create_yt_note
from dotenv import load_dotenv
import pandas as pd
from flask import Flask
import os

load_dotenv()

gfilepath = os.getenv('GFILEPATH')
test = pd.read_csv('test.csv')

for index, row in test.iterrows():
    create_yt_note(gfilepath, row)

app = Flask(__name__)
        
@app.route("/")
def hello_world():
    return test