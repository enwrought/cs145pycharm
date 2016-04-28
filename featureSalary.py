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
        self.salEdgeWeights = self.getSalEdgeWeights(network.graph, network.featureVec)

        # Add salary ratio weights to networkx object

        # Again we don't use this yet
        # nx.set_edge_attributes(network.graph, 'salary_ratio', self.salEdgeWeights)

        self.salVals = network.featureVec.values()
        # self.edgeWeights = network.edgeWeights

        self.generateGraphs()

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
            # ratio = float(salaries[edge[0]]) / salaries[edge[1]]
            # ratio = min(ratio, 1 / ratio)
            ratio = abs(salaries[edge[0]] - salaries[edge[1]])
            salRatioEdges[edge] = ratio
        return salRatioEdges

    # TODO: Have a generic graph function that supports plot arguments and saving files instead of repeating 4 times
    def generateGraphs(self):
        edgeWeights = self.network.edgeWeights.values()
        salEdges = self.salEdgeWeights.values()
        # Histogram of edge weights from network
        plt.figure(1)
        plt.hist(edgeWeights)
        plt.xlabel('Weight')
        plt.ylabel('Frequency')
        plt.title('Mutual Friend Frequencies')

        # Histogram of salaries of all nodes
        plt.figure(2)
        plt.hist(self.salVals, bins=40)
        plt.xlabel('Salary')
        plt.ylabel('Frequency')
        plt.title('Salary Frequencies')

        # Histogram of salary ratios along edges
        plt.figure(3)
        plt.hist(salEdges)
        plt.xlabel('Salary Differences on Edges')
        plt.ylabel('Frequency')
        plt.title('Salary Difference on Edges Frequencies')

        plt.figure(4)
        # TODO: double check that .values() returns the same order
        plt.plot(edgeWeights, salEdges, 'ro')
        plt.xlabel('Mutual Friends')
        plt.ylabel('Salary Ratios')
        plt.title('Mutual Friends vs Salary Differences')


        plt.figure(5)
        # heatmap, xedges, yedges = np.histogram2d(self.network.edgeWeights.values(), self.salEdgeWeights.values(), bins=50)
        # extent = [xedges[0], xedges[-1], yedges[0], yedges[-1]]
        # plt.imshow(heatmap, extent=extent)
        plt.hexbin(edgeWeights, salEdges, gridsize=40, bins=15)
        cb = plt.colorbar()
        plt.xlabel('Mutual Friends')
        plt.ylabel('Salary Difference')
        plt.title('Mutual Friends vs Salary Differences')


        plt.figure(6)
        plt.hexbin(edgeWeights, salEdges, gridsize=(25,10), bins=15)
        plt.axis([min(edgeWeights), 50, min(salEdges), 20])
        cb = plt.colorbar()
        plt.xlabel('Mutual Friends')
        plt.ylabel('Salary Difference')
        plt.title('Mutual Friends vs Salary Differences')

        plt.figure(7)
        sorted_edge_weights = sorted(edgeWeights)
        edge_weights_percentile = map(lambda x: float(x)/len(sorted_edge_weights), xrange(len(sorted_edge_weights)))
        plt.plot(sorted_edge_weights, edge_weights_percentile, 'b-')
        plt.xlabel('Number of mutual friends')
        plt.ylabel('Percentile')
        plt.title('CDF of Social Distance')

        plt.figure(8)
        sorted_salaries = sorted(self.salVals)
        salaries_percentile = map(lambda x: float(x) / len(sorted_salaries), xrange(len(sorted_salaries)))
        plt.plot(sorted_salaries, salaries_percentile, 'b-')
        plt.xlabel('Annual income (thousands)')
        plt.ylabel('Percentile')
        plt.title('CDF of Salary')

        plt.show()
