import Network
import networx as nx
import numpy as np


class featureSalary:
    """
        network = Network object

        edgeList = list of edges in graph

    """

    def __init__(self, network):
        self.network = network
        self.edgeList = nx.edges(network)


    def generateGraphs():
        plt.figure(1)
        plt.hist(edgeWeights)
        plt.xlabel('Weight')
        plt.ylabel('Frequency')
        plt.title('Weight Frequencies')

        plt.figure(2)
        plt.hist(salVals)
        plt.xlabel('Salary')
        plt.ylabel('Frequency')
        plt.title('Salary Frequencies')

        plt.figure(3)
        plt.hist(salRatios)
        plt.xlabel('Salary Ratios on Edges')
        plt.ylabel('Frequency')
        plt.title('Salary Ratio on Edge Frequencies')

        plt.figure(4)
        plt.plot(edgeWeights, salRatios, 'ro')
        plt.xlabel('Edge Weights')
        plt.ylabel('Salary Ratios')
        plt.title('Edge Weights vs Salary Ratios')


        plt.show()