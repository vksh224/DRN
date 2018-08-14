import networkx as nx

def read(G):

    mapping = {}
    a = 0
    s = 0


    for u in G.nodes():

        #If node id is less than 1000, it is an amenity (a)
        if int(u) > 1000:
            mapping[u] = 'a' + str(a)
            a = a + 1

        # If node id is greater than 1000, it is a shelter-point(s)
        else:
            mapping[u] = 's' + str(s)
            s = s + 1

    H = nx.relabel_nodes(G,mapping)

    return H

#Ratio of t1 and t2 nodes in DRN
t1_ratio = 0.01
t2_ratio = 0.1

G = nx.read_gml('inputDRN.gml')
G = read(G)

hubs = [u for u in G.nodes() if 's' in u]

t1 = hubs[:int(t1_ratio * len(G))]
t2 = hubs[int(t1_ratio * len(G)):int(t1_ratio * len(G)) + int(t2_ratio * len(G))]
t3 = [u for u in G.nodes() if u not in hubs]

print (len(t1),len(t2),len(t3))