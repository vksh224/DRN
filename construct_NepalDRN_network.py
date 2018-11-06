import networkx as nx
import pickle

from constants import *
from construct_NepalDRN_utility import *

def responder_visiting_IDs():
    # Get CC and PoI IDs that each responder visits
    Res_visiting_IDs_list = []

    for k in range(len(Res_paths)):
        Res_visiting_IDs = []
        for loc in Res_paths[k]:
            for i in range(len(CC_locs)):
                if loc == CC_locs[i]:
                    Res_visiting_IDs.append(i)
                    break
            for j in range(len(PoI_locs)):
                if loc == PoI_locs[j]:
                    Res_visiting_IDs.append(len(CC_locs) + j)
                    break
        # print("Res locs", k, Res_paths[k])
        print("Res ", k, Res_visiting_IDs)
        Res_visiting_IDs_list.append(Res_visiting_IDs)

    return Res_visiting_IDs_list

#Get links between tier 1 and tier 2 nodes
def get_tier1_tier2_links(G, Res_visiting_IDs_list):
    for res in Res_visiting_IDs_list:
        for u in res:
            for v in res:
                if u != v and G.has_edge(u, v) == False:
                    G.add_edge(u, v)
                    #G.add_edge(v, u)

def create_static_network(Res_visiting_IDs_list, start_time, end_time):
    G = nx.DiGraph()

    #Add DRN nodes
    for id in CC_IDs:
        G.add_node(id)
    for id in PoI_IDs:
        G.add_node(id)
    for id in Vol_IDs:
        G.add_node(id)
    for id in S_IDs:
        G.add_node(id)

    print("Prev: # Nodes", len(G))

    get_tier1_tier2_links(G, Res_visiting_IDs_list)

    #Add edges between each pair of nodes for the given time interval
    with open(loc_des_folder + "ext_position.txt", "r") as f:
        node_pos_lines = f.readlines()[1:]

    for line1 in node_pos_lines:
        line1_arr = line1.strip().split(" ")
        line1_arr = [int(ele) for ele in line1_arr]

        for line2 in node_pos_lines:
            line2_arr = line2.strip().split(" ")
            line2_arr = [int(ele) for ele in line2_arr]

            # u != v, and start_time < t(u), t(v) <= end_time, and t(u) == t(v) and dist(u, v) < range
            if line1_arr[1] != line2_arr[1] \
                and line1_arr[0] > start_time and line1_arr[0] <= end_time \
                and line2_arr[0] > start_time and line2_arr[0] <= end_time \
                and line1_arr[0] == line2_arr[0] \
                and euclideanDistance(line1_arr[2], line1_arr[3], line2_arr[2], line2_arr[3]) <= bt_range:

                #print(line1_arr[1], line2_arr[1])
                G.add_edge(line1_arr[1], line2_arr[2])

    print("# Nodes", G.nodes())
    print("# Edges", len(G.edges()))
    print("Density:", float(len(G.edges()) * 2) / (len(G) * (len(G) - 1)))

    return G




#Main Starts here

#Get CC, PoI, Vol, S, Res (in this order for node ID)
CC_locs = pickle.load(open(directory + "Data/CC_locs.p", "rb"))
PoI_locs = pickle.load(open(directory + "Data/PoI_locs.p", "rb"))
Vol_locs = pickle.load(open(directory + "Data/Vol_locs.p", "rb"))
S_locs = pickle.load(open(directory + "Data/S_locs.p", "rb"))
Res_paths = pickle.load(open(directory + "Data/Res_paths.p", "rb"))

#Except survivors
CC_IDs = [i for i in range(len(CC_locs))]
PoI_IDs = [i for i in range(len(CC_locs), len(CC_locs) + len(PoI_locs))]
Vol_IDs = [i for i in range(len(CC_locs) + len(PoI_locs), len(CC_locs) + len(PoI_locs) + len(Vol_locs))]
S_IDs = [i for i in range(len(CC_locs) + len(PoI_locs) + len(Vol_locs), len(CC_locs) + len(PoI_locs) + len(Vol_locs) + len(S_locs))]

print("last node_id", S_IDs[len(S_IDs) - 1])
Res_visiting_IDs_list = responder_visiting_IDs()

start_time = 0
end_time = 1500

G = create_static_network(Res_visiting_IDs_list, start_time, end_time)

