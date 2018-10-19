import random
import networkx as nx
import os
import pickle

from scipy.spatial.distance import *
from writeFile import *

def generate(X,Y,VN,R):

    # Node set
    N = [i for i in range(VN)]
    G = nx.DiGraph()
    G.add_nodes_from(N)

    # Coordinate of nodes
    C = [(random.randint(0,X),random.randint(0,Y)) for i in range(VN)]


    # Number of hub, sub and non
    HC = int(0.01 * VN)
    SC = int(0.05 * VN)
    #NC = VN - HC - SC

    # Set of hub, sub and non-hubs

    HCN = N[:HC]
    SCN = N[HC:(HC + SC)]
    NCN = N[(HC + SC):]

    #CC location
    for i in HCN:
        C[i] = (random.randint(0,X),random.randint(0,Y))

    #PoI location
    for i in SCN:
        C[i] = (random.randint(0,X),random.randint(0,Y))

    #Survivor location
    for i in NCN:
        C[i] = (random.randint(max(C[i][0]  - 10, 0), min(X, C[i][0] + poi_radius)),random.randint(max(C[i][0]  - 10, 0), min(Y, C[i][0] + poi_radius)))

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

    # Introduce edges
    for u in G.nodes():
        for v in G.nodes():
            #CC and CC
            if u!= v and u in HCN and v in HCN and euclidean(C[u],C[v]) <= tower_range:
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

    print (len(G))
    print (len(G.edges()))
    print ((len(G.edges()) * 2)/ (len(G) * (len(G) - 1)))

    return G, HCN, SCN, NCN

# Area of deployment
X = 50
Y = 50
# Communication Radius
R = 20

tower_range = 20
ble_range = 10
poi_radius = 10
# Number of nodes in input DRN
# VN = 100
curr = os.getcwd()

for i in range(5):

    print (i)
    s = (i + 2) * 50
    os.chdir('graphs')

    G,H,S,N = generate(X, Y, s, R)

    nx.write_gml(G,'O' + str(s) + '.gml')
    pickle.dump(H, open('H' + str(i) + '.p', "wb"))
    pickle.dump(S, open('S' + str(i) + '.p', "wb"))
    pickle.dump(N, open('N' + str(i) + '.p', "wb"))

    os.chdir(curr)

