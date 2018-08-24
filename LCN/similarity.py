import networkx as nx
import numpy as np
import math

from numpy import linalg as LA

def check(A,B,e):

    for eachA in range(len(A)):
        for eachB in range(len(A[0])):
            if abs(A[eachA][eachB] - B[eachA][eachB]) > e:
                return False

    return True
np.set_printoptions(suppress = True)
np.set_printoptions(precision = 6)


#G1 = nx.gnp_random_graph(10,p = 0.4,directed = True)
#G2 = nx.gnp_random_graph(10,p = 0.3,directed = True)

G1 = nx.DiGraph()
G2 = nx.DiGraph()

G1.add_edges_from([(0,1),(2,1),(2,3)])
G2.add_edges_from([(0,1),(1,2),(0,2),(0,3)])

#print (len(G1))
#print (len(G2))

inG1 = [G1.predecessors(u) for u in G1.nodes()]
inG2 = [G2.predecessors(u) for u in G2.nodes()]

outG1 = [G1.successors(u) for u in G1.nodes()]
outG2 = [G2.successors(u) for u in G2.nodes()]

print (inG1)
print (inG2)
print (outG1)
print (outG2)


oS = [[-1.0 for i in range(len(G2))] for j in range(len(G1))]
S = [[0.1 for i in range(len(G2))] for j in range(len(G1))]
#print (S)
e = 0.1
Iterate = 10000
counter = 0

while(counter < Iterate):

    print (counter)
    _S = [[0.0 for i in range(len(G2))] for j in range(len(G1))]
    for i in G1.nodes():

        for j in G2.nodes():
            if len(outG1[i]) == 0 or len(outG2[j]) == 0:
                continue

            for p in outG1[i]:
                for q in outG2[j]:
                    _S[i][j] += S[p][q]

    for i in G1.nodes():
        for j in G2.nodes():

            if len(inG1[i]) == 0 or len(inG2[j]) == 0:
                continue

            for p in inG1[i]:
                for q in inG2[j]:
                    _S[i][j] += S[p][q]


    #f = lambda x: x
    #sq = np.sum([[f(_S[u][v]) for v in range(len(_S[0]))] for u in range(len(_S))])

    PSD = B = np.dot(_S,np.transpose(_S))
    w,v = LA.eig(PSD)
    sq = math.sqrt(max(w))

    _S = [[float(_S[j][i])/float(sq) for i in range(len(G2))] for j in range(len(G1))]

    if check(S,_S,e) or check(oS,_S,e):
        break

    oS = S.copy()
    S = _S.copy()
    print (np.array(S))
    counter += 1
