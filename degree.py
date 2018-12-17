import sys

import matplotlib.pyplot as plt
import networkx as nx
import os
from constants import *

def deg(G):

    md = max([G.degree(u) for u in G.nodes()])

    Y = [0.0 for i in range(md + 1)]
    X = [i for i in range(md + 1)]

    for u in G.nodes():
        Y[G.degree(u)] += 1


    plt.plot(X,Y)
    plt.show()

def plot_deg_dist(G, filename):
    md = max([G.degree(u) for u in G.nodes()])

    Y = [0.0 for i in range(md + 1)]
    X = [i for i in range(md + 1)]

    for u in G.nodes():
        Y[G.degree(u)] += 1

    plt.figure()
    #plt.title("Nodes: " + str(len(G.nodes())) + " Edges: " + str(len(G.edges())) + " Fidelity: " + str(fidelity))
    #nx.draw(G, with_labels=True)
    # plt.xlabel('Degree')
    # plt.ylabel('Number of nodes')
    plt.plot(X, Y)
    plt.savefig(filename + ".png")
    plt.close()


#Main starts here
plot_directory = directory + "Plot/"
data_directory = directory +"Data/"
if not os.path.exists(plot_directory):
    os.makedirs(plot_directory)

for time in range(0, total_simulation_time, network_construction_interval):
    inputDRN = nx.read_gml(directory + "Orig_NepalDRN_" + str(time) + ".gml")
    plot_deg_dist(inputDRN, plot_directory + "Orig_deg_" + str(time))

    bioDRN = nx.read_gml(data_directory + 'GBD_' + str(time) + '.gml')
    plot_deg_dist(bioDRN, plot_directory + "GBD_deg_" + str(time))

#
# refG = nx.read_gml(folder + 'refG.gml')
# plot_deg_dist(refG, folder + "refG")
#
# origG = nx.read_gml('this_grn.gml')
# plot_deg_dist(origG, "origGRN")

## ================ MetroFi
# metroFi = nx.read_gml('metrofi.gml')
# plot_deg_dist(metroFi, "metroFi")
#
# bioMetroFi = nx.read_gml('GBD_metrofi.gml')
# plot_deg_dist(bioMetroFi, "bioMetroFi")
#
# refG_metroFi = nx.read_gml('refG_metrofi.gml')
# plot_deg_dist(refG_metroFi, "refG_metroFi")
#
# origG = nx.read_gml('this_grn.gml')
# plot_deg_dist(origG, "origGRN")

#GBD = nx.read_gml('inputDRN.gml')
#print ("Original DRN: Nodes", len(GBD))
#print ("Original DRN: Edges", len(GBD.edges()))
