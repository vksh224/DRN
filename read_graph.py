import networkx as nx
import pickle
import matplotlib.pyplot as plt
from Centrality import motif

def plot_graph(G, filename):
    plt.figure()
    plt.title("Nodes: " + str(len(G.nodes())) + " Edges: " + str(len(G.edges())))
    nx.draw(G, with_labels=True)
    # plt.xlabel('Degree')
    # plt.ylabel('Number of nodes')
    plt.draw()
    plt.savefig("Plots/" + filename + "_" + str(len(G.nodes())) + ".png")
    plt.close()


def makedirected(G):
    H = nx.DiGraph()
    H.add_nodes_from(G.nodes())

    for e in G.edges():
        H.add_edge(e[0],e[1])
        H.add_edge(e[1],e[0])

    return H

def read(G):
    mapping = {}
    a = 0
    s = 0

    #Add hubs and sub hubs
    for u in G.nodes():
        #If node id is less than 1000, it is an amenity (a)
        if int(u) > 1000:
            mapping[u] = a
            a = a + 1

    #Add non hubs
    for u in G.nodes():
        # If node id is greater than 1000, it is a shelter-point(s)
        mapping[u] = a
        a = a + 1

    H = nx.relabel_nodes(G, mapping)

    return H

folder = "kathmandu/"
#Ratio of t1 and t2 nodes in DRN
t1_ratio = 0.02
t2_ratio = 0.08

G = nx.read_gml(folder + 'inputDRN.gml')
print("Original DRN Nodes:", len(G.nodes()))
print("Original DRN Edges:", len(G.edges()))
print("Original DRN isConnected:", nx.number_connected_components(G))

G = read(G)

#print("Before ", G.nodes())
G = makedirected(G)
G = nx.convert_node_labels_to_integers(G, first_label = 0)
#print("After ", G.nodes())

#Non-increasing motif central nodes
MC_G = motif(G)
MC_G = [each[0] for each in sorted(MC_G.items(), key=lambda x: x[1], reverse=True)]
allNodes = MC_G

#Non-increasing degree central nodes
# degrees = G.degree()
# allNodes = [each[0] for each in sorted(degrees.items(), key=lambda x: x[1], reverse=True)]

t1 = allNodes[:int(t1_ratio * len(G))]
t2 = allNodes[int(t1_ratio * len(G)):int(t1_ratio * len(G)) + int(t2_ratio * len(G))]
t3 = [u for u in G.nodes() if u not in t1 and u not in t2]

print("Cardinality of DRN tier nodes", len(t1),len(t2),len(t3))
print("DRN tier 1 and 2 nodes", t1, t2)
print("DRN tier 1 and 2 degree", [G.degree(u) for u in t1], [G.degree(u) for u in t2])

pickle.dump(t1, open(folder + 'HO.p','wb'))
pickle.dump(t2, open(folder + 'SO.p','wb'))
pickle.dump(t3, open(folder + 'NO.p','wb'))

nx.write_gml(G, folder + "labeled_DRN.gml")
plot_graph(G, "labeled_DRN2")