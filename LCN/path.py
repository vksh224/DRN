import networkx as nx
import random
import matplotlib.pyplot as plt

def cycle(G):

    cnt = []
    for u in G.nodes():
        for v in G.nodes():
            for w in G.nodes():
                if G.has_edge(u,v) and G.has_edge(v,w) and G.has_edge(w,u):
                    cnt.append([u,v,w])
                    G.remove_edge(u,v)
    return G


def multiplicity(G,h,n, c):

    cnt = 0
    for u in G.nodes():
        for v in h:
            #print u,v
            if nx.has_path(G,u,v):
                paths = nx.all_simple_paths(G, source = u, target = v,cutoff = c)
                cnt += len(list(paths))

    return float(cnt)/float(n)
def motifCount(G):


    cnt = 0
    for u in G.nodes():
        for v in G.nodes():
            for w in G.nodes():
                if G.has_edge(u,v) and G.has_edge(v,w) and G.has_edge(u,w):
                    cnt += 1


    return cnt


def avg_path(G,h,n):

    avg = 0.0
    cnt = 0.0
    for u in G.nodes():
        for v in h:
            #print ("iter", u,v)
            if nx.has_path(G,u,v):
                avg += 1.0/float(len(nx.shortest_path(G,source = u,target = v)))

            cnt += 1.0

    return float(avg)/float(n * len(h))


h = [1,2]
f = 5.0
od = nx.read_gml('od.gml')
md = nx.read_gml('md.gml')

n = len(od)
c = nx.average_shortest_path_length(od)

for i in range(len(od.edges()) - len(md.edges())):
    r = random.choice(od.edges())
    od.remove_edge(r[0],r[1])

od_e = len(od.edges())
md_e = len(md.edges())

#print len(od.edges())
#print len(md.edges())
mdl = []
rdl = []
for fail in range(6):

    #md.remove_nodes_from(nx.isolates(md))
    od.remove_nodes_from([random.choice(list(set(od.nodes()) - set(h))) for i in range(int(float(f)/100.0 * float(n)))])
    md.remove_nodes_from([random.choice(list(set(md.nodes()) - set(h))) for i in range(int(float(f)/100.0 * float(n)))])

    #od.remove_edges_from([random.choice(list(set(od.edges()))) for i in range(int(float(f)/100.0 * float(od_e)))])
    #md.remove_edges_from([random.choice(list(set(md.edges()))) for i in range(int(f/100.0 * float(md_e)))])

    rdl.append(multiplicity(od, h, n, c))
    mdl.append(multiplicity(md, h, n, c))

print rdl
print mdl

