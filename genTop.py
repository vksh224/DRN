import random
import networkx as nx
import os
from read_graph import plot_graph
import pickle
from constants import *
from construct_NepalDRN_utility import convert_to_real_world_DRN
from construct_Bio_NepalDRN import *
import shutil

from writeFile import writeF

def rename_graph(O):

    m = {}
    for u in O.nodes():
        m[u] = int(u)

    O = nx.relabel_nodes(O,m)
    return O

def bioDRN(G2, t1_G2, t2_G2, t3_G2, t):
    # G1 = nx.read_gml(GRN_directory + 'Yeast_Ordered.gml')
    G1 = nx.read_gml('this_grn.gml')
    # G1 = G1.reverse()

    print("\n======= Start Time : " + str(t) + " ======== ")

    print("Number of nodes in DRN", len(G2))
    print ("Number of edges in DRN", len(G2.edges()))
    print("Density:", float(len(G2.edges())) / (len(G2) * (len(G2) - 1)))
    print("Is Orig-DRN connected: ", nx.is_connected(G2.to_undirected()))

    # Calculate node motif centralities of the two graphs
    # MC_G1 = pickle.load(open(GRN_directory + "NMC_Y.p", "rb"))
    MC_G1 = pickle.load(open("GRN_Centrality.p", "rb"))

    # MC_G1 = motif(G1)
    MC_G2 = motif(G2)
    # print ("Node motif centrality for DRN", MC_G2)

    G = ref_GRN_old(G1, G2, MC_G1, MC_G2, t1_G2, t2_G2, t3_G2)
    # G = G1.copy()

    # degree_dist(G,'ref')
    print ("Ref GRN - Nodes:", len(G.nodes()))
    print ("Ref GRN - Edges:", len(G.edges()))
    # MC_G = motif(G)

    t1_G, t2_G, t3_G = tiers(G, None, [], [], [])

    print ("GRN tiers ", len(t1_G), len(t2_G), len(t3_G))
    print ("DRN tiers ", len(t1_G2), len(t2_G2), len(t3_G2))

    # G is reference GRN, and G2 is DRN
    GBD = generateBioDRN_fast(G, G2, t1_G, t2_G, t3_G, t1_G2, t2_G2, t3_G2)

    print ("NOT FINAL NODE COUNT:", len(GBD))
    print ("NOT FINAL EDGE COUNT:", len(GBD.edges()))

    # Address isolated or unmapped nodes
    GBD = supplement(GBD, G2, t1_G2)

    print ("FINAL NODE COUNT:", len(GBD))
    print ("FINAL EDGE COUNT:", len(GBD.edges()))

    print("Is Bio-DRN connected after supplementary step?", nx.is_connected(GBD.to_undirected()))

    #real_world_G = convert_to_real_world_DRN(GBD)
    #print ("Real world G: #nodes:", len(real_world_G))
    #print ("Real world G: #edges:", len(real_world_G.edges()))
    #GBD.add_edges_from([e for e in G2.edges() if (e[0] not in S_IDs and e[1] not in S_IDs)])

    return GBD


def kregular(O, G, k, S_IDs):

    R = O.to_undirected()
    L = list(R.edges())

    while(len(L) > 0):
        e = L.pop(0)
        if R.degree(e[0]) > k and R.degree(e[1]) > k:
            R.remove_edge(e[0], e[1])

            # if not nx.is_connected(R):
            #     L.append(e[0], e[1])
            #     R.add_edge(e[0], e[1])

    #R.add_edges_from([e for e in O.edges() if (e[0] not in S_IDs and e[1] not in S_IDs)])
    return R

def kconnected(R,k):

    RG = R.copy()
    #RG = RG.to_undirected()
    N = nx.k_components(RG.to_undirected())
    N = list(N[k][0])

    G = nx.DiGraph()
    G.add_nodes_from(N)
    for u in N:
        for v in N:
            if (u,v) in RG.edges():
                G.add_edge(u,v)

    G = nx.convert_node_labels_to_integers(G,first_label = 0)

    return G

def randomDRN(O,B, S_IDs):
    R = O.to_undirected()
    # Number of edges to be preserved from original DRN
    r = len(B.edges())
    L = list(R.edges())

    while (len(R.edges()) > r and len(L) > 0):

        #select random edge
        re = random.choice(L)

        R.remove_edge(re[0],re[1])
        L.remove(re)

        # if (not nx.is_weakly_connected(R)):
        #     R.add_edge(re[0], re[1])

    #print("Rand DRN: Is weakly connected", nx.is_weakly_connected(R))

    # R = R.to_undirected()
    #R.add_edges_from([e for e in O.edges() if (e[0] not in S_IDs and e[1] not in S_IDs)])
    return R


def spanning(O, R, S_IDs):
    O_U = O.to_undirected()
    S = nx.minimum_spanning_tree(O_U)

    '''
    S_D = nx.DiGraph()

    for e in S.edges():
        if (e[0], e[1]) in R.edges():
            S_D.add_edge(e[0],e[1])
        else:
            S_D.add_edge(e[1], e[0])
    '''
    #S.add_edges_from([e for e in O.edges() if (e[0] not in S_IDs and e[1] not in S_IDs)])

    return S

'''
def main(O,B):
    # O: original DRN
    # B: bio-DRN
    # S: spanning tree
    # R: random DRN
    R = randomDRN(O,B)
    print("\nRandom edges:", len(R.edges()))
    print("Rand DRN isConnected:", nx.is_connected(R.to_undirected()))

    S = spanning(R.copy())
    print("\nST edges:", len(S.edges()))
    print("ST DRN isConnected:", nx.is_connected(S.to_undirected()))

    #K2 = kconnected(R.copy(),2)
    #K4 = kconnected(O.copy(),4)

    KR2 = kregular(O.copy(),2)
    print("\nKR2 edges:", len(KR2.edges()))
    print("KR2 DRN isConnected:", nx.is_connected(KR2.to_undirected()))

    KR4 = kregular(O.copy(),4)
    print("\nKR4 edges:", len(KR4.edges()))
    print("KR4 DRN isConnected:", nx.is_connected(KR4.to_undirected()))

    KR8 = kregular(O.copy(),8)
    print("\nKR8 edges:", len(KR8.edges()))
    print("KR8 DRN isConnected:", nx.is_connected(KR8.to_undirected()))

    return R, S, KR2, KR4, KR8


folder = "kathmandu/"

O = nx.read_gml(folder + 'labeled_DRN.gml')
print("\nOriginal DRN edges:", len(O.edges()))
print("Original DRN isConnected:", nx.is_connected(O.to_undirected()))

B = nx.read_gml(folder + 'GBD.gml')
print("\nBio DRN edges:", len(B.edges()))
print("Bio DRN: is connected", nx.is_connected(B.to_undirected()))
#print("Bio DRN: connected components", sorted(nx.connected_components(B.to_undirected()), key = len, reverse=False))

plot_graph(B, "bioDRN")

R, S, KR2, KR4, KR8 = main(O, B)

plot_graph(R, "randDRN")
plot_graph(S, "ST-DRN")
plot_graph(KR2, "KR2-DRN")
plot_graph(KR4, "KR4-DRN")

nx.write_gml(R, folder + 'R.gml')
nx.write_gml(S, folder + 'S.gml')
nx.write_gml(KR2, folder + 'KR2.gml')
nx.write_gml(KR4, folder + 'KR4.gml')
nx.write_gml(KR8, folder + 'KR8.gml')

'''

#-------------------------------------------------------------------------------

print("\n ======== GenTop: " + directory)
data_directory = directory + 'Data/'

CC_locs = pickle.load(open(data_directory + "CC_locs.p", "rb"))
PoI_locs = pickle.load(open(data_directory + "PoI_locs.p", "rb"))
Vol_locs = pickle.load(open(data_directory + "Vol_locs.p", "rb"))
S_locs = pickle.load(open(data_directory + "S_locs.p", "rb"))
Res_paths = pickle.load(open(data_directory + "Res_paths.p", "rb"))

V = len(CC_locs) + len(PoI_locs) + len(Vol_locs) + len(S_locs) + len(Res_paths)

# Find source destination nodes
CC_IDs = range(len(CC_locs))
PoI_IDs = range(len(CC_locs), len(CC_locs) + len(PoI_locs))
Vol_IDs = range(len(CC_locs) + len(PoI_locs), len(CC_locs) + len(PoI_locs) + len(Vol_locs))
S_IDs = range(len(CC_locs) + len(PoI_locs) + len(Vol_locs), len(CC_locs) + len(PoI_locs) + len(Vol_locs) + len(S_locs))

f_bio = open(neigh_des_folder + 'B_' + str(V) + ".txt", 'w')
f_bio_ideal = open(neigh_des_folder + 'B_ideal_' + str(V) + ".txt", 'w')
f_spanning = open(neigh_des_folder + 'S_' + str(V) + ".txt",'w')
f_random = open(neigh_des_folder + 'R_' + str(V) + '.txt','w')
f_k2 = open(neigh_des_folder + 'K2_' + str(V) + '.txt','w')
f_k4 = open(neigh_des_folder + 'K4_' + str(V) + '.txt','w')
f_k8 = open(neigh_des_folder + 'K8_' + str(V) + '.txt','w')
f_k3 = open(neigh_des_folder + 'K3_' + str(V) + '.txt','w')
f_k5 = open(neigh_des_folder + 'K5_' + str(V) + '.txt','w')

s_bio = '0 ' + str(total_simulation_time) + '\n'
s_bio_ideal = '0 ' + str(total_simulation_time) + '\n'
s_spanning = '0 ' + str(total_simulation_time) + "\n"
s_random = '0 ' + str(total_simulation_time) + "\n"
s_k2 = '0 ' + str(total_simulation_time) + "\n"
s_k4 = '0 ' + str(total_simulation_time) + "\n"
s_k8 = '0 ' + str(total_simulation_time) + "\n"
s_k3 = '0 ' + str(total_simulation_time) + "\n"
s_k5 = '0 ' + str(total_simulation_time) + "\n"

f_bio.write(s_bio)
f_bio_ideal.write(s_bio_ideal)
f_spanning.write(s_spanning)
f_random.write(s_random)
f_k2.write(s_k2)
f_k4.write(s_k4)
f_k8.write(s_k8)
f_k3.write(s_k3)
f_k5.write(s_k5)

#Only for Bio-DRN
t1_G2 = pickle.load(open(data_directory + "HO.p", "rb"))
t2_G2 = pickle.load(open(data_directory + "SO.p", "rb"))
t3_G2 = pickle.load(open(data_directory + "NO.p", "rb"))


for t in range(network_construction_interval, network_generation_time, network_construction_interval):

    # O: original DRN
    # B: bio-DRN
    # S: spanning tree
    # R: random DRN

    O = nx.read_gml(directory + 'Orig_NepalDRN_' + str(t - network_construction_interval) + '.gml')
    O = rename_graph(O)

    #B = bioDRN(O, t1_G2, t2_G2, t3_G2, t)
    B = nx.read_gml(data_directory + 'Bio_' + str(t - network_construction_interval) + '.gml')
    R = randomDRN(O, B, S_IDs)

    K2 = kregular(O, R, 2, S_IDs)
    K4 = kregular(O, R, 4, S_IDs)
    K8 = kregular(O, R, 8, S_IDs)
    K3 = kregular(O, R, 3, S_IDs)
    K5 = kregular(O, R, 5, S_IDs)
    S = spanning(K3, R, S_IDs)

    O = O.to_undirected()
    B = B.to_undirected()

    #print (O.nodes())

    #------------------Writing the topology in Data folder----------
    curr = os.getcwd()
    os.chdir(directory + 'Data/')

    #nx.write_gml(O,'Original'+ '.gml')
    # nx.write_gml(B,'Bio_' + str(t - network_construction_interval) + '.gml')
    nx.write_gml(R,'Random_' + str(t - network_construction_interval) + '.gml')
    nx.write_gml(S,'Spanning_' + str(t - network_construction_interval) + '.gml')
    nx.write_gml(K2,'K2_' + str(t - network_construction_interval) + '.gml')
    nx.write_gml(K4,'k4_' + str(t - network_construction_interval) + '.gml')
    nx.write_gml(K8,'k8_' + str(t - network_construction_interval) + '.gml')
    nx.write_gml(K3, 'k3_' + str(t - network_construction_interval) + '.gml')
    nx.write_gml(K5, 'k5_' + str(t - network_construction_interval) + '.gml')

    #print ('See here:', t, len(B.nodes()))

    os.chdir(curr)

    # K8 = kconnected(R, 8)


    #TODO: These graphs need to be converted to ONE simulator specific (See lines 450-455 in construct_Bio_NepalDRN.py)
    # For instance, there exists no direct link between CC 0 and PoI 1, but it is through multiple responders, say 9, 10, and 11
    # then, the link 0-1 in Orig-DRN/Bio-DRN, is equivalent to 0-9, 0-10, 0-11, 1-9, 1-10, 1-11 (if all all 9, 10 and 11 visit both 0 and 1)
    real_world_B = convert_to_real_world_DRN(B)
    real_world_SG = convert_to_real_world_DRN(S)
    real_world_RG = convert_to_real_world_DRN(R)
    real_world_K2 = convert_to_real_world_DRN(K2)
    real_world_K4 = convert_to_real_world_DRN(K4)
    real_world_K8 = convert_to_real_world_DRN(K8)
    real_world_K3 = convert_to_real_world_DRN(K3)
    real_world_K5 = convert_to_real_world_DRN(K5)

    s_bio = writeF(real_world_B, t - network_construction_interval)
    f_bio.write(s_bio)

    s_spanning = writeF(real_world_SG, t - network_construction_interval)
    f_spanning.write(s_spanning)

    s_random = writeF(real_world_RG, t - network_construction_interval)
    f_random.write(s_random)

    s_k2 = writeF(real_world_K2, t - network_construction_interval)
    f_k2.write(s_k2)

    s_k4 = writeF(real_world_K4, t - network_construction_interval)
    f_k4.write(s_k4)

    s_k8 = writeF(real_world_K8, t - network_construction_interval)
    f_k8.write(s_k8)

    s_k3 = writeF(real_world_K3, t - network_construction_interval)
    f_k3.write(s_k3)

    s_k5 = writeF(real_world_K5, t - network_construction_interval)
    f_k5.write(s_k5)

    if t == network_construction_interval:
        f_bio_s = open(neigh_des_folder + 'B_' + str(V) + "_s.txt", "w")
        f_bio_s.write('0 ' + str(total_simulation_time) + '\n')
        f_bio_s.write(s_bio)
        f_bio_s.close()

    if generate_B_ideal == True:
        O_ideal = nx.read_gml(directory + 'Orig_NepalDRN_' + str(t) + '.gml')
        O_ideal = rename_graph(O_ideal)
        B_ideal = bioDRN(O_ideal, t1_G2, t2_G2, t3_G2, t)
        real_world_B_ideal = convert_to_real_world_DRN(B_ideal)
        s_bio_ideal = writeF(real_world_B_ideal, t)
        f_bio_ideal.write(s_bio_ideal)


f_bio.close()
f_spanning.close()
f_random.close()
f_k2.close()
f_k4.close()
f_k8.close()
f_k3.close()
f_k5.close()

if generate_B_ideal == True:
    f_bio_ideal.close()

