import Network
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt


class FeatureSalary:
    """
        Analyze graphs based with salary as only node feature. Assumes salaries is 
        stored in the featureVec parameter of the input Network object.

        self.network = Network object

        self.edgeList = list of edges in graph

    """

    def __init__(self, network):

        self.network = network
        # 1) We don't use this. 2) This is definitely wrong
        # self.edgeList = nx.edges(network)
        self.salEdgeWeights = self.getSalEdgeWeights(network.graph, network.featuresVec)

        # Add salary ratio weights to networkx object
        nx.set_edge_attributes(network.graph, 'salary_ratio', self.salEdgeWeights)

    # TODO: pass in a "metric" lambda function instead of automatically defaulting to minRatio
    def getSalEdgeWeights(self, graph, salaries):
        """
            Takes in a graph and dictionary of salaries.
            salaries = {node_id : salary}
            sets edge weights as ratio of salaries between connected nodes
        """
        edges = nx.edges(graph)

        salRatioEdges = {}
        for edge in edges:
            ratio = float(salaries[edge[0]]) / salaries[edge[1]]
            ratio = min(ratio, 1 / ratio)
            salRatioEdges[edge] = ratio
        return salRatioEdges

    # TODO: assign the values to self.salVals, self.salRatios, and self.edgeWeights
    # TODO: Have a generic graph function that supports plot arguments and saving files instead of repeating 4 times
    def generateGraphs(self):
        plt.figure(1)
        plt.hist(self.salEdgeWeights)
        plt.xlabel('Weight')
        plt.ylabel('Frequency')
        plt.title('Weight Frequencies')

        plt.figure(2)
        plt.hist(self.salVals)
        plt.xlabel('Salary')
        plt.ylabel('Frequency')
        plt.title('Salary Frequencies')

        plt.figure(3)
        plt.hist(self.salRatios)
        plt.xlabel('Salary Ratios on Edges')
        plt.ylabel('Frequency')
        plt.title('Salary Ratio on Edge Frequencies')

        plt.figure(4)
        plt.plot(self.edgeWeights, self.salRatios, 'ro')
        plt.xlabel('Edge Weights')
        plt.ylabel('Salary Ratios')
        plt.title('Edge Weights vs Salary Ratios')

        plt.show()
