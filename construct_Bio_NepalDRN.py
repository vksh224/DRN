
from Centrality import *
#from munkres import Munkres
from blondel import *
from find_tiers import *
from constants import *
from construct_NepalDRN_utility import plot_graph
from degree import plot_deg_dist
import operator
from writeFile import *
from construct_NepalDRN_utility import convert_to_real_world_DRN

def supplement(GBD,G2,t1_G2):
    D = list(set(G2.nodes()) - set(GBD.nodes()))
    GBD.add_nodes_from(D)
    D.extend(nx.isolates(GBD))
    print("Isolated nodes: ", len(D))
    for u in D:
        for v in t1_G2:
            if nx.has_path(G2,u,v):
                p = nx.shortest_path(G2,source = u,target = v)
                for i in range(1,len(p)):
                    GBD.add_edge(p[i - 1],p[i])
                break
    return GBD

def reverse(Y):
    for i in range(len(Y)):
        for j in range(len(Y[0])):
                Y[i,j] = - float(Y[i,j])

    return Y

def ref_GRN_old(G1,G2,MC_G1,MC_G2,t1_G2, t2_G2, t3_G2):
    # List of nodes sorted in the non-increasing order of their motif centralities
    MC_G1 = [each[0] for each in sorted(MC_G1.items(), key=lambda x: x[1], reverse=True)]
    MC_G2 = [each[0] for each in sorted(MC_G2.items(), key=lambda x: x[1], reverse=True)]

    # Identify tiers
    t1_G1, t2_G1, t3_G1 = tiers(G1, MC_G1,[],[],[])
    t1_G2, t2_G2, t3_G2 = tiers(G2, MC_G2, t1_G2, t2_G2, t3_G2)

    if debug_mode:
        print("Total tier 2 nodes in GRN ", len(t2_G1), " DRN", len(t2_G2))

    #Nodes participating in motifs with each node
    # NSM = pickle.load(open(GRN_directory + "NSM_Y.p", "rb"))
    NSM = pickle.load(open("NSM.p", "rb"))

    # Node and edge set in reference GRN
    E = []
    N = []

    visited_t2_G2_nodes = []
    visited_t2_G1_nodes = []
    # while (True):
    #flag = False
    for k in t2_G1:  # GRN
        for j in t2_G2: #DRN

            d_G1_t1 = find_tier_degree(k, t1_G1, G1)
            d_G2_t1 = find_tier_degree(j, t1_G2, G2)

            d_G1_t3 = find_tier_degree(k, t3_G1, G1)
            d_G2_t3 = find_tier_degree(j, t3_G2, G2)

            # if (len(d_G2_t1) <= len(d_G1_t1) and len(d_G2_t3) <= len(d_G1_t3)) and j not in visited_t2_G2_nodes:
            #Tier 2 node must have both in-degree and out-degree
            if len(d_G1_t1) > 0 and len(d_G1_t3) > 0 and j not in visited_t2_G2_nodes:
                N.append(k)

                #add each tier 1 GRN nodes (with an edge with node K) in the ref GRN
                for each in d_G1_t1:
                    if each not in N and each in NSM[k]:
                        N.append(each)

                for each in d_G1_t3:
                    if each not in N and each in NSM[k]:
                        N.append(each)

                visited_t2_G2_nodes.append(j)
                visited_t2_G1_nodes.append(k)
                break

    G = nx.DiGraph()
    for u in N:
        for v in N:
            if G1.has_edge(u, v):
                E.append((u, v))

    G.add_nodes_from(N)
    G.add_edges_from(E)

    G = nx.convert_node_labels_to_integers(G,first_label = 0)
    return G

#ICDCS code
def ref_GRN_ICDCS(G1,G2,MC_G1,MC_G2,t1_G2, t2_G2, t3_G2):

    # List of nodes sorted in the non-increasing order of their motif centralities
    MC_G1 = [each[0] for each in sorted(MC_G1.items(), key=lambda x: x[1], reverse=True)]
    MC_G2 = [each[0] for each in sorted(MC_G2.items(), key=lambda x: x[1], reverse=True)]

    #print("1:",MC_G1)
    #print("2:",MC_G2)

    # Identify tiers
    t1_G1, t2_G1, t3_G1 = tiers(G1, MC_G1,[],[],[])
    t1_G2, t2_G2, t3_G2 = tiers(G2, MC_G2,t1_G2, t2_G2, t3_G2)

    # print("G1 Tiers", t1_G1, t2_G1, t3_G1)
    # print("G2 Tiers", t1_G2, t2_G2, t3_G2)

    #Copy tiers of DRN graph
    c_t1_G2 = deepcopy(t1_G2)
    c_t2_G2 = deepcopy(t2_G2)
    c_t3_G2 = deepcopy(t3_G2)

    #Nodes participating in motifs with each node
    NSM = pickle.load(open("NSM.p", "rb"))
    print ('NSM:',len(NSM))

    # Node and edge set in reference GRN
    E = []
    N = []

    while (True):

        flag = False
        for j in t2_G2:

            #print("j:", j)
            for k in t2_G1:

                d_G1_t1 = find_tier_degree(k, t1_G1, G1)
                d_G2_t1 = find_tier_degree(j, t1_G2, G2)

                d_G1_t3 = find_tier_degree(k, t3_G1, G1)
                d_G2_t3 = find_tier_degree(j, t3_G2, G2)

                if len(d_G2_t1) <= len(d_G1_t1) and len(d_G2_t3) <= len(d_G1_t3):

                    N.append(k)

                    for each in d_G1_t1:
                        if each not in N and each in NSM[k]:
                            N.append(each)

                    for each in d_G1_t3:
                        if each not in N and each in NSM[k]:
                            N.append(each)

                    t2_G2.pop(t2_G2.index(j))
                    t2_G1.pop(t2_G1.index(k))
                    flag = True
                    break

            if flag:
                break

        if not flag or len(t2_G2) == 0:
            break

    G = nx.DiGraph()
    for u in N:
        for v in N:
            if G1.has_edge(u, v):
                E.append((u, v))

    G.add_nodes_from(N)
    G.add_edges_from(E)

    G = nx.convert_node_labels_to_integers(G,first_label = 0)
    return G


#G1 - GRN, G2 - DRN
def ref_GRN(G1,G2,MC_G1,MC_G2,t1_G2, t2_G2, t3_G2):
    # List of nodes sorted in the non-increasing order of their motif centralities
    MC_G1 = [int(each[0]) for each in sorted(MC_G1.items(), key=lambda x: x[1], reverse=True)]
    MC_G2 = [int(each[0]) for each in sorted(MC_G2.items(), key=lambda x: x[1], reverse=True)]

    #print("1:",MC_G1)
    print("Sorted node motif centralities", MC_G2)

    # Identify tiers
    t1_G1, t2_G1, t3_G1 = tiers(G1, MC_G1,[],[],[])

    print("Before: DRN tier nodes ", t1_G2, t2_G2)
    t1_G2, t2_G2, t3_G2 = tiers(G2, MC_G2,t1_G2, t2_G2, t3_G2)
    print("After: DRN tier nodes ", t1_G2, t2_G2)

    #Copy tiers of DRN graph
    c_t1_G2 = deepcopy(t1_G2)
    c_t2_G2 = deepcopy(t2_G2)
    c_t3_G2 = deepcopy(t3_G2)

    #Nodes participating in motifs with each node
    #NSM = pickle.load(open(GRN_directory + "NSM.p", "rb"))
    NSM = pickle.load(open("NSM.p", "rb"))

    print ('NSM:',len(NSM))

    # Node and edge set in reference GRN
    E = []
    N = []

    while (True):
        flag = False
        for j in t2_G2:
            for k in t2_G1:
                d_G1_t1 = find_tier_degree(k, t1_G1, G1)
                d_G2_t1 = find_tier_degree(j, t1_G2, G2)

                d_G1_t3 = find_tier_degree(k, t3_G1, G1)
                d_G2_t3 = find_tier_degree(j, t3_G2, G2)

                if len(d_G2_t1) <= len(d_G1_t1) and len(d_G2_t3) <= len(d_G1_t3):
                    N.append(k)

                    for i in range(len(d_G1_t1)):
                        if d_G1_t1[i] not in N and d_G1_t1[i] in NSM[k]:
                            N.append(d_G1_t1[i])

                    #For tier 3 nodes
                    #Get first k elements of motif sorted nodes
                    sorted_G1_t3_ids = sorted(d_G1_t3)

                    unsorted_NSM_G1_t3 = [len(NSM[each]) for each in sorted_G1_t3_ids]
                    sorted_NSM_G1_t3_ids = [x for y,x in sorted(zip(unsorted_NSM_G1_t3, sorted_G1_t3_ids), reverse=True)]
                    for i in range(min(len(sorted_NSM_G1_t3_ids), 4 * len(d_G2_t3))):
                    #for i in range(len(sorted_NSM_G1_t3_ids)):
                        if sorted_NSM_G1_t3_ids[i] not in N and sorted_NSM_G1_t3_ids[i] in NSM[k]:
                            N.append(sorted_NSM_G1_t3_ids[i])

                t2_G2.pop(t2_G2.index(j))
                t2_G1.pop(t2_G1.index(k))
                flag = True
                break

            if flag:
                break

        if not flag or len(t2_G2) == 0:
            break

    G = nx.DiGraph()
    for u in N:
        for v in N:
            if G1.has_edge(u, v):
                E.append((u, v))

    G.add_nodes_from(N)
    G.add_edges_from(E)

    G = nx.convert_node_labels_to_integers(G,first_label = 0)
    return G

#Fast
def generateBioDRN_fast(G, G2, t1_G, t2_G, t3_G, t1_G2, t2_G2, t3_G2):

    n_D = len(G2)
    n_G = len(G)

    #DRN
    D_T = [t1_G2, t2_G2, t3_G2]
    #Reference GRN
    G_T = [t1_G, t2_G, t3_G]

    M = np.array(similarity(G, G2, 0.1))

    # mapping function
    m = {}

    for k in range(len(D_T)):

        D = {}
        for u in G_T[k]:
            for v in D_T[k]:
                D[(u, v)] = M[u, v]

        # print (D)

        cnt = 0
        while cnt < len(D_T[k]):

            max_v = max(D.items(), key=operator.itemgetter(1))[0]
            # print (k,max_v)
            # input('Enter a character.')

            m[max_v[1]] = max_v[0]

            remove_keys = []
            for keys in D.keys():
                if max_v[0] == keys[0] or max_v[1] == keys[1]:
                    remove_keys.append(keys)
                    #D.pop(keys, None)

            D = {key: D[key] for key in D if key not in remove_keys}

            cnt += 1

    GBD = nx.DiGraph()
    GBD.add_nodes_from(G2.nodes())

    # Introduce edges in Bio-DRN
    for u in GBD.nodes():
        for v in GBD.nodes():
            if u in m.keys() and v in m.keys():
                if (u, v) in G2.edges() and nx.has_path(G, m[u],m[v]) == True:
                    GBD.add_edge(u,v)

    return GBD

'''
def generateBioDRN(G, G2, t1_G, t2_G, t3_G, t1_G2, t2_G2, t3_G2):
    # List of nodes in reference GRN
    L1 = [t1_G, t2_G, t3_G]
    # List of nodes in DRN
    L2 = [t1_G2, t2_G2, t3_G2]
    Y = np.array(blondelS(G, G2, 0.1))

    # Nodes and edges in bio-DRN
    NBD = []
    EBD = []

    # Corresponding mapped node of reference GRN
    NRG = []

    for i in range(len(L1)):
        # print (i)
        YM = Y[L1[i], :][:, L2[i]]
        # print (YM)

        YM = reverse(YM)

        YM = YM.tolist()
        m = Munkres()

        indexes = m.compute(YM)
        print ("Index", indexes)

        for each in indexes:
            NBD.append(L2[i][each[1]])
            NRG.append(L1[i][each[0]])

    for u in NBD:
        for v in NBD:

            if (u, v) in G2.edges() and (NRG[NBD.index(u)], NRG[NBD.index(v)]) in G.edges():
                EBD.append((u, v))

    # print (len(NBD))
    # print (len(NRG))
    # print (len(EBD))

    GBD = nx.DiGraph()
    GBD.add_nodes_from(NBD)
    GBD.add_edges_from(EBD)

    return GBD
'''

#Main starts here
print("\n ======== Construct Bio-DRN: " + directory)

data_directory = directory + "Data/"
plot_directory = directory + "Plot/"
CC_locs = pickle.load(open(data_directory + "CC_locs.p", "rb"))
PoI_locs = pickle.load(open(data_directory + "PoI_locs.p", "rb"))
Vol_locs = pickle.load(open(data_directory + "Vol_locs.p", "rb"))
S_locs = pickle.load(open(data_directory + "S_locs.p", "rb"))
Res_paths = pickle.load(open(data_directory + "Res_paths.p", "rb"))

num_of_nodes = len(CC_locs) + len(PoI_locs) + len(Vol_locs) + len(S_locs)

#G1 = nx.read_gml(GRN_directory + 'Yeast_Ordered.gml')
G1 = nx.read_gml('this_grn.gml')
#G1 = G1.reverse()

t1_G2 = pickle.load(open(data_directory + "HO.p", "rb" ))
t2_G2 = pickle.load(open(data_directory + "SO.p", "rb" ))
t3_G2 = pickle.load(open(data_directory + "NO.p", "rb" ))

# Need to create these graphs for each time interval e.g., [0, 900; 900, 1800; 1800, 2700; 2700, 3600]

nei_o = '0 ' + str(total_simulation_time) + '\n'
bio_neighList_filename = 'B_N' + str(num_of_nodes  + len(Res_paths)) + ".txt"
#bio_neighList_filename = "random_Orig_DRN.txt"

print("\nBio - Neighbor list filename: " + bio_neighList_filename )
f = open(neigh_des_folder + bio_neighList_filename, 'w')
f.write(nei_o)

#network_construction_interval = snapshot_time_interval

# Create static original graph snapshots for given time interval
for t in range(0, total_simulation_time, network_construction_interval):
    print("\n======= Start Time : " + str(t) + " ======== ")

    G2 = nx.read_gml(directory + 'Orig_NepalDRN_' + str(t) + '.gml')
    G2 = nx.convert_node_labels_to_integers(G2, first_label = 0)
    #G2 = nx.erdos_renyi_graph(n = 100, p = 0.3, directed = True)

    # t1_G2 = [0]
    # t2_G2 = [i for i in range(1, 5)]
    # t3_G2 = [i for i in range(5, 100)]

    print("Number of nodes in DRN", len(G2))
    print ("Number of edges in DRN", len(G2.edges()))
    print("Density:", float(len(G2.edges())) / (len(G2) * (len(G2) - 1)))
    print("Is Orig-DRN connected: ", nx.is_connected(G2.to_undirected()))


    # Calculate node motif centralities of the two graphs
    # MC_G1 = pickle.load(open(GRN_directory + "NMC_Y.p", "rb"))
    MC_G1 = pickle.load(open("GRN_Centrality.p", "rb"))

    #MC_G1 = motif(G1)
    MC_G2 = motif(G2)
    # print ("Node motif centrality for DRN", MC_G2)

    G = ref_GRN_old(G1,G2,MC_G1,MC_G2,t1_G2, t2_G2, t3_G2)
    # G = G1.copy()

    #degree_dist(G,'ref')
    print ("Ref GRN - Nodes:",len(G.nodes()))
    print ("Ref GRN - Edges:",len(G.edges()))
    #MC_G = motif(G)

    t1_G, t2_G, t3_G = tiers(G,None,[],[],[])

    print ("GRN tiers ", len(t1_G), len(t2_G), len(t3_G))
    print ("DRN tiers ", len(t1_G2), len(t2_G2), len(t3_G2))

    #G is reference GRN, and G2 is DRN
    GBD = generateBioDRN_fast(G, G2, t1_G, t2_G, t3_G, t1_G2, t2_G2, t3_G2)

    print ("NOT FINAL NODE COUNT:", len(GBD))
    print ("NOT FINAL EDGE COUNT:", len(GBD.edges()))

    #Address isolated or unmapped nodes
    GBD = supplement(GBD, G2, t1_G2)

    print ("FINAL NODE COUNT:", len(GBD))
    print ("FINAL EDGE COUNT:", len(GBD.edges()))

    print("Is Bio-DRN connected after supplementary step?", nx.is_connected(GBD.to_undirected()))

    real_world_G = convert_to_real_world_DRN(GBD)
    print ("Real world G: #nodes:", len(real_world_G))
    print ("Real world G: #edges:", len(real_world_G.edges()))

    nei_b = writeF(real_world_G, t)
    f.write(nei_b)

    nx.write_gml(GBD, data_directory + 'GBD_' + str(t) + '.gml')
    nx.write_gml(G, data_directory + 'refG.gml')

    # if t == 0:
    #     plot_deg_dist(GBD, plot_directory + 'GBD_deg_' + str(t))
    #     plot_graph(GBD, plot_directory + "GBD_" + str(t))
    #
    #     plot_deg_dist(G, plot_directory + 'refG_deg_' + str(t))
    #     plot_graph(G, plot_directory + "refG_" + str(t))

f.close()




