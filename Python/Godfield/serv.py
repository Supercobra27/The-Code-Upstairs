from flask import Flask

app = Flask(__name__)

class Card:
    def __init__(value, element, mana, type):
            v = value
            e = element
            m = mana
            t = type
        

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"
