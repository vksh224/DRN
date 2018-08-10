import networkx as nx
import pickle
import os
import numpy as np

def failures(G,f):

    n = int(f * 0.05 * len(G))

    i = 0
    while(i <= n):

        i = i + 1
        G.remove_node(np.random.choice(G.nodes()))

    return G

def pathcount(G,CC,S):

    p = 0.0
    for s in S:
        if s not in G.nodes():
            continue
        for c in CC:
            if c not in G.nodes():
                continue

            if nx.has_path(G,s,c):
                paths = nx.all_simple_paths(G, source = s, target = c,cutoff = 4)
                p += len(list(paths))

    return p

def efficiency(G,CC,S):

    e = 0.0
    den = 0.0
    for s in S:
        if s not in G.nodes():
            continue

        for c in CC:

            if c not in G.nodes():
                continue

            if nx.has_path(G, s, c):
                l = nx.shortest_path_length(G, source = s, target = c)
                e = e + 1.0/float(l)

            den = den + 1.0

    if den == 0:
        return 0

    return float(e)/den

def motif(G):

    m = 0
    for u in G.nodes():
        for v in G.nodes():
            if v <= u:
                continue

            for w in G.nodes():
                if w <= v:
                    continue

                if G.has_edge(u, v) and G.has_edge(v, w) and G.has_edge(u, w):
                    m += 1
    return m

def perf(G,CC,S):

    m = motif(G)
    print ("Number of nodes:",len(G))
    print ("Number of motifs in G:",m)
    print("Number of isolated nodes in G:", len(nx.isolates(G)))
    print ("Motifs density in G:",float(m)/float(len(G)))

    e = efficiency(G,CC,S)
    print("Average network efficiency of G:", e)

    p = pathcount(G,CC,S)
    print("Path count of G:", p)


curr = os.getcwd()

MC_G1 = pickle.load(open("GRN_Centrality.p", "rb"))
motifG = sum([each for each in MC_G1.values()])
motifG /= 3

print("Motifs density in GRN:", float(motifG) / 4441.0)

for ii in range(2,3):

    ss = (ii + 2) * 50
    print ("Number of nodes:",ss)
    print ("--------------------\n")

    for f in range(5):

        print ("Failure percentage:",f * 0.05)

        os.chdir('graphs')
        CC = pickle.load(open( "H" + str(ii) + ".p", "rb" ))
        S = pickle.load(open( "N" + str(ii) + ".p", "rb" ))

        O = nx.read_gml('refG' + str(ss) + '.gml')
        O = failures(O,f)

        GBD = nx.read_gml('GBD' + str(ss) + '.gml')
        GBD = failures(GBD, f)

        SP = nx.read_gml('S' + str(ss) + '.gml')
        SP = failures(SP, f)

        R = nx.read_gml('R' + str(ss) + '.gml')
        R = failures(R, f)

        K2 = nx.read_gml('KR2-' + str(ss) + '.gml')
        K2 = failures(K2, f)

        K4 = nx.read_gml('KR4-' + str(ss) + '.gml')
        K4 = failures(K4, f)

        K8 = nx.read_gml('KR8-' + str(ss) + '.gml')
        K8 = failures(K8, f)

        os.chdir(curr)

        print ('refG' + str(ss) + '.gml')
        perf(O.to_undirected(),CC,S)

        print('GBD' + str(ss) + '.gml')
        perf(GBD.to_undirected(), CC, S)

        print('S' + str(ss) + '.gml')
        perf(SP.to_undirected(), CC, S)

        print('R' + str(ss) + '.gml')
        perf(R.to_undirected(), CC, S)

        print('KR2-' + str(ss) + '.gml')
        perf(K2, CC, S)

        print('KR4-' + str(ss) + '.gml')
        perf(K4, CC, S)

        print('KR8-' + str(ss) + '.gml')
        perf(K8, CC, S)

        print("\n")



