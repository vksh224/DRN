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
    MC_G1 = [each[0] for each in sorted(MC_G1.items(), key=lambda x: x[1], reverse=True)]
    MC_G2 = [each[0] for each in sorted(MC_G2.items(), key=lambda x: x[1], reverse=True)]

    #print("1:",MC_G1)
    #print("2:",MC_G2)


    # Identify tiers
    t1_G1, t2_G1, t3_G1 = tiers(G1, MC_G1,[],[],[])
    t1_G2, t2_G2, t3_G2 = tiers(G2, MC_G2,t1_G2, t2_G2, t3_G2)

    print(t1_G1, t2_G1, t3_G1)
    print(t1_G2, t2_G2, t3_G2)

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

#Area of deployment
X = 50
Y = 50
#Communication Radius
R = 20
#Number of nodes in input DRN

for ii in range(4,5):

    #G1 = nx.read_gml('Yeast.gml')
    #G1 = G1.reverse()
    #G1 = nx.convert_node_labels_to_integers(G1,first_label = 0)
    #nx.write_gml(G1,'this_grn.gml')

    #G1 = nx.read_gml('this_grn.gml')
    #MC_G1 = motif(G1)
    #pickle.dump(MC_G1, open("GRN_Centrality.p", "wb"))

    #Larger GRN Graph
    #G1 = nx.DiGraph()
    #G1.add_edges_from([(0,2), (2,1), (0,1), (2,3),(0,3)])
    #G1 = nx.read_gml('Yeast.gml')
    #G1 = G1.reverse()
    #G1 = nx.convert_node_labels_to_integers(G1,first_label = 0)
    #nx.write_gml(G1,'this_grn.gml')
    G1 = nx.read_gml('this_grn.gml')
    #MC_G1 = motif(G1)
    #pickle.dump(MC_G1, open("GRN_Centrality.p", "wb"))

    #Smaller DRN graph
    #G2 = nx.DiGraph()
    #G2.add_edges_from([(7,1), (0,1), (1,2), (0,2), (1,3), (0,3), (2,3), (0,4), (4,3), (0,5), (5,6), (0,6)])
    #G2,t1_G2, t2_G2, t3_G2 = generate(X,Y,VN,R)
    curr = os.getcwd()

    #os.chdir('graphs')
    ss = (ii + 2) * 50
    VN = ss

    G2 = nx.read_gml('labeled_DRN.gml')
    t1_G2 = pickle.load(open( "HO.p", "rb" ))
    t2_G2 = pickle.load(open( "SO.p", "rb" ))
    t3_G2 = pickle.load(open( "NO.p", "rb" ))

    print (len(G2.edges()))
    os.chdir(curr)

    # Calculate node motif centralities of the two graphs
    MC_G1 = pickle.load(open("GRN_Centrality.p", "rb"))
    #MC_G1 = motif(G1)
    MC_G2 = motif(G2)

    print (MC_G1)
    print (MC_G2)

    G = ref_GRN(G1,G2,MC_G1,MC_G2,t1_G2, t2_G2, t3_G2)
    #degree_dist(G,'ref')
    print ("Number of nodes in reference GRN:",len(G.nodes()))
    print ("Number of edges in reference GRN:",len(G.edges()))
    #MC_G = motif(G)

    t1_G, t2_G, t3_G = tiers(G,None,[],[],[])

    print (len(t1_G), len(t2_G), len(t3_G))
    print (len(t1_G2), len(t2_G2), len(t3_G2))

    #List of nodes in reference GRN
    L1 = [t1_G,t2_G,t3_G]
    #List of nodes in DRN
    L2 = [t1_G2,t2_G2,t3_G2]
    Y = np.array(similarity(G, G2, 0.00001))

    #Nodes and edges in bio-DRN
    NBD = []
    EBD = []

    #Corresponding mapped node of reference GRN
    NRG = []

    for i in range(len(L1)):

        print (i)
        YM = Y[L1[i], :][:, L2[i]]
        #print (YM)

        YM = reverse(YM)

        YM = YM.tolist()
        m = Munkres()

        indexes = m.compute(YM)
        print (indexes)

        for each in indexes:
            NBD.append(L2[i][each[1]])
            NRG.append(L1[i][each[0]])



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

    GBD = supplement(GBD, G2, t1_G2)
    #GBD = GBD.to_undirected()

    os.chdir('graphs')
    print ("FINAL NODE COUNT:", len(GBD))
    print ("FINAL EDGE COUNT:", len(GBD.edges()))

    nx.write_gml(GBD,'GBD' + str(ss) + '.gml')
    nx.write_gml(G,'refG' + str(ss) + '.gml')

    os.chdir(curr)
    #degree_dist(GBD,'bio')



