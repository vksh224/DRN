from computeHarvesine import *
import networkx as nx
from degree import *
import pickle

def makedirected(G):

    H = nx.DiGraph()
    H.add_nodes_from(G.nodes())

    for e in G.edges():
        H.add_edge(e[0],e[1])
        H.add_edge(e[1],e[0])

    return H

def create_static_network(filename):
    wifi_range = 1000

    with open(filename) as f:
        apslocations = f.readlines()

    #Initialize graph
    G = nx.Graph()

    # add nodes
    for ap in apslocations:
        mac_id = ap.split()
        G.add_node(mac_id[0])

    #add edges
    for ap1 in apslocations:
        ap1_arr = ap1.split()
        u = ap1_arr[0]
        lat1 = ap1_arr[1]
        lon1 = ap1_arr[2]

        for ap2 in apslocations:
            ap2_arr = ap2.split()
            v = ap2_arr[0]
            lat2 = ap2_arr[1]
            lon2 = ap2_arr[2]

            dist = funHaversine(float(lon1), float(lat1), float(lon2), float(lat2))

            if dist <= wifi_range and u != v:
                G.add_edge(u, v)
                G[u][v]['weight'] = 1

    print ("Number of nodes in G: ",len(G))
    print ("Number of edges in G: ",len(G.edges()))
    print ("Density of G: ",(2 * len(G.edges()))/(len(G) * (len(G) - 1)))

    return G


G = create_static_network("metrofi/aps.txt")
G = nx.convert_node_labels_to_integers(G,first_label = 0)
nx.write_gml(G, "metrofi.gml")

#Ratio of t1 and t2 nodes in DRN
t1_ratio = 0.02
t2_ratio = 0.1

#G = nx.read_gml('metrofi.gml')
G = makedirected(G)
#deg(G)

allNodes = [u for u in G.nodes()]

t1 = allNodes[:int(t1_ratio * len(G))]
t2 = allNodes[int(t1_ratio * len(G)):int(t1_ratio * len(G)) + int(t2_ratio * len(G))]
t3 = [u for u in G.nodes() if u not in t1 and u not in t2]

print (len(t1),len(t2),len(t3))
pickle.dump(t1,open('metro_HO.p','wb'))
pickle.dump(t2,open('metro_SO.p','wb'))
pickle.dump(t3,open('metro_NO.p','wb'))

nx.write_gml(G, "labeled_metrofi.gml")
