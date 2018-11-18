import os
import networkx as nx
import pickle
from constants import input_grn, data_directory


def generate_GRN_edge_directions_reversed(input_grn):
    G1 = nx.read_gml(input_grn)
    G1 = G1.reverse()
    G1 = nx.convert_node_labels_to_integers(G1,first_label = 0)
    nx.write_gml(G1, data_directory + 'yeast_grn_reversed.gml')
    return G1

def compute_GRN_NSM_NMC(G):
    # Node motif centrality
    NMC = {}
    # List of nodes sharing motif (NSM) with current node
    NSM = [[] for _ in G.nodes()]

    for u in G.nodes():
        NMC[u] = 0

    # For directed graphs
    if G.is_directed():
        for u in G.nodes():

            # print ("Node:",u)
            for v in G.nodes():
                for w in G.nodes():

                    if G.has_edge(u, v) and G.has_edge(v, w) and G.has_edge(u, w):
                        NMC[u] += 1
                        NMC[v] += 1
                        NMC[w] += 1

                        if v not in NSM[u]:
                            NSM[u].append(v)

                        if w not in NSM[u]:
                            NSM[u].append(w)

                        if u not in NSM[v]:
                            NSM[v].append(u)

                        if w not in NSM[v]:
                            NSM[v].append(w)

                        if u not in NSM[w]:
                            NSM[w].append(u)

                        if v not in NSM[w]:
                            NSM[w].append(v)

    # For undirected graphs
    else:
        for u in G.nodes():
            for v in G.nodes():
                if v <= u:
                    continue
                for w in G.nodes():
                    if w <= v:
                        continue

                    if G.has_edge(u, v) and G.has_edge(v, w) and G.has_edge(u, w):
                        NMC[u] += 1
                        NMC[v] += 1
                        NMC[w] += 1

    pickle.dump(NMC, open(data_directory + "NMC.p", "wb"))
    pickle.dump(NSM, open(data_directory + "NSM.p", "wb"))
    #return NMC, NSM


os.system('python construct_Orig_NepalDRN.py')
os.system('python construct_Orig_NepalDRN_network.py')
os.system('python create_ONE_setting_file.py')
#os.system('python3 construct_Bio_NepalDRN.py')

#------------- Make GRN ready for mapping with DRN - to create Bio-DRN
# input GRN with edge directions reversed
#G = generate_GRN_edge_directions_reversed(input_grn)
#compute_GRN_NSM_NMC(G)
