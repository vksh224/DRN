import networkx as nx
import collections
import pickle
import os

from Centrality import *
from find_tiers import *
from munkres import Munkres
from blondel import *
from find_tiers import *
#from bioDRN.generateDRN import *
from dist import *

def supplement(GBD,G2,t1_G2):
    D = list(set(G2.nodes()) - set(GBD.nodes()))
    GBD.add_nodes_from(D)
    D.extend(nx.isolates(GBD))

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

def ref_GRN(G1,G2,MC_G1,MC_G2,t1_G2, t2_G2, t3_G2):
    # List of nodes sorted in the non-increasing order of their motif centralities
    MC_G1 = [int(each[0]) for each in sorted(MC_G1.items(), key=lambda x: x[1], reverse=True)]
    MC_G2 = [int(each[0]) for each in sorted(MC_G2.items(), key=lambda x: x[1], reverse=True)]

    #print("1:",MC_G1)
    print("Sorted node motif centralities", MC_G2)

    # Identify tiers
    t1_G1, t2_G1, t3_G1 = tiers(G1, MC_G1,[],[],[])

    print("Before: DRN tier nodes ", t1_G2, t2_G2, t3_G2)

    t1_G2, t2_G2, t3_G2 = tiers(G2, MC_G2,t1_G2, t2_G2, t3_G2)

    #print(t1_G1, t2_G1, t3_G1)
    print("After: DRN tier nodes ", t1_G2, t2_G2, t3_G2)

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

                # if len(d_G2_t1) <= len(d_G1_t1) and len(d_G2_t3) <= len(d_G1_t3):
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

folder = "kathmandu/"
G1 = nx.read_gml('this_grn.gml')
G2 = nx.read_gml(folder + 'labeled_DRN.gml')
G2 = nx.convert_node_labels_to_integers(G2, first_label = 0)

t1_G2 = pickle.load(open(folder + "HO.p", "rb" ))
t2_G2 = pickle.load(open(folder + "SO.p", "rb" ))
t3_G2 = pickle.load(open(folder + "NO.p", "rb" ))

print ("Number of edges in DRN", len(G2.edges()))

# Calculate node motif centralities of the two graphs
MC_G1 = pickle.load(open("GRN_Centrality.p", "rb"))
#MC_G1 = motif(G1)
MC_G2 = motif(G2)

#print (MC_G1)
print ("Node motif centrality for DRN", MC_G2)

G = ref_GRN(G1,G2,MC_G1,MC_G2,t1_G2, t2_G2, t3_G2)

#degree_dist(G,'ref')
print ("Ref GRN - Nodes:",len(G.nodes()))
print ("Ref GRN - Edges:",len(G.edges()))
#MC_G = motif(G)

t1_G, t2_G, t3_G = tiers(G,None,[],[],[])

print ("GRN tiers ", len(t1_G), len(t2_G), len(t3_G))
print ("DRN tiers ", len(t1_G2), len(t2_G2), len(t3_G2))

#List of nodes in reference GRN
L1 = [t1_G,t2_G,t3_G]
#List of nodes in DRN
L2 = [t1_G2,t2_G2,t3_G2]

Y = np.array(similarity(G, G2, 0.01))
# S = Y.shape
# print ('Dimension of Y: ',S)

#Nodes and edges in bio-DRN
NBD = []
EBD = []

#Corresponding mapped node of reference GRN
NRG = []

for i in range(len(L1)):
    print (i)
    YM = Y[L1[i], :][:, L2[i]]
    YM = reverse(YM)
    YM = YM.tolist()
    m = Munkres()

    indexes = m.compute(YM)
    print (indexes)

    for each in indexes:
        NBD.append(L2[i][each[1]])
        NRG.append(L1[i][each[0]])

#Introduce edges in Bio-DRN
for u in NBD:
    for v in NBD:
        if (u,v) in G2.edges() and (NRG[NBD.index(u)],NRG[NBD.index(v)]) in G.edges():
            EBD.append((u,v))

print (len(NBD))
print (len(NRG))
print (len(EBD))

GBD = nx.DiGraph()
GBD.add_nodes_from(NBD)
GBD.add_edges_from(EBD)

print ("NOT FINAL NODE COUNT:", len(GBD))
print ("NOT FINAL EDGE COUNT:", len(GBD.edges()))

#Address isolated or unmapped nodes
GBD = supplement(GBD, G2, t1_G2)
#GBD = GBD.to_undirected()

print ("FINAL NODE COUNT:", len(GBD))
print ("FINAL EDGE COUNT:", len(GBD.edges()))

nx.write_gml(GBD, folder + 'GBD.gml')
nx.write_gml(G, folder + 'refG.gml')

#degree_dist(GBD,'bio')



