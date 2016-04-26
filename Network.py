# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.
import networkx as nx

class Network:
    """
        Stub for Netork class
        
        graph = NetworkX graph
        features = {featurenames: [network_ids with true as the features]}
        
        edgeWeights = distance of edges in the graph in data space 
            (by default uncomputed as {})
            (indexed by network edge object edges)
    """
    def __init__(self, featureVec, featuresByName, networkx_obj, all_pairs_edges = {}):
        self.featureVec = featureVec
        self.featureByName = featuresByName
        self.graph = networkx_obj
        self.edgeWeights = all_pairs_edges

        if (all_pairs_edges == {}):
            self.edgeWeights = getDistances(networkx_obj)

        nx.set_edge_attributes(self.graph, 'graph_distance', self.edgeWeights)

    def getDistances(graph):
        # TODO: Calculate edge weights