from writer import *

import networkx as nx
import random,math
import numpy as np


def dist(u,v):

    d = math.pow((u[0] - v[0]),2) + math.pow((u[1] - v[1]),2)

    return math.sqrt(float(d))

N = 100
TRan = 100.0
Xlim = 100.0
Ylim = 100.0

G = nx.DiGraph()
G.add_nodes_from([i for i in range(N)])

Coor = [(random.uniform(0,Xlim),random.uniform(0,Ylim)) for u in range(N)]
print Coor

for u in G.nodes():
    for v in G.nodes():
        if v <= u:
            continue
        r = random.uniform(0,1)
        if dist(Coor[u],Coor[v]) < TRan and r < 0.25:
            G.add_edge(u,v)

print (len(G))
print (len(G.edges()))

d = np.array([G.in_degree(u) for u in G.nodes()])
d = d.argsort()[-1:][::-1]
print ([G.in_degree(u) for u in d])
neighbor(G, None, None, d,0)
writers(G, Coor, 0)
