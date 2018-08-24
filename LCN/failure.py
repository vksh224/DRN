import networkx as nx
import random

#import matplotlib.pyplot as plt

#ran = nx.read_gml('rd.gml')
od = nx.read_gml('od.gml')
md = nx.read_gml('md.gml')
md.remove_nodes_from(nx.isolates(md))

od_e = len(od.edges())
md_e = len(md.edges())

print (od_e,md_e)
for i in range(od_e - md_e):
    r = random.choice(od.edges())
    od.remove_edge(r[0],r[1])

f = [i for i in range(10)]
p = int(0.02 * len(md.nodes()))
print (p)
tr = float(len(od))
td = float(len(md))

print ("Total nodes Random graph:", tr)
print ("Total nodes mapped graph:", td)
print ("Total edges Random graph:", len(od.edges()))
print ("Total edges mapped graph:", len(md.edges()))

rdl = []
mdl = []

for each in f:

    n = p * each
    #print ("Number of nodes failed:",n)
    e = [random.choice(od.nodes()) for i in range(n)]
    od.remove_nodes_from(e)
    e = [random.choice(md.nodes()) for i in range(n)]
    md.remove_nodes_from(e)

    rdl.append(len(od.edges()))
    mdl.append(len(md.edges()))


print (rdl)
print (mdl)
