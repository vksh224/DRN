import random
import math
import networkx as nx
from scipy.spatial.distance import *
from writeFile import *
#from turtle1 import *

#allocate each survivor to a unique PoI
def allocate_survivors():
    last_S_id = 0

    # PoI location
    for i in range(len(PoIs_loc)):
       #allocate each survivor in this PoI
        for j in range(PoI_S_count[i]):
            # random angle
            alpha = 2 * math.pi * random.random()
            r = poi_radius * math.sqrt(random.random())

            # calculating coordinates
            x = r * math.cos(alpha) + PoIs_loc[i][0]
            y = r * math.sin(alpha) + PoIs_loc[i][1]
            S_loc[j + last_S_id] = (x, y)

        #prev_S_id = last_S_id
        last_S_id += PoI_S_count[i]

        # print("PoI ", i,  PoIs_loc[i])
        # print("Survivors", PoI_S_count[i], [S_loc[j] for j in range(prev_S_id, last_S_id)])

#Get links between tier 1 and tier 2 nodes
def get_tier1_tier2_links(G):
    for res in responders:
        for u in res:
            for v in res:
                if u != v and G.has_edge(u, v) == False:
                    G.add_edge(u, v)
                    #G.add_edge(v, u)


def generate_Nepal_DRN():
    time_periods = 720
    loc_o = '0 ' + str(time_periods * 300) + " 0 " + str(X) + " 0 " + str(Y) + '\n'
    nei_o = '0 ' + str(time_periods * 300) + '\n'

    for i in range(time_periods):
        G = nx.DiGraph()

        node_id = 0

        # add CC
        for cc in CC_loc:
            G.add_node(node_id)
            CC_IDs.append(node_id)
            node_id += 1

        #add PoIs
        for poi in PoIs_loc:
            G.add_node(node_id)
            PoI_IDs.append(node_id)
            node_id += 1

        #add survivors
        for s in S_loc:
            G.add_node(node_id)
            S_IDs.append(node_id)
            node_id += 1

        print ("Largest node id (or # of nodes in the network): ", node_id)

        # add edges
        get_tier1_tier2_links(G)
        print("Tier 1 - 2 edges: ", G.edges())
        for u in G.nodes():
            #print(u, node_locs[u])
            for v in G.nodes():
                if u != v and euclidean(node_locs[u], node_locs[v]) <= bt_range:
                    G.add_edge(u,v)

        loc_o += writeC(node_locs, i)
        nei_o += writeF(G, i)

        print ("# Nodes", len(G))
        print ("# Edges", len(G.edges()))
        print ("Density:", float(len(G.edges()) * 2) / (len(G) * (len(G) - 1)))

    return G, loc_o, nei_o


#Main starts here
X = 10000
Y = 10000

#V = 200 # survivor only
poi_radius = 200

bt_range = 100
tower_range = 1000

CC_loc = [(2809, 4516)]
PoIs_loc = [(2190, 5390), (2370, 4530), (2940, 5240), (3690, 4160), (4230, 4700), (4620, 4990)]
responders = [[0, 2, 4, 0], [0, 3, 2, 0], [0, 3, 1, 3, 0], [0, 4, 0], [0, 5, 6, 0], [0, 6, 0], [0, 6, 5, 4, 0], [0, 5, 0]]

PoI_S_count = [25, 35, 35, 45, 35, 25]
PoI_Vol_count = [2, 2, 3, 3, 3, 2]
S_loc = [(-1, -1) for i in range(sum(PoI_S_count))]
Vol_loc = [(-1, -1) for i in range(sum(PoI_Vol_count))]

CC_0 = 0
CC_n = len(CC_loc)

PoIs_0 = CC_0
PoIs_n = PoIs_0 + len(PoIs_loc)

S_0 = PoIs_n
S_n = S_0 + sum(PoI_S_count)

#all cc, poi, S ids
CC_IDs = []
PoI_IDs = []
S_IDs = []
node_locs = []

allocate_survivors()

for loc in CC_loc:
    node_locs.append(loc)

for loc in PoIs_loc:
    node_locs.append(loc)

for loc in S_loc:
    node_locs.append(loc)

G, loc_o, nei_o = generate_Nepal_DRN()

neigh_des_folder = "/Users/vijay/BioDRNICDCSWorkSpace/ONEICDCS/src/NeighborList/"
loc_des_folder = "/Users/vijay/BioDRNICDCSWorkSpace/ONEICDCS/src/NodePosition/"

f = open(loc_des_folder + 'O_C' + str(sum(PoI_S_count)) + '_new.txt','w')
f.write(loc_o)
f.close()

f = open(neigh_des_folder + 'O_N' + str(sum(PoI_S_count)) + '_new.txt','w')
f.write(nei_o)
f.close()


