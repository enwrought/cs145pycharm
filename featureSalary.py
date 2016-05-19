import networkx as nx
import numpy as np
import scipy
import scipy.stats
import math
import bisect
import matplotlib.pyplot as plt
from scipy.stats import chisquare


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

        """
            self.edgeWeights
        """
        self.salEdgeWeights = self.getSalEdgeWeights(network.graph, network.featureVec)
        self.salPairWeights = self.getSalPairWeights(network.graph, network.featureVec)

        # Add salary ratio weights to networkx object

        # Again we don't use this yet
        # nx.set_edge_attributes(network.graph, 'salary_ratio', self.salEdgeWeights)

        self.salVals = network.featureVec.values()
        # self.edgeWeights = network.edgeWeights

        # List of positive indices
        print('filtering...')
        print len(self.salEdgeWeights)
        print len(self.salPairWeights)
        self.positive_income = filter(lambda x: self.salVals[x] > 0, xrange(len(self.salVals)))

        """
            self.network.edgeWeights().values()
        """
        self.positive_sal_edge_weights = filter(lambda x: self.salEdgeWeights.values()[x] > 0,
                                                xrange(len(self.salEdgeWeights)))
        self.positive_sal_pair_weights = filter(lambda x: self.salPairWeights.values()[x] > 0,
                                                xrange(len(self.salPairWeights)))

        print('filtered')
        self.generateGraphs()

    # TODO: pass in a "metric" lambda function instead of automatically defaulting to minRatio
    def getSalPairWeights(self, graph, salaries):
        """
            Takes in a graph and dictionary of salaries.
            salaries = {node_id : salary}
            sets edge weights as ratio of salaries between connected nodes

            If either of the salaries are 0, then we set it to some negative value we can filter

        """
        nodes = nx.nodes(graph)

        salRatioPairs = {}

        for i in xrange(len(nodes)):
            for j in xrange(len(nodes[i+1:])):
                pair = (nodes[i], nodes[j])
                ratio = abs(salaries[nodes[i]] - salaries[nodes[j]])
                if salaries[nodes[i]] < 0 or salaries[nodes[j]] < 0:
                    # Set to some negative value we can filter
                    ratio = -1.0
                salRatioPairs[pair] = ratio
        return salRatioPairs


    def getSalEdgeWeights(self, graph, salaries):
        """
            Takes in a graph and dictionary of salaries.
            salaries = {node_id : salary}
            sets edge weights as ratio of salaries between connected nodes

            If either fo the salaries are 0, then we set it to some negative value we can filter
        """
        edges = nx.edges(graph)

        salRatioEdges = {}
        for edge in edges:
            # ratio = float(salaries[edge[0]]) / salaries[edge[1]]
            # ratio = min(ratio, 1 / ratio)
            ratio = abs(salaries[edge[0]] - salaries[edge[1]])
            if salaries[edge[0]] < 0 or salaries[edge[1]] < 0:
                # Set to some negative value we can filter
                ratio = -1.0
            salRatioEdges[edge] = ratio
        return salRatioEdges


    def index(self, a, x):
        'Locate the leftmost value exactly equal to x'
        i = bisect.bisect_left(a, x)
        if i != len(a) and a[i] == x:
            return i
        raise ValueError

    def find_le(self, a, x):
        'Find rightmost value less than or equal to x'
        i = bisect.bisect_right(a, x)
        if i:
            return a[i-1]
        raise ValueError


    def getChiSquare(self, salEdges, sal_percentile_edges, salPairs, sal_percentile_pairs):
        expected = []
        for i in salEdges:
            val = self.find_le(salPairs, i)
            index = self.index(salPairs, val)
            expected.append(sal_percentile_pairs[index])

        chisq, p = chisquare(sal_percentile_edges, expected)

        return (chisq, p)



    # TODO: Have a generic graph function that supports plot arguments and saving files instead of repeating 4 times
    def generateGraphs(self):
        print('generating graphs')
        # edgeWeights and salEdges only include people that have salary information
        # pairWeights = map(lambda x: self.network.pairWeights.values()[x], self.positive_pair_weights)
        salPairs = map(lambda x: self.salPairWeights.values()[x], self.positive_sal_pair_weights)

        # Edge weights corresponding to the positive salary edge weights
        edgeWeights = map(lambda x: self.network.edgeWeights.values()[x], self.positive_sal_edge_weights)
        salEdges = map(lambda x: self.salEdgeWeights.values()[x], self.positive_sal_edge_weights)

        salVals = map(lambda x: self.salVals[x], self.positive_income)

        # Histogram of edge weights from network
        fig1 = plt.figure(1)
        plt.hist(edgeWeights)
        plt.xlabel('Weight')
        plt.ylabel('Frequency')
        plt.title('Mutual Friend Frequencies')
        plt.savefig(self.network.name + '_freq_mutual_friends.png')
        plt.close(fig1)

        # Histogram of salaries of all nodes
        fig2 = plt.figure(2)
        plt.hist(salVals, bins=40)
        plt.xlabel('Salary')
        plt.ylabel('Frequency')
        plt.title('Salary Frequencies')
        plt.savefig(self.network.name + '_freq_salary.png')
        plt.close(fig2)

        # Histogram of salary ratios along edges
        fig3 = plt.figure(3)
        plt.hist(salEdges)
        plt.xlabel('Salary Differences on Edges')
        plt.ylabel('Frequency')
        plt.title('Salary Difference (USD)')
        plt.savefig(self.network.name + '_freq_salary_diff.png')
        plt.close(fig3)

        fig4 = plt.figure(4)
        # TODO: double check that .values() returns the same order
        fit = np.polyfit(edgeWeights, salEdges, 1)
        slope, intercept, r_value, p_value, std_err = scipy.stats.linregress(edgeWeights, salEdges)
        print "salEdges = %f * edgeWeights + %f" % (fit[0], fit[1])
        print "(m, b, R^2, p, std_err) = (%f, %f, %f, %f, %f)" % (slope, intercept, r_value ** 2, p_value, std_err)
        fit_fn = np.poly1d(fit)
        plt.plot(edgeWeights, salEdges, 'ro', edgeWeights, fit_fn(edgeWeights), '--k')
        plt.xlabel('Mutual Friends')
        plt.ylabel('Salary Difference')
        plt.title('Mutual Friends vs Salary Differences')
        plt.savefig(self.network.name + '_mutual_friends_salary_diff.png')
        plt.close(fig4)

        fig5 = plt.figure(5)
        # heatmap, xedges, yedges = np.histogram2d(self.network.edgeWeights.values(),
        #                                          self.salEdgeWeights.values(), bins=50)
        # extent = [xedges[0], xedges[-1], yedges[0], yedges[-1]]
        # plt.imshow(heatmap, extent=extent)
        plt.hexbin(edgeWeights, salEdges, gridsize=40, bins=15)
        cb = plt.colorbar()
        plt.xlabel('Mutual Friends')
        plt.ylabel('Salary Difference')
        plt.title('Mutual Friends vs Salary Differences')
        plt.savefig(self.network.name + '_heatmap.png')
        plt.close(fig5)

        fig6 = plt.figure(6)
        plt.hexbin(edgeWeights, salEdges, gridsize=(25, 10), bins=15)
        plt.axis([min(edgeWeights), 50, min(salEdges), 20])
        cb = plt.colorbar()
        plt.xlabel('Mutual Friends')
        plt.ylabel('Salary Difference')
        plt.title('Mutual Friends vs Salary Differences')
        plt.savefig(self.network.name + '_heatmap_zoomed.png')
        plt.close(fig6)

        fig7 = plt.figure(7)
        sorted_edge_weights = sorted(edgeWeights)
        edge_weights_percentile = map(lambda x: float(x)/len(sorted_edge_weights), xrange(len(sorted_edge_weights)))
        plt.plot(sorted_edge_weights, edge_weights_percentile, 'b-')
        plt.xlabel('Mutual Friends Ratio')
        plt.ylabel('Percentile')
        plt.title('CDF of Social Distance')
        plt.savefig(self.network.name + '_cdf_mutual_friends.png')
        plt.close(fig7)

        fig8 = plt.figure(8)
        sorted_salaries = sorted(salVals)
        salaries_percentile = map(lambda x: float(x) / len(sorted_salaries), xrange(len(sorted_salaries)))
        plt.plot(sorted_salaries, salaries_percentile, 'b-')
        plt.xlabel('Annual income (thousands)')
        plt.ylabel('Percentile')
        plt.title('CDF of Salary')
        plt.savefig(self.network.name + '_cdf_salary.png')
        plt.close(fig8)

        plt.figure(9)
        """
            # TODO: Address that some friends have 0 mutual friends
        """
        """ sorted_edge_weights = map(lambda x: math.log(x), sorted(edgeWeights))
        edge_weights_percentile = map(lambda x: math.log(1 - float(x) / len(sorted_edge_weights)),
                                      xrange(len(sorted_edge_weights)))
        plt.plot(sorted_edge_weights, edge_weights_percentile, 'b-')
        plt.xlabel('log (# mutual friends)')
        plt.ylabel('log P(#mutual friends > x)')
        plt.title('Log-Log Rank Plot of Social Distance')
        """

        fig10 = plt.figure(10)
        sorted_salaries = map(lambda x: math.log(x), sorted(salVals))
        salaries_percentile = map(lambda x: math.log(1 - float(x) / len(sorted_salaries)), xrange(len(sorted_salaries)))
        plt.plot(sorted_salaries, salaries_percentile, 'b-')
        plt.xlabel('Log (Annual income)')
        plt.ylabel('log P(Salary > x)')
        plt.title('Log-Log Rank Plot of Salary')
        plt.savefig(self.network.name + '_rank_salary.png')
        plt.close(fig10)

        fig11 = plt.figure(11)
        salEdges2 = filter(lambda x: x > 0, salEdges)
        sorted_salary_diff = map(lambda x: math.log(x), sorted(salEdges2))
        salary_diff_percentile = map(lambda x: math.log(1 - float(x) / len(sorted_salary_diff)),
                                     xrange(len(sorted_salary_diff)))
        plt.plot(sorted_salary_diff, salary_diff_percentile, 'b-')
        plt.xlabel('Log (Salary Difference)')
        plt.ylabel('log P(Salary Difference > x)')
        plt.title('Log-Log Rank Plot of Salary Differences')
        plt.savefig(self.network.name + '_rank_salary_diff.png')
        plt.close(fig11)

        fig12 = plt.figure(12)
        salEdges2 = sorted(salEdges2)
        sal_percentile_edges = map(lambda x: float(x) / len(salEdges2),
                                     xrange(len(salEdges2)))
        plt.plot(salEdges2, sal_percentile_edges, 'b-')
        plt.xlabel('Salary difference')
        plt.ylabel('Percentile')
        plt.title('CDF of Salary Difference')
        plt.savefig(self.network.name + '_cdf_salary_diff.png')
        plt.close(fig12)

        fig13 = plt.figure(13)
        salPairs = sorted(salPairs)
        sal_percentile_pairs = map(lambda x: float(x) / len(salPairs),
                                           xrange(len(salPairs)))
        plt.plot(salPairs, sal_percentile_pairs, 'b-')
        plt.xlabel('Salary difference (thousands)')
        plt.ylabel('Percentile')
        plt.title('CDF of Salary Difference on Node Pairs')
        plt.savefig(self.network.name + '_cdf_all_pairs_salary_diff.png')
        plt.close(fig13)

        plt.figure(14)
        plt.plot(salEdges2, sal_percentile_edges, label='Edges')
        plt.plot(salPairs, sal_percentile_pairs, label='Pairs')
        plt.xlabel('Salary difference (thousands)')
        plt.ylabel('Percentile')
        plt.title('CDF of Salary Difference on Node Pairs and Edges')
        plt.legend()


        print self.getChiSquare(salEdges, sal_percentile_edges, salPairs, sal_percentile_pairs)

        plt.show()
