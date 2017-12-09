import os
from os import path
import sys
import logging

from flask import Flask
from flask import render_template
from flask import send_from_directory

app = Flask(__name__)

logger = logging.getLogger('myapp')
hdlr = logging.FileHandler('axiom.log')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr) 
logger.setLevel(logging.INFO)

class Paper:
    def __init__(self, paper_path):
        self.href = paper_path
        self.title = path.basename(paper_path).split(".")[0]
def load_papers():
    papers = os.listdir("Papers")
    logger.info(papers)
    return (Paper(path.join("Papers", p)) for p in papers if not \
        p.startswith("."))

@app.route('/')
@app.route('/papers')
def paper_list():
    papers = load_papers()
    return render_template('papers.html', papers=papers)

@app.route('/Papers/<p_id>')
def send_pdf(p_id=None):
    return send_from_directory('Papers', p_id )
