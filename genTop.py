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
    S = spanning(R.copy())
    #K2 = kconnected(R.copy(),2)
    #K4 = kconnected(O.copy(),4)

    KR2 = kregular(O.copy(),2)
    KR4 = kregular(O.copy(),4)
    KR8 = kregular(O.copy(),8)

    print (len(KR2.edges()))
    print (len(KR4.edges()))
    print (len(KR8.edges()))
    return R,S, KR2, KR4, KR8

'''
curr = os.getcwd()
for ii in range(2,3):

    print (ii)
    s = (ii + 2) * 50

    os.chdir('graphs')
    O = nx.read_gml('O' + str(s) + '.gml')
    B = nx.read_gml('GBD' + str(s) + '.gml')
    os.chdir(curr)

    #R, S, K2, K4,K8 = main(O,B)
    R, S, KR2, KR4, KR8 = main(O,B)
    os.chdir('graphs')
    nx.write_gml(R,'R' + str(s) + '.gml')
    nx.write_gml(S,'S' + str(s) + '.gml')

    #nx.write_gml(K2,'K2-' + str(s) + '.gml')
    #nx.write_gml(K4,'K4-' + str(s) + '.gml')

    nx.write_gml(KR2, 'KR2-' + str(s) + '.gml')
    nx.write_gml(KR4, 'KR4-' + str(s) + '.gml')
    nx.write_gml(KR8, 'KR8-' + str(s) + '.gml')

    os.chdir(curr)
'''
