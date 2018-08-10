
import networkx as nx

def motif(G):

    #Node motif centrality
    mcount = 0

    #For directed graphs
    if G.is_directed():
        for u in G.nodes():

            for v in G.nodes():
                for w in G.nodes():
                    if G.has_edge(u,v) and G.has_edge(v,w) and G.has_edge(u,w):
                        mcount += 1


    return mcount

G1 = nx.erdos_renyi_graph(98,p = 0.0265,directed = True)
G2 = nx.read_gml('GBD.gml')

print (len(G1.edges()))
print (len(G2.edges()))

print (motif(G1))
print (motif(G2))

