import Network
import networkx as nx
import numpy as np
from sklearn.decomposition import PCA


class featurePCA:
    """
        network = Network object

        edgeList = list of edges in graph

        featureIDs = list of relevant features for PCA

        pca = PCA object for the input network on the input features

    """

    def __init__(self, network, featureIDs):
        self.network = network
        self.edgeList = nx.edges(network)
        self.featureIDs = featureIDs
        self.pca = featurePCA(network, featureIDs)

    # TODO: We need to make this a less hack-ish data structure and document it well
    def filterByIndex(self, user, featureIDs):
        """
            Helper function
            Returns a list
        """
        return [user[i] for i in featureIDs]

    def featurePCA(self, network, featureIDs):
        """
            Inputs a network and a list of relevant feature ID's
            Calculates PCA on input features
        """
        featureList = network.features.values()

        filteredList = [self.filterByIndex(user, featureIDs) for user in featureList]
        pca = PCA(n_components=len(featureIDs))
        pca.fit(filteredList)

    # TODO: Add relevant graphs
    def generateGraphs(self):
        pass
