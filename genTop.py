import random
import networkx as nx
import os
from read_graph import plot_graph
from constants import *
from construct_NepalDRN_utility import convert_to_real_world_DRN

def rename_graph(O):

    m = {}
    for u in O.nodes():
        m[u] = int(u)

    O = nx.relabel_nodes(O,m)
    return O

def neighbor_list(G,s,t):

    #print (G.nodes())
    for u in sorted(G.nodes()):
        next = [u]
        next.extend(G.successors(u))

        s = s + str(t) + ' ' + " ".join(str(x) for x in next) + '\n'

    return s

def kregular(G,k):
    #R = G.to_undirected()
    R = G.to_undirected()
    L = list(R.edges())

    while(len(L) > 0):
        e = L.pop(0)
        if R.degree(e[0]) > k and R.degree(e[1]) > k:
            R.remove_edge(e[0], e[1])

            # if not nx.is_connected(R):
            #     L.append(e[0], e[1])
            #     R.add_edge(e[0], e[1])

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

def randomDRN(O,B):
    R = O.copy()
    # Number of edges to be preserved from original DRN
    r = len(B.edges())
    L = list(R.edges())

    while (len(R.edges()) > r and len(L) > 0):
        #select random edge
        re = random.choice(L)
        R.remove_edge(re[0],re[1])
        L.remove(re)
        if (not nx.is_weakly_connected(R)):
            R.add_edge(re[0], re[1])
    #print("Rand DRN: Is weakly connected", nx.is_weakly_connected(R))
    return R

def spanning(R):
    O_U = R.to_undirected()
    S = nx.minimum_spanning_tree(O_U)
    S_D = nx.DiGraph()

    for e in S.edges():
        if (e[0], e[1]) in R.edges():
            S_D.add_edge(e[0],e[1])
        else:
            S_D.add_edge(e[1], e[0])
    return S_D

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


s_spanning = '0 ' + str(total_simulation_time) + "\n"
s_random = '0 ' + str(total_simulation_time) + "\n"
s_k2 = '0 ' + str(total_simulation_time) + "\n"
s_k4 = '0 ' + str(total_simulation_time) + "\n"
# s_k8 = '0 ' + str(total_simulation_time) + "\n"

naming = '_'
once = False
for t in range(0, total_simulation_time, network_construction_interval):

    # O: original DRN
    # B: bio-DRN
    # S: spanning tree
    # R: random DRN

    O = nx.read_gml(directory + 'Orig_NepalDRN_' + str(t) + '.gml')
    O = rename_graph(O)

    if not once:
        naming = naming + str(len(O))
        once = True

    B = nx.read_gml(data_directory + 'GBD_' + str(t) + '.gml')
    B = rename_graph(B)

    R = randomDRN(O,B)
    S = spanning(R)
    K2 = kconnected(R, 2)
    K4 = kconnected(R, 4)
    # K8 = kconnected(R, 8)

    s_spanning = neighbor_list(S,s_spanning, t)
    s_random = neighbor_list(R,s_random, t)
    #s_bioDRN = neighbor_list(B,s_bioDRN, t)
    s_k2 = neighbor_list(K2, s_k2, t)
    s_k4 = neighbor_list(K4, s_k4, t)
    # s_k8 = neighbor_list(K8, s_k8, t)

    real_world_SG = convert_to_real_world_DRN(s_spanning)
    real_world_RG = convert_to_real_world_DRN(s_random)
    real_world_K2 = convert_to_real_world_DRN(s_k2)
    real_world_K4 = convert_to_real_world_DRN(s_k4)

f_spanning = open(neigh_des_folder + 'S' + naming + '.txt','w')
f_random = open(neigh_des_folder + 'R' + naming + '.txt','w')
#f_bioDRN = open('b' + naming + '.txt','w')
f_k2 = open(neigh_des_folder + 'K2' + naming + '.txt','w')
f_k4 = open(neigh_des_folder + 'K4' + naming + '.txt','w')
# f_k8 = open(neigh_des_folder + 'K8' + naming + '.txt','w')

f_spanning.write(real_world_SG)
f_random.write(real_world_RG)
f_k2.write(real_world_K2)
f_k4.write(real_world_K4)
# f_k8.write(s_k8)

f_spanning.close()
f_random.close()
f_k2.close()
f_k4.close()
# f_k8.close()

