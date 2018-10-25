import random
import networkx as nx
import os
import pickle

from scipy.spatial.distance import *
from writeFile import *
#from genTop import *

import networkx as nx
import collections
import pickle
import os

from Centrality import *
from find_tiers import *
from munkres import Munkres
from blondel import *
#from find_tiers import *
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
            if Y[i,j] > 0:
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

    #print("DRN Tier nodes ", t1_G1, t2_G1, t3_G1)
    #print("GRN Tier nodes ", t1_G2, t2_G2, t3_G2)

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


def bioD(G2,t1_G2, t2_G2, t3_G2):

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

    #print (len(G2.edges()))

    # Calculate node motif centralities of the two graphs
    MC_G1 = pickle.load(open("GRN_Centrality.p", "rb"))
    #MC_G1 = motif(G1)
    MC_G2 = motif(G2)

    #print (MC_G1)
    #print (MC_G2)

    G = ref_GRN(G1,G2,MC_G1,MC_G2,t1_G2, t2_G2, t3_G2)
    #degree_dist(G,'ref')
    #print ("Number of nodes in reference GRN:",len(G.nodes()))
    #print ("Number of edges in reference GRN:",len(G.edges()))
    #MC_G = motif(G)

    t1_G, t2_G, t3_G = tiers(G,None,[],[],[])

    print ("GRN: Number of nodes in each tier ", len(t1_G), len(t2_G), len(t3_G))
    print ("DRN: Number of nodes in each tier ", len(t1_G2), len(t2_G2), len(t3_G2))

    #List of nodes in reference GRN
    L1 = [t1_G,t2_G,t3_G]
    #List of nodes in DRN
    L2 = [t1_G2,t2_G2,t3_G2]
    Y = np.array(blondelS(G, G2, 0.1))

    #Nodes and edges in bio-DRN
    NBD = []
    EBD = []

    #Corresponding mapped node of reference GRN
    NRG = []

    for i in range(len(L1)):

        print ("Tier ", i)
        YM = Y[L1[i], :][:, L2[i]]
        #print (YM)

        YM = reverse(YM)

        YM = YM.tolist()
        m = Munkres()

        indexes = m.compute(YM)
        print ("Mapped nodes ", indexes)

        for each in indexes:
            NBD.append(L2[i][each[1]])
            NRG.append(L1[i][each[0]])

    for u in NBD:
        for v in NBD:

            if (u,v) in G2.edges() and (NRG[NBD.index(u)],NRG[NBD.index(v)]) in G.edges():
                EBD.append((u,v))

    #print (len(NBD))
    #print (len(NRG))
    #print (len(EBD))

    GBD = nx.DiGraph()
    GBD.add_nodes_from(NBD)
    GBD.add_edges_from(EBD)

    print ("***Number of nodes in GBD:",len(GBD))
    print ("***Number of edges in GBD:",len(GBD.edges()))
    GBD = supplement(GBD,G2,t1_G2)
    #GBD = GBD.to_undirected()

    print ("***Number of nodes in GBD:",len(GBD))
    print ("***Number of edges in GBD:",len(GBD.edges()))
    return GBD

def generateSim(X,Y,VN,R):

    #Node set
    N = [i for i in range(VN)]
    N = sorted(N,reverse = False)
    G = nx.DiGraph()
    G.add_nodes_from(N)

    # Coordinate of nodes
    C = [(random.randint(0,X),random.randint(0,Y)) for i in range(VN)]

    # Number of hub, sub and non
    HC = int(0.01 * VN)
    SC = int(0.05 * VN)
    NC = VN - HC - SC

    # Set of hub, sub and non-hubs
    HCN = N[:HC]
    SCN = N[HC:(HC + SC)]
    NCN = N[(HC + SC):]

    print ("HCN: ", HCN)
    print ("SCN: ", SCN)

    # CC location
    for i in HCN:
        C[i] = (random.randint(0, X), random.randint(0, Y))

    chosen_survivors = []
    count_pois = 0
    # PoI location
    for i in SCN:
        count_pois += 1
        C[i] = (random.randint(0, X), random.randint(0, Y))

        rem_survivors = [x for x in NCN if x not in chosen_survivors]
        avg_survivors_per_poi = len(NCN)/len(SCN)

        rand_survivors = int(random.uniform(0.5 * avg_survivors_per_poi, 1.5 * avg_survivors_per_poi))
        count_chosen_survivors = 0
        #print("\n ====== PoI", i, C[i])
        #print("\n Rem. survivors ", len(rem_survivors))
        # Survivor location
        for j in rem_survivors:
            if count_pois== len(SCN): #last PoI - need to include all remaining survivors
                rand_survivors = len(rem_survivors)

            if count_chosen_survivors <= rand_survivors:
                # random angle
                alpha = 2 * math.pi * random.random()
                r = poi_radius * math.sqrt(random.random())
                # calculating coordinates
                x = r * math.cos(alpha) + C[i][0]
                y = r * math.sin(alpha) + C[i][1]

                C[j] = (x, y)
                # print("Survivor", j, C[j])
                # C[j] = (random.randint(max(C[i][0] - poi_radius, 0), min(X, C[i][0] + poi_radius)),
                #         random.randint(max(C[i][0] - poi_radius, 0), min(Y, C[i][0] + poi_radius)))
                count_chosen_survivors += 1
                chosen_survivors.append(j)

    print ("Assigned CC, PoIs, and survivors: ", len(HCN), len(SCN), len(chosen_survivors))

    '''
    while(len(N) > 0):

        r = random.choice(N)
        N.pop(N.index(r))

        if HC > 0:
            HC = HC - 1
            HCN.append(r)

        elif SC > 0:
            SC = SC - 1
            SCN.append(r)

        else:
            NC = NC - 1
            NCN.append(r)
    '''

    time_periods = 13

    loc_o = '0 ' + str(time_periods * 600) + " 0 " + str(X) + " 0 " + str(Y) + '\n'
    nei_o = '0 ' + str(time_periods * 600) + '\n'
    nei_b = '0 ' + str(time_periods * 600) + '\n'
    nei_s = '0 ' + str(time_periods * 600) + '\n'
    nei_r = '0 ' + str(time_periods * 600) + '\n'
    nei_k2 = '0 ' + str(time_periods * 600) + '\n'
    nei_k4 = '0 ' + str(time_periods * 600) + '\n'
    nei_k8 = '0 ' + str(time_periods * 600) + '\n'

    N = [i for i in range(VN)]
    for i in range(time_periods):

        # change = random.sample(range(1, len(G)), int(0.2 * len(NCN)))
        # for j in change:
        #     C[j] = (random.randint(max(C[j][0] - poi_radius, 0), min(X, C[j][0] + poi_radius)),
        #             random.randint(max(C[j][0] - poi_radius, 0), min(Y, C[j][0] + poi_radius)))

        G = nx.DiGraph()
        G.add_nodes_from(N)

        # # Introduce edges
        # for u in G.nodes():
        #     for v in G.nodes():
        #         if u != v and euclidean(C[u],C[v]) <= R:
        #             G.add_edge(u,v)

        # Introduce edges
        for u in G.nodes():
            for v in G.nodes():
                # CC and CC
                if u != v and u in HCN and v in HCN and euclidean(C[u], C[v]) <= tower_range:
                    G.add_edge(u, v)
                    # print("C - C", u, v, HCN)

                # CC and PoI
                if u != v and u in HCN and v in SCN and euclidean(C[u], C[v]) <= tower_range:
                    G.add_edge(u, v)
                    # print("C - P", u, v, HCN)

                # PoI and PoI
                if u != v and u in SCN and v in SCN and euclidean(C[u], C[v]) <= tower_range:
                    G.add_edge(u, v)
                    # print("P - P", u, v, HCN)

                # PoI and Survivor
                if u != v and u in SCN and v in NCN and euclidean(C[u], C[v]) <= ble_range:
                    G.add_edge(u, v)
                    # print("P - S", u, v, HCN)

                # Survivor and Survivor
                if u != v and u in NCN and v in NCN and euclidean(C[u], C[v]) <= ble_range:
                    G.add_edge(u, v)
                    # print("S - S", u, v, HCN)

                    # if u != v and euclidean(C[u],C[v]) <= R:
                    #     G.add_edge(u,v)

        GBD = bioD(G, HCN, SCN, NCN)
        # RA = randomDRN(G,GBD)
        # S = spanning(RA.copy())

        # KR2 = kregular(RA,2)
        # KR4 = kregular(RA,4)
        # KR8 = kregular(RA,8)

        loc_o += writeC(C,i)
        nei_o += writeF(G,i)
        nei_b += writeF(GBD,i)
        # nei_s += writeF(S,i)
        # nei_r += writeF(RA,i)
        # nei_k2 += writeF(KR2, i)
        # nei_k4 += writeF(KR4, i)
        # nei_k8 += writeF(KR8, i)

    # return loc_o, nei_o, nei_b, nei_s, nei_r, nei_k2, nei_k4, nei_k8,HCN, SCN, NCN
    return loc_o, nei_o, nei_b, HCN, SCN, NCN

# Area of deployment
X = 3000
Y = 3000
# Communication Radius
R = 20 #Obsolete

tower_range = 500
ble_range = 100
poi_radius = 200

# Number of nodes in input DRN
# VN = 100

curr = os.getcwd()

for i in range(2,3):

    print ('i:',i)
    s = i * 100

    # loc_o, nei_o, nei_b, nei_s, nei_r, nei_k2, nei_k4, nei_k8, HCN, SCN, NCN = generateSim(X, Y, s, R)
    loc_o, nei_o, nei_b, HCN, SCN, NCN = generateSim(X, Y, s, R)

    #os.chdir('simulation')
    # os.chdir(str(s))

    neigh_des_folder = "/Users/vijay/BioDRNICDCSWorkSpace/ONEICDCS/src/NeighborList/"
    loc_des_folder = "/Users/vijay/BioDRNICDCSWorkSpace/ONEICDCS/src/NodePosition/"

    f = open(loc_des_folder + 'O_C' + str(s) + '.txt','w')
    f.write(loc_o)
    f.close()

    f = open(neigh_des_folder + 'O_N' + str(s) + '.txt','w')
    f.write(nei_o)
    f.close()

    f = open(neigh_des_folder + 'B_N' + str(s) + '.txt','w')
    f.write(nei_b)
    f.close()
    #
    # f = open('S_N' + str(s) + '.txt','w')
    # f.write(nei_s)
    # f.close()
    #
    # f = open('R_N' + str(s) + '.txt','w')
    # f.write(nei_r)
    # f.close()
    #
    # f = open('K2_' + str(s) + '.txt','w')
    # f.write(nei_k2)
    # f.close()
    #
    # f = open('K4_' + str(s) + '.txt','w')
    # f.write(nei_k4)
    # f.close()
    #
    # f = open('K8_' + str(s) + '.txt','w')
    # f.write(nei_k8)
    # f.close()

    #nx.write_gml(G,'O' + str(s) + '.gml')
    pickle.dump(HCN, open('H' + str(i) + '.p', "wb"))
    pickle.dump(SCN, open('S' + str(i) + '.p', "wb"))
    pickle.dump(NCN, open('N' + str(i) + '.p', "wb"))

    os.chdir(curr)
