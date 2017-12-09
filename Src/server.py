import os

from flask import Flask
from flask import render_template

app = Flask(__name__)

class Paper:
    def __init__(self, p):
        self.href = 
    pass

def get_papers():
    papers = os.listdir("../Papers")

    
@app.route('/')
@app.route('/hello/<name>')
def hello_world(name=None):
    return render_template('hello.html', name=name)
