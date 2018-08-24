import networkx as nx
import random



N = [50, 100, 150, 200, 250]

for n in N:

    fname_m = str(n) + 'm.gml'
    fname_o = str(n) + 'o.gml'

    G_o = nx.read_gml(fname_o)
    G_m = nx.read_gml(fname_m)
    G_os = G_o.copy()
    diff = len(G_o.edges()) - len(G_m.edges())
    for i in range(diff):
        e = random.choice(G_os.edges())
        G_os.remove_edge(e[0],e[1])

    G_st = nx.minimum_spanning_tree(G_o.to_undirected())

    fname_os = str(n) + 'os.gml'
    fname_st = str(n) + 'st.gml'

    nx.write_gml(G_os,fname_os)
    nx.write_gml(G_st,fname_st)

    fh=open("G_o" + str(n) + ".adjlist",'wb')
    nx.write_adjlist(G_o, fh)

    fh=open("G_m" + str(n) + ".adjlist",'wb')
    nx.write_adjlist(G_m, fh)

    fh=open("G_os" + str(n) + ".adjlist",'wb')
    nx.write_adjlist(G_os, fh)

    fh=open("G_st" + str(n) + ".adjlist",'wb')
    nx.write_adjlist(G_st, fh)
