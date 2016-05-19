# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.
import networkx as nx
import featureSalary
import math


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

    def __init__(self, featureVec, featuresByName, networkx_obj, name):
        self.featureVec = featureVec
        self.featureByName = featuresByName
        self.graph = networkx_obj

        # If no edge weights were provided, calculate using default function
        self.edgeWeights = self.get_social_edge_distances(networkx_obj)

        self.pairWeights = self.get_all_pairs_social_distances(networkx_obj)

        self.salaries = featureSalary.FeatureSalary(self)
        self.name = name
        # Add edge weights to networkx object

        # Right now we never use any of the networkX attributes, so there is no point in wasting memory
        # nx.set_edge_attributes(self.graph, 'graph_distance', self.edgeWeights)

    # TODO: maybe change this to editing self.all_pairs_edges directly (instead of a static function)
    # TODO: pass a lambda function as a parameter metric of distance
    def get_social_edge_distances(self, graph):
        """
            Calculate edge distances in graph as inverse of number of mutual friends

            @param{nx.Network object}{graph}
        """
        # edge list for input graph
        edges = nx.edges(graph)

        # weights = {edge : weight}
        weights = {}

        # calculate edge weight and add to dictionary
        for edge in edges:
            weight = self.__ratio_mutual_friends_product(graph, edge)
            weights[edge] = weight

        return weights

    def get_all_pairs_social_distances(self, graph):
        """
            Calculate distances in graph as inverse of number of mutual friends
            over all pairs of nodes, including non-connected ones

            @param{nx.Network object}{graph}
        """
        nodes = nx.nodes(graph)

        weights = {}

        for i in range(len(nodes)):
            for j in range(len(nodes[i+1:])):
                pair = (nodes[i], nodes[j])
                weight = self.__ratio_mutual_friends_product(graph, pair)
                weights[pair] = weight

        return weights

    def __num_mutual_friends(self, graph, edge):
        return len(sorted(nx.common_neighbors(graph, edge[0], edge[1])))

    """
    # We don't use this right now

    def __ratio_mutual_friends(self, graph, edge):
        intersection = len(sorted(nx.common_neighbors(graph, edge[0], edge[1])))
        union = len(set(nx.neighbors(graph, edge[0])) | set(nx.neighbors(graph, edge[1])))
        return float(intersection) / union
    """

    def __ratio_mutual_friends_product(self, graph, edge):
        intersection = len(sorted(nx.common_neighbors(graph, edge[0], edge[1])))
        union = len(nx.neighbors(graph, edge[0])) * len(nx.neighbors(graph, edge[1]))
        return float(intersection) / math.sqrt(union)

