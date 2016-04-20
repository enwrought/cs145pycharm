import numpy as np
import math
from sklearn.decomposition import PCA


class FeaturePCA:
    def __init__(self, features, featureIDs):
        """
            @:param{features}{list} - Network.feature_vec object
            @:param{featureIDs}{list} - List of feature IDs

            Initializes and combines the PCA.
        """
        # TODO: add parameter to allow passing advanced options to PCA
        def filterByIndex(user, featureIDs):
            return [user[i] for i in featureIDs]

        featureList = features
        filteredList = [filterByIndex(user, featureIDs) for user in featureList]
        self.pca = PCA(n_components=len(featureIDs))
        self.pca.fit(filteredList)

    def generate_PCA_graph(self, filename):
        """
            Creates the graph of the points in PCA space and saves to 'filename'
        """
        pass

    def get_distances(self, metric=lambda coord1, coord2: math.sqrt((coord1-coord2)*(coord1-coord2))):
        """
            Returns a list of distances (in PCA space)
            @:param{metric}{function} - Metric for distances between two points (default Euclidean)
        """
        pass
