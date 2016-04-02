# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.
import networkx as nx

class Network:
    """
        Stub for Netork class
        
        networkx_obj = NetworkX graph
        features = {featurenames: [network_ids with true as the features]}
        
        all_pairs_edges = distance of edges in the graph in data space 
            (by default uncomputed as {})
            (indexed by network edge object edges)
    """
    def __init__(self, features, networkx_obj, all_pairs_edges = {}):
        self.features = features
        self.networkx_obj = networkx_obj
        self.all_pairs_edges = all_pairs_edges
    