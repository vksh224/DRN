import random
import networkx as nx
import os

def kregular(G,k):

    R = G.to_undirected()
    L = R.edges()

    while(len(L) > 0):

        e = L.pop(0)
        if R.degree(e[0]) > k and R.degree(e[1]) > k:
            R.remove_edge(e[0],e[1])

    return R

def kconnected(R,k):

    RG = R.copy()
    RG = RG.to_undirected()
    N = nx.k_components(RG)
    N = list(N[k][0])

    G = nx.Graph()
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
    L = R.edges()

    while (len(R.edges()) > r):

        #select random edge
        re = random.choice(L)
        R.remove_edge(re[0],re[1])
        L.remove((re[0], re[1]))
        if (not nx.is_weakly_connected(R)):
            R.add_edge(re[0], re[1])

    print (nx.is_weakly_connected(R))
    return R

def spanning(R):
    O_U = R.to_undirected()
    S = nx.minimum_spanning_tree(O_U)

    S_D = nx.DiGraph()

    for e in S.edges():

        if (e[0],e[1]) in R.edges():
            S_D.add_edge(e[0],e[1])
        else:
            S_D.add_edge(e[1], e[0])


    return S_D

def main(O,B):

    # O: original DRN
    # B: bio-DRN
    # S: spanning tree
    # R: random DRN

    R = randomDRN(O,B)
    print("Random edges:", len(R.edges()))

    S = spanning(R.copy())
    print("S edges:", len(S.edges()))
    #K2 = kconnected(R.copy(),2)
    #K4 = kconnected(O.copy(),4)

    KR2 = kregular(O.copy(),2)
    print("KR2 edges:", len(KR2.edges()))

    KR4 = kregular(O.copy(),4)
    print("KR4 edges:", len(KR4.edges()))

    KR8 = kregular(O.copy(),8)
    print("KR8 edges:", len(KR8.edges()))

    return R, S, KR2, KR4, KR8



folder = "kathmandu/"
O = nx.read_gml(folder + 'labeled_DRN.gml')
print("Original DRN edges:", len(O.edges()))

B = nx.read_gml(folder + 'GBD.gml')
print("Bio DRN edges:", len(B.edges()))

R, S, KR2, KR4, KR8 = main(O, B)

nx.write_gml(R, folder + 'R.gml')
nx.write_gml(S, folder + 'S.gml')
nx.write_gml(KR2, folder + 'KR2.gml')
nx.write_gml(KR4, folder + 'KR4.gml')
nx.write_gml(KR8, folder + 'KR8.gml')

