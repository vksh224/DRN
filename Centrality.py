import networkx as nx
import pickle

def motif(G):

    #Node motif centrality
    NMC = {}
    #List of nodes sharing motif (NSM) with current node
    #NSM = [[] for _ in G.nodes()]



    for u in G.nodes():
        NMC[u] = 0

    #For directed graphs
    if G.is_directed():
        for u in G.nodes():

            #print ("Node:",u)
            for v in G.nodes():
                for w in G.nodes():

                    if G.has_edge(u,v) and G.has_edge(v,w) and G.has_edge(u,w):
                        NMC[u] += 1
                        NMC[v] += 1
                        NMC[w] += 1

                        '''
                        if v not in NSM[u]:
                            NSM[u].append(v)

                        if w not in NSM[u]:
                            NSM[u].append(w)

                        if u not in NSM[v]:
                            NSM[v].append(u)

                        if w not in NSM[v]:
                            NSM[v].append(w)

                        if u not in NSM[w]:
                            NSM[w].append(u)

                        if v not in NSM[w]:
                            NSM[w].append(v)
                        '''

    #For undirected graphs
    else:
        for u in G.nodes():
            for v in G.nodes():
                if v <= u:
                    continue
                for w in G.nodes():
                    if w <= v:
                        continue

                    if G.has_edge(u, v) and G.has_edge(v, w) and G.has_edge(u, w):
                        NMC[u] += 1
                        NMC[v] += 1
                        NMC[w] += 1

    return NMC

'''
G = nx.read_gml('Ecoli-1.gml')
G = nx.convert_node_labels_to_integers(G,first_label = 0)
NMC,NSM = motif(G)

pickle.dump(NMC, open("NMC.p", "wb"))
pickle.dump(NSM, open("NSM.p", "wb"))
print (NSM)
'''