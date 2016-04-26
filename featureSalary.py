import Network
import networx as nx
import numpy as np


class featureSalary:
    """
        Analyze graphs based with salary as only node feature. Assumes salaries is 
        stored in the featureVec parameter of the input Network object.

        network = Network object

        edgeList = list of edges in graph

    """

    def __init__(self, network):

        self.network = network
        self.edgeList = nx.edges(network)
        self.salEdgeWeights = getSalEdgeWeights(network.graph, network.featuresVec)

        # Add salary ratio weights to networx object
        nx.set_edge_attributes(network.graph, 'salary_ratio', self.salEdgeWeights)

    # Takes in a graph and dictionary of salaries.
    # salaries = {node_id : salary}
    # sets edge weights as ratio of salaries between connected nodes
    def getSalEdgeWeights(graph, salaries):
        edges = nx.edges(graph)

        for edge in edges:
            ratio = float(salaries[edge[0]]) / salaries[edge[1]]
            ratio = min(ratio, 1 / ratio)
            salRatioEdges[edge] = ratio
        
        return salRatioEdges


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