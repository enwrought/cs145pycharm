# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.
import networkx as nx


class Network:
    """
        Stub for Network class
        
        graph = NetworkX graph

        featureVec

        used to be [feature vector for each node in the graph]
        is now a single vector of salaries for each node
            Vector of features as they appear in data

        featuresByName = {featurenames: [network_ids with true as the features]}
        
        edgeWeights = distance of edges in the graph in data space 
            (by default uncomputed as {})
            (indexed by network edge object edges)
    """

    def __init__(self, featureVec, featuresByName, networkx_obj, all_pairs_edges={}):
        self.featureVec = featureVec
        self.featureByName = featuresByName
        self.graph = networkx_obj

        # If no edge weights were provided, calculate using default function
        self.edgeWeights = (self.mutualFriendDist(networkx_obj)
                            if not all_pairs_edges else all_pairs_edges)

        # Add edge weights to networkx object

        # Right now we never use any of the networkX attributes, so there is no point in wasting memory
        # nx.set_edge_attributes(self.graph, 'graph_distance', self.edgeWeights)

    # TODO: maybe change this to editing self.all_pairs_edges directly (instead of a static function)
    # TODO: pass a lambda function as a parameter metric of distance
    def mutualFriendDist(self, graph):
        """
            Calculate edge distances in graph as inverse of number of mutual friends
        """
        # edge list for input graph
        edges = nx.edges(graph)

        # weights = {edge : weight}
        weights = {}

        # calculate edge weight and add to dictionary
        for edge in edges:
            num_mutual = float(len(sorted(nx.common_neighbors(graph, edge[0], edge[1]))))
            weight = 1 / (1 + num_mutual)
            weights[edge] = weight

        return weights

