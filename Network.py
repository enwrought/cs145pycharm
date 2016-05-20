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

    def __init__(self, featureVec, featuresByName, networkx_obj, all_pairs_edges={}):
        self.featureVec = featureVec
        self.featureByName = featuresByName
        self.graph = networkx_obj

        # If no edge weights were provided, calculate using default function
        self.edgeWeights = (self.friend_dist(networkx_obj)
                            if not all_pairs_edges else all_pairs_edges)

        self.pairWeights = (self.pair_dist(networkx_obj)
                            if not all_pairs_edges else all_pairs_edges)

        self.salaries = featureSalary.FeatureSalary(self)
        # Add edge weights to networkx object

        # Right now we never use any of the networkX attributes, so there is no point in wasting memory
        # nx.set_edge_attributes(self.graph, 'graph_distance', self.edgeWeights)

    # TODO: maybe change this to editing self.all_pairs_edges directly (instead of a static function)
    # TODO: pass a lambda function as a parameter metric of distance
    def friend_dist(self, graph):
        """
            Calculate edge distances in graph as inverse of number of mutual friends
        """
        # edge list for input graph
        edges = nx.edges(graph)

        # weights = {edge : weight}
        weights = {}

        # calculate edge weight and add to dictionary
        for edge in edges:
            weight = self.__scaled_mutual_friends(graph, edge)
            weights[edge] = weight

        return weights

    def pair_dist(self, graph):
        """
            Calculate distances in graph as inverse of number of mutual friends
            over all pairs of nodes
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

    def __ratio_mutual_friends(self, graph, edge):
        intersection = len(sorted(nx.common_neighbors(graph, edge[0], edge[1])))
        union = len(set(nx.neighbors(graph, edge[0])) | set(nx.neighbors(graph, edge[1])))
        return float(intersection) / union

    def __ratio_mutual_friends_product(self, graph, edge):
        intersection = len(sorted(nx.common_neighbors(graph, edge[0], edge[1])))
        union = len(nx.neighbors(graph, edge[0]))  * len(nx.neighbors(graph, edge[1]))
        return float(intersection) / math.sqrt(union)

    def __scaled_mutual_friends(self, graph, edge):
        num_mutual = len(sorted(nx.common_neighbors(graph, edge[0], edge[1])))
        A = num_mutual / float(len(nx.neighbors(graph, edge[0])))
        B = num_mutual / float(len(nx.neighbors(graph, edge[1])))

        return num_mutual * math.sqrt(A * B) + 1

