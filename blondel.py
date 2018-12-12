import numpy as np
import math
import networkx as nx
import pickle,os
from copy import deepcopy,copy
from numpy import linalg as LA

def checks(A,B,e):

    for eachA in range(len(A)):
        for eachB in range(len(A[0])):
            if abs(A[eachA][eachB] - B[eachA][eachB]) > e:
                return False

    return True

def similarity(G1,G2,e):

    #G1 = nx.gnp_random_graph(10,p = 0.4,directed = True)
    #G2 = nx.gnp_random_graph(10,p = 0.3,directed = True)

    #print (len(G1))
    #print (len(G2))

    inG1 = [list(G1.predecessors(u)) for u in G1.nodes()]
    inG2 = [list(G2.predecessors(u)) for u in G2.nodes()]

    outG1 = [list(G1.successors(u)) for u in G1.nodes()]
    outG2 = [list(G2.successors(u)) for u in G2.nodes()]

    #print (inG1)
    #print (inG2)
    #print (outG1)
    #print (outG2)

    oS = [[-1.0 for i in range(len(G2))] for j in range(len(G1))]
    S = [[0.1 for i in range(len(G2))] for j in range(len(G1))]
    #print (S)
    #e = 0.00001
    Iterate = 100
    counter = 0

    while(counter < Iterate):
        #print (counter)
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

        if checks(S,_S,e) or checks(oS,_S,e):
            # print ("Counter:",counter)
            #print (S)
            return np.array(S)

        oS = copy(S)
        S = copy(_S)
        #print (np.array(S))
        counter += 1


def check(Y,threshold):
    for u in range(len(Y)):
        for v in range(len(Y[0])):
            if Y[u][v] > threshold:
                return False
    return True

def denominator(Y):
    sum = 0.0
    for u in range(len(Y)):
        for v in range(len(Y[0])):
            sum = sum + math.pow(Y[u][v],2)

    for u in range(len(Y)):
        for v in range(len(Y[0])):
            Y[u][v] /= sum

    return np.array(Y)

def blondelS(G1,G2,threshold):

    iterate = 0
    X = [[1.0 for u in range(len(G2))] for v in range(len(G1))]
    Y = deepcopy(X)
    while(True):
        #print ("Iteration ",iterate)
        #print (X)

        #Y = deepcopy(X)
        for e1 in G1.edges():
            for e2 in G2.edges():

                (p,i) = e1
                (q,j) = e2

                Y[p][q] += X[p][q]

                Y[i][j] += X[p][q]

        #   print(Y)

        if iterate > 0:
            if check(Y,threshold) or iterate > 100:
                print ("ITERATE:",iterate)
                # print (Y)
                return Y
                break

        Y = denominator(deepcopy(Y))
        X = deepcopy(Y)

        iterate += 1

'''
os.chdir('/usr/local/home/sr3k2/sandbox/journal GRN/modules/wsn/200')
G1 = nx.read_gml('mw0.gml')
mapping = pickle.load(open("mapping0.p","rb"))
G2 = nx.read_gml('grn_.gml')

Y = similarity(G1,G2,0.1)

a = 0.0
for u in mapping.keys():
    a = a + Y[u][mapping[u]]

print ("Average similarity:",float(a)/len(G1))
'''