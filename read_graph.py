import networkx as nx
import pickle

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

#Ratio of t1 and t2 nodes in DRN
t1_ratio = 0.01
t2_ratio = 0.05

G = nx.read_gml('inputDRN.gml')

G = read(G)

#print("Before ", G.nodes())
G = makedirected(G)
G = nx.convert_node_labels_to_integers(G, first_label = 0)
#print("After ", G.nodes())

allNodes = [u for u in G.nodes()]
t1 = allNodes[:int(t1_ratio * len(G))]
t2 = allNodes[int(t1_ratio * len(G)):int(t1_ratio * len(G)) + int(t2_ratio * len(G))]
t3 = [u for u in G.nodes() if u not in t1 and u not in t2]

print (len(t1),len(t2),len(t3))
print (t1, t2)
pickle.dump(t1,open('HO.p','wb'))
pickle.dump(t2,open('SO.p','wb'))
pickle.dump(t3,open('NO.p','wb'))

nx.write_gml(G,"labeled_DRN.gml")