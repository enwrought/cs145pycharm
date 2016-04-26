import Network
import networx as nx
import numpy as np
from sklearn.decomposition import PCA


class featurePCA:
    """
        network = Network object

        featureIDs = list of relevant features for PCA

        pca = PCA object for the input network on the input features

    """

    def __init__(self, network, featureIDs):
        self.network = network
        self.edgeList = nx.edges(network)
        self.featureIDs = featureIDs
        self.pca = featurePCA(netowrk, featureIDs)


    def filterByIndex(user, featureIDs):
        return [user[i] for i in featureIDs]

    # Inputs a network and a list of relevant feature ID's
    def featurePCA(network, featureIDs):

        featureList = network.features

        filteredList = [filterByIndex(user, featureIDs) for user in featureList]

        pca = PCA(n_components=len(featureIDs))
        pca.fit(filteredList)


