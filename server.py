import os
from os import path
import sys
import logging
import hashlib
import json

from flask import Flask
from flask import render_template
from flask import send_from_directory
from flask import request

from networkx.readwrite import json_graph

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
        self.hash = _paper_hash(paper_path)

def _paper_hash(paper_path, BUF_SIZE = 65536):
    md5 = hashlib.md5()
    with open(paper_path, 'rb') as fp:
        while True:
            data = fp.read(BUF_SIZE)
            if not data:
                break
            md5.update(data)
    return md5.hexdigest()

def load_papers():
    papers = os.listdir("Papers")
    logger.info(papers)
    return (Paper(path.join("Papers", p)) for p in papers if not \
        p.startswith("."))

def load_tangle():
    """
    Reads tangle.json and loads as networkx object. 

    Returns:
    Graph: networkx graph object of tangle.
    """
    graph_data = json.load(open("tangle.json", "rb"))
    tangle = json_graph.node_link_graph(graph_data)
    return tangle

def update_tangle(tangle, paper, link_1, rev_1,  link_2, rev_2, pub):
    """
    Adds a paper to the tangle.

    Args:
    tangle: tangle graph
    paper: Paper object
    link_1: hash of paper to review
    rev_1: review of paper 1
    link_2: hash of other paper to review
    rev_2: review of paper 2
    pub: public key of submitter
    """
    data = {
        'link_1': link_1,
        'link_2': link_2,
        'pub': pub
            }
    #add node to graph
    tangle.add_node(paper, attr_dict=data)
    tangle.add_edge(paper, link_1, rev=rev_1)
    tangle.add_edge(paper, link_1, rev=rev_1)

    #dump new version of tangle
    graph_data = json_graph.node_link_data(G)
    json.dump(graph_data, open("tangle.json", "wb"))

    pass

@app.route('/')
def welcome():
    return render_template('index.html')

@app.route('/submit')
def submit_form():
    return render_template('submit.html')

@app.route('/submitted', methods=['POST', 'GET'])
def submit_paper():
    if request.method == "POST":
        result = request.form
        tangle = load_tangle()

        paper_hash = result['hash']
        pub = result['pub_key']
        link_1 = result['link_1']
        link_2 = result['link_2']
        rev_1 = result['rev_1']
        rev_2 = result['rev_2']

        update_tangle(tangle, paper_hash, link_1, rev_1, \
            link_2, rev_2, pub)

        return render_template("submitted.html", result=result)
    pass

@app.route('/papers')
def paper_list():
    papers = load_papers()
    return render_template('papers.html', papers=papers)

@app.route('/Papers/<p_id>')
def send_pdf(p_id=None):
    return send_from_directory('Papers', p_id )

@app.route('/<path:path>')
def tangle(path):
    """
    Needs to take tangle graph object
    """
    return app.send_static_file(path)

if __name__ == "__main__":
    app.run()
