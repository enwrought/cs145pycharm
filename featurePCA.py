import Network
import numpy as np
from sklearn.decomposition import PCA

def filterByIndex(user, featureIDs):
    return [user[i] for i in featureIDs]

# Inputs a network and a list of relevant feature ID's
def featurePCA(network, featureIDs):

    featureList = network.features

    filteredList = [filterByIndex(user, featureIDs) for user in featureList]

    pca = PCA(n_components=len(featureIDs))
    pca.fit(filteredList)
