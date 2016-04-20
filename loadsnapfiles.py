# Load files from SNAP (https://snap.stanford.edu/data/) into NetworkX
import sys
import os
import re
import networkx as nx

import Network


def get_valid_networks(directory):
    """ 
        @param {string} dir
        
        Looks through the directory and returns a dictionary of valid network 
        files.  Run as a precaution.
        
        Each network must have the files
        network_id.edges
        network_id.circles
        network_id.feat
        network_id.egofeat
        network_id.featnames
    """
    networks = {}
    # remove the extension
    for FILE in os.listdir(directory):
        network, ext = re.split('\.', FILE)
        if network in networks:
            networks[network][ext] = True
        else:
            networks[network] = {ext: True}
    
    # check which ones are valid
    valid_network_ids = []
    for network_id in networks:
        network = networks[network_id]
        if all(filetype in network for filetype in 
                ['edges', 'circles', 'feat', 'egofeat', 'featnames']):
            valid_network_ids.append(network_id)
    
    return list(set(valid_network_ids))
    

def load_files(directory, network_id):
    """
        @param {string} dir - Directory of files
        @param {string} networkid - network id (file name, without extensions)
        
        @throws ValueError if the files have improper sizes
        Loads the data into the classes
        Returns a new class 
   """
    edges_file = open("%s/%s.edges" % (directory, network_id))
    circles_file = open("%s/%s.circles" % (directory, network_id))
    feat_file = open("%s/%s.feat" % (directory, network_id))
    egofeat_file = open("%s/%s.egofeat" % (directory, network_id))
    featnames_file = open("%s/%s.featnames" % (directory, network_id))
    
    # Read in graph information
    def split_line(x):
        return tuple(re.split(' |\t', x.strip()))
    
    g = nx.Graph()
    lis = [split_line(line) for line in edges_file]
    g.add_edges_from(lis)
    # g.add_edges_from(split_line(line) for line in edges_file)

    # g_edges = g.edges()
    # missing_edges = [line if line not in g_edges and (line[1], line[0]) not in g_edges else None for line in lis]
    # sum(0 if value == None else 1 for value in missing_edges) = 0
    g.add_edges_from((network_id, circle_id) for circle_id in
                     re.split('\t', circles_file.read().strip())[1:])
    
    # Read in features
    feature_names = [line.strip() for line in featnames_file]
    featuresName = {name: [] for name in feature_names}
    featuresName['data'] = []

    # Vector of features as they appear in data
    featuresVec = []
    featuresVec.append(map(int, egoFeats))
    
    # Features for network_id
    # features = { feature_name1: [network_ids that are True for feature_name1],
    #              feature_name2: [network_ids that are True for feature_name2], ...}
    featuresName['data'].append(network_id)

    def to_bool(x):
        return False if x == '0' else True

    network_id_feat_values = map(to_bool, split_line(egofeat_file.read()))
    
    # Safety check for valid files
    if len(network_id_feat_values) != len(feature_names):
        # error
        raise Exception('Wrong size of features.')
    
    for i in xrange(len(network_id_feat_values)):
        featuresName[feature_names[i]].append(network_id_feat_values[i])
    
    # Repeat for other nodes (besides network_id) in network
    for line in feat_file:
        tmp = split_line(line)
        feat_id = tmp[0]
        feats = tmp[1:]

        # TODO: these are mostly False, so we should just have a sparse representation
        featuresName['data'].append(feat_id)
        featuresVec.append(map(int, feats))
        feat_values = map(to_bool, feats)
        
        if len(feat_values) != len(feature_names):
            # error
            raise Exception('Wrong size of features.')
    
        for i in xrange(len(feat_values)):
            featuresName[feature_names[i]].append(feat_values[i])
    
    # Done!
    
    network = Network.Network(featuresVec, featuresName, g)

    edges_file.close()
    circles_file.close()
    feat_file.close()
    egofeat_file.close()
    featnames_file.close()
    
    return network
    # pass


def load_networks(directory):
    network_ids = get_valid_networks(directory)
    print 'Loading information from networks: ' + ','.join(network_ids)
    networks = []
    for network_id in network_ids:
        try:
            networks.append(load_files(sys.argv[1], network_id))
        except Exception as e:
            print "Network %s failed with error: %s." % (network_id, e)
    print networks


if __name__ == "__main__":
    print("Loading SNAP files")
    if len(sys.argv) != 2:
        print "Format: %s directory" % sys.argv[0]
    else:
        load_networks(sys.argv[1])