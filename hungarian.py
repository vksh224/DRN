import networkx as nx

from munkres import Munkres
from bioDRN.blondel import *
from bioDRN.find_tiers import *

def reverse(Y):

    for i in range(len(Y)):
        for j in range(len(Y[0])):
            Y[i][j] = - float(Y[i][j])

    return Y

G1 = nx.DiGraph()
G1.add_edges_from([(0,1), (1,2)])
G1_t1, G1_t2,G1_t3 = [2],[1],[0]

G2 = nx.DiGraph()
G2.add_edges_from([(0,2), (2,1), (0,1),(2,3)])
G2_t1, G2_t2, G2_t3 = [1,3],[2],[0]

Y = blondelS(G1,G2,0.01)
print ( Y)

Y = reverse(Y)
Y = np.array(Y)

m = Munkres()

indexes = m.compute(Y[G1_t1, :][:, G2_t1])
print (indexes)

