# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.
import networkx as nx

class Network:
    """
        Stub for Netork class
        
        graph = NetworkX graph

        featureVec = [feature vector for each node in the graph]
            Vector of features as they appear in data

        featuresByName = {featurenames: [network_ids with true as the features]}
        
        edgeWeights = distance of edges in the graph in data space 
            (by default uncomputed as {})
            (indexed by network edge object edges)
    """

    def __init__(self, featureVec, featuresByName, networkx_obj, all_pairs_edges = {}):
        self.featureVec = featureVec
        self.featureByName = featuresByName
        self.graph = networkx_obj
        self.edgeWeights = all_pairs_edges

        # If no edge weights were provided, calculate using default function
        if (all_pairs_edges == {}):
            self.edgeWeights = mutualFriendDist(networkx_obj)

        # Add edge weights to networx object
        nx.set_edge_attributes(self.graph, 'graph_distance', self.edgeWeights)

    # Calculate edge distances in graph as inverse of number of mutual friends
    def mutualFriendDist(graph):
        # edge list for input graph
        edges = nx.edges(graph)

        # weights = {edge : weight}
        weights = {}

        # calculate edge weight and add to dictionary
        for edge in edges:
            num_mutual = float(len(nx.common_neighbors(graph, edge[0], edge[1])))
            weight = 1 / (1 + num_mutual)
            weights[edge] = weight

        return weights

