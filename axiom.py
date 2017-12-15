import time
import json

import networkx as nx
from networkx.readwrite import json_graph
from fastecdsa import keys, curve

def keypair():
    priv_key = keys.gen_private_key(curve.secp256k1)
    pub_key = keys.get_public_key(priv_key, curve.secp256k1)
    return priv_key, pub_key
    
def axiom_paper():
    """
    Need to change key to actual public key.
    """
    #allows self loops need to fix this
    G = nx.DiGraph()
    node_data = {
        'link_1': '000000000000000000000000000000000',
        'link_2': '000000000000000000000000000000000',
        'pub': keypair()[1].x,
        'timestamp': time.time()}
    G.add_node('23b391d38e4827864257263921fae0fb', attr_dict=node_data)

    node_data_2 = {
        'link_1':'000000000000000000000000000000000',
        'link_2':'000000000000000000000000000000000',
        'pub': keypair()[1].x,
        'timestamp': time.time()
    }
    G.add_node('2ca8634aba5742cf565650e771cb70bd', attr_dict=node_data_2)

    crick_data = {
        'link_1':'23b391d38e4827864257263921fae0fb',
        'link_2':'2ca8634aba5742cf565650e771cb70bd',
        'pub': keypair()[1].x,
        'timestamp': time.time()
    }
    crick_addr = 'e4d8e61c260d6e053a1e32347dcd3d44'
    G.add_node(crick_addr, attr_dict=crick_data)
    
    G.add_edge(crick_addr, crick_data['link_1'], rev=1)
    G.add_edge(crick_addr, crick_data['link_2'], rev=1)


    graph_data = json_graph.node_link_data(G)
    json.dump(graph_data, open("force/tangle.json", "w"))

    pass

if __name__ == "__main__":
    axiom_paper()
    # json.load(open("tangle.json", "r"))
